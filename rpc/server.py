import os
import sys
import asyncio
import errno
import time
import datetime
import signal
import multiprocessing
from typing import Optional
from importlib import import_module
from thriftpy2.contrib.aio.protocol.binary import TAsyncBinaryProtocolFactory
from thriftpy2.contrib.aio.transport.buffered import TAsyncBufferedTransportFactory
from thriftpy2.contrib.aio.socket import TAsyncServerSocket
from thriftpy2.contrib.aio.processor import TAsyncProcessor as TProcessor, TApplicationException
from thriftpy2.server import TServer
from thriftpy2.transport import TTransportException
from tornado.process import cpu_count, gen_log, _reseed_random
from tornado.util import errno_from_exception
from .pipe import PipeCommand
from .errors import NetworkTimeout


class TAsyncProcessor(TProcessor):
    async def process(self, iprot, oprot):
        self.current_api = None
        api, seqid, result, call = await self.process_in(iprot)

        if isinstance(result, TApplicationException):
            return await self.send_exception(oprot, api, result, seqid)

        try:
            result.success = await asyncio.wait_for(call(), timeout=3)
        except asyncio.TimeoutError as e:
            self.handle_exception(e, result)
        except Exception as e:
            # raise if api don't have throws
            self.handle_exception(e, result)

        if not result.oneway:
            await self.send_result(oprot, api, result, seqid)


class TAsyncServer(TServer):
    def __init__(self, *args, **kwargs):
        self.loop = None
        if os.name == 'nt':
            signal.signal(signal.SIGTERM, lambda sig, frame: self.shutdown())
        else:
            signal.signal(signal.SIGUSR1, lambda sig, frame: self.reload())
            signal.signal(signal.SIGTERM, lambda sig, frame: self.shutdown())

        TServer.__init__(self, *args, **kwargs)
        self.closed = False
        self.num_processes = 0
        self._task_id = None
        self.children = {}
        self.num_restarts = 0
        self._exit_code = 0
        self._active_clients = 0
        self._last_grace_exit_time = 0
        self.max_restarts = 100
        self._reloading_tid = None

        pipe_cmd = PipeCommand()
        pipe_cmd.register_handler(PipeCommand.Shutdown, self.on_quit)
        pipe_cmd.register_handler(PipeCommand.Reload, self.on_reload)
        self._pipe_command = pipe_cmd
        self.subproc_pipe_fds = None

    def start(self) -> None:
        if os.name == 'nt':
            pass
        else:
            self.fork_processes(self.num_processes)
        self.loop = asyncio.get_event_loop()

    def shutdown(self):
        if self.subproc_pipe_fds:
            for fd in self.subproc_pipe_fds:
                if fd > 0:
                    os.write(fd, bytes([PipeCommand.Shutdown]))

    def on_quit(self):
        """
        退出所在工作进程，且不再重启
        """
        self.loop.create_task(self.close(0))

    def _reload_next(self):
        """
        一个工作进程退出后重启下一个
        """
        reloading_tid = self._reloading_tid
        if reloading_tid is None:
            reloading_tid = 0
        else:
            reloading_tid += 1
        if reloading_tid < len(self.subproc_pipe_fds):
            os.write(self.subproc_pipe_fds[reloading_tid], bytes([PipeCommand.Reload]))
            self._reloading_tid = reloading_tid
        else:
            self._reloading_tid = None

    def reload(self):
        """
        主进程依次通知工作进程处理完请求退出
        """
        self._reload_next()
        self.num_restarts = 0

    def on_reload(self):
        """
        工作进程对PipeCommand.Reload指令的处理函数
        """
        self.loop.create_task(self.close(-1))

    def serve(self):
        gen_log.info(f"{datetime.datetime.now()} [rpc]   rpc server started on port [5000]")
        self.init_server()
        self.loop.run_forever()
        sys.exit(self._exit_code)

    def init_server(self):
        self.server = self.loop.run_until_complete(self.trans.accept(self.handle))

    async def handle(self, client):
        self._active_clients += 1
        itrans = self.itrans_factory.get_transport(client)
        otrans = self.otrans_factory.get_transport(client)
        iprot = self.iprot_factory.get_protocol(itrans)
        oprot = self.oprot_factory.get_protocol(otrans)
        processor = self.processor
        try:
            while not client.reader.at_eof():
                await asyncio.wait_for(processor.process(iprot, oprot), timeout=10)
        except TTransportException:
            pass
        except asyncio.TimeoutError:
            raise NetworkTimeout
        except Exception as x:
            pass

        itrans.close()
        self._active_clients -= 1
        if self.closed and self._active_clients == 0:
            self.loop.stop()

    async def close(self, exit_code=0):
        self.server.close()
        await self.server.wait_closed()
        self.closed = True
        self._exit_code = exit_code
        if self._active_clients == 0:
            self.loop.stop()

    @property
    def task_id(self):
        return self._task_id

    def fork_processes(self, num_processes: Optional[int]) -> int:
        assert self.task_id is None
        if num_processes is None or num_processes <= 0:
            num_processes = cpu_count()
        self.children = {}
        self.subproc_pipe_fds = [-1] * num_processes
        for i in range(num_processes):
            id = self.start_child(i)
            # sub_process 直接返回
            if id is not None:
                return id
        self.num_restarts = 0
        while self.children:
            try:
                pid, status = os.wait()
            except OSError as e:
                if errno_from_exception(e) == errno.EINTR:
                    continue
                raise
            if pid not in self.children:
                continue
            id = self.children.pop(pid)
            if self._reloading_tid == id:
                self._reload_next()
            if os.WIFSIGNALED(status):
                gen_log.warning(
                    "child %d (pid %d) killed by signal %d, restarting",
                    id,
                    pid,
                    os.WTERMSIG(status),
                )
            elif os.WEXITSTATUS(status) != 0:
                gen_log.warning(
                    "child %d (pid %d) exited with status %d, restarting",
                    id,
                    pid,
                    os.WEXITSTATUS(status),
                )
            else:
                gen_log.info("child %d (pid %d) exited normally", id, pid)
                continue
            self.num_restarts += 1
            if self.num_restarts > self.max_restarts:
                raise RuntimeError("Too many child restarts, giving up")
            new_id = self.start_child(id)
            if new_id is not None:
                return new_id
        sys.exit(0)

    def start_child(self, i: int) -> Optional[int]:
        old_fd = self.subproc_pipe_fds[i]
        if old_fd > 0:
            os.close(old_fd)
        fds = os.pipe()
        pid = os.fork()
        if pid == 0:
            # child process
            os.close(fds[1])
            self._pipe_command.start(fds[0])
            _reseed_random()
            self._task_id = i
            return i
        else:
            os.close(fds[0])
            self.subproc_pipe_fds[i] = fds[1]
            self.children[pid] = i
            return None
