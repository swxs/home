import os
import sys
import asyncio
import errno
import time
import signal
from typing import Optional
from importlib import reload
from importlib import import_module
from thriftpy2.rpc import make_server
from thriftpy2.contrib.aio.protocol.binary import TAsyncBinaryProtocolFactory
from thriftpy2.contrib.aio.transport.buffered import TAsyncBufferedTransportFactory
from thriftpy2.contrib.aio.socket import TAsyncServerSocket
from thriftpy2.contrib.aio.processor import TAsyncProcessor, TApplicationException
from thriftpy2.server import TServer
from thriftpy2.transport import TTransportException
from tornado.process import cpu_count, gen_log, _reseed_random
from tornado.util import errno_from_exception
import settings
import fire

from rpc.client_pool import BaseDispatcher


class TAsyncServer(TServer):
    def __init__(self, *args, **kwargs):
        self.loop = None
        if settings.OS.upper() == 'WINDOWS':
            signal.signal(signal.SIGTERM, lambda sig, frame: self.on_grace_exit())
            signal.signal(signal.SIGINT, lambda sig, frame: self.on_force_exit())
        else:
            signal.signal(signal.SIGUSR1, lambda sig, frame: self.on_reload())
            signal.signal(signal.SIGCHLD, lambda sig, frame: self.on_child_quit())
            signal.signal(signal.SIGTERM, lambda sig, frame: self.on_grace_exit())
            signal.signal(signal.SIGINT, lambda sig, frame: self.on_force_exit())

        TServer.__init__(
            self,
            *args,
            **kwargs
        )
        self.closed = False
        self._task_id = None
        self.children = {}
        self.num_restarts = 0
        self._reload_pid_list = []
        self._exit_code = 0
        self._active_clients = 0
        self._last_grace_exit_time = 0
        self.max_restarts = 100

    def start(self, num_processes: Optional[int] = 0, max_restarts: int = None) -> None:
        if max_restarts:
            self.max_restarts = max_restarts
        if settings.OS.upper() == 'WINDOWS':
            pass
        else:
            self.fork_processes(num_processes)
        loop = asyncio.get_event_loop()
        if settings.OS.upper() == 'WINDOWS':
            # loop.add_signal_handler(signal.SIGTERM, self.on_grace_exit)
            # loop.add_signal_handler(signal.SIGINT, self.on_force_exit)
            pass
        else:
            loop.add_signal_handler(signal.SIGUSR1, self.on_reload)
            loop.add_signal_handler(signal.SIGTERM, self.on_grace_exit)
            loop.add_signal_handler(signal.SIGINT, self.on_force_exit)
        reload(settings)
        self.loop = loop
        # self.logger = get_logging('rpc.main_rpc_server', file_name="main_rpc_server.log")

    def serve(self):
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
                ms = int((time.time() - processor.last_time) * 1000)
                # self.logger.info('%s %sms' % (processor.current_api, ms))

        except TTransportException:
            pass
            # self.logger.exception('Transport failed')
        except asyncio.TimeoutError:
            api = processor.current_api
            if api:
                ms = int((time.time() - processor.last_time) * 1000)
                pass
                # self.logger.error('PROCESS %s Timeout %sms' % (api, ms))
        except Exception as x:
            pass
            # self.logger.exception(x)

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

    def on_reload(self):
        if settings.OS.upper() == 'WINDOWS':
            return
        if self.task_id() is not None:
            # 子进程
            asyncio.ensure_future(rpc_server.close(-1), loop=self.loop)
            return
        if self._reload_pid_list:
            # 正在reload
            print('reloading, stale pid = ' + str(self._reload_pid_list))
            return
        self.num_restarts = 0
        child_pid_list = self.child_pid()
        if child_pid_list:
            self._reload_pid_list = child_pid_list
            last_pid = child_pid_list[-1]
            os.kill(last_pid, signal.SIGUSR1)

            def reload_retry(sig, frame):
                if child_pid_list and last_pid == child_pid_list[-1]:
                    try:
                        os.kill(last_pid, signal.SIGUSR1)
                    except:
                        pass

            # 无奈，signal.SIGUSR1小概率不触达，设置1s后重试
            signal.signal(signal.SIGALRM, reload_retry)
            signal.alarm(1)

    def on_child_quit(self):
        reload_pid_list = self._reload_pid_list
        while reload_pid_list:
            try:
                last_pid = reload_pid_list[-1]
                os.kill(last_pid, signal.SIGUSR1)
                return
            except ProcessLookupError:
                # worker is exited
                try:
                    reload_pid_list.remove(last_pid)
                except Exception:
                    pass

    def on_grace_exit(self):
        if self.task_id() is not None:
            # 子进程
            asyncio.ensure_future(rpc_server.close(), loop=self.loop)
            return
        else:
            current = time.time()
            if current - self._last_grace_exit_time > 1:
                self._last_grace_exit_time = current
                os.kill(0, signal.SIGTERM)

    def on_force_exit(self):
        if self.task_id() is None:
            os.kill(0, signal.SIGINT)
        self.loop.stop()
        sys.exit(0)

    def task_id(self):
        return self._task_id

    def child_pid(self):
        return list(self.children.keys())

    def fork_processes(self, num_processes: Optional[int]) -> int:
        assert self._task_id is None
        if num_processes is None or num_processes <= 0:
            num_processes = cpu_count()
        gen_log.info("Starting %d processes", num_processes)
        self.children = {}
        for i in range(num_processes):
            id = self.start_child(i)
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
            reload_pid_list = self._reload_pid_list
            if reload_pid_list:
                try:
                    reload_pid_list.remove(pid)
                    os.kill(reload_pid_list[-1], signal.SIGUSR1)
                except:
                    pass
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
        pid = os.fork()
        if pid == 0:
            # child process
            _reseed_random()
            self._task_id = i
            return i
        else:
            self.children[pid] = i
            return None


def save_pid(port, pid):
    with open('%s/rpc_%s.pid' % (settings.TEMP_PATH, port), 'w') as wfile:
        wfile.write(str(pid))


def find_services(thrift):
    services = set()
    thrifts = []
    for key, val in vars(thrift).items():
        if type(val) == type:
            for base in val.__bases__[::-1]:
                if hasattr(base, 'thrift_service'):
                    services.update(base.thrift_services)
            services.update(val.thrift_services)
            thrifts.append(val)
    return thrifts, services


def _make_server(port):
    if port:
        server_socket = TAsyncServerSocket(
            host="0.0.0.0", port=port,
            client_timeout=None)
    else:
        raise ValueError("port must be provided.")
    try:
        import socket
        s = socket.socket()
        s.bind(('0.0.0.0', port))
        s.close()
    except OSError:
        gen_log.exception('port %s is in use' % port)
    server_socket.listen()
    save_pid(port, os.getpid())

    global rpc_server
    rpc_server = TAsyncServer(None, server_socket,
                              iprot_factory=TAsyncBinaryProtocolFactory(),
                              itrans_factory=TAsyncBufferedTransportFactory())
    rpc_server.start()

    pid = os.getpid()
    # rpc_server.logger.info(f'rpc server[pid={pid}] is started on 0.0.0.0:{port}...')
    module_list = settings.RPC_MODULE_LIST

    dispatchers = []
    services = set()
    thrifts = []
    for module in module_list:
        module = import_module(module)
        for key, val in vars(module).items():
            if issubclass(val, BaseDispatcher):
                dispatchers.extend(set(val))
            elif hasattr(val, '__thrift_meta__'):
                data = find_services(val)
                thrifts.extend(data[0])
                services.update(data[1])

    Dispatcher = type('Dispatcher', tuple(dispatchers), {})
    Service = type('Service', tuple(thrifts), {'thrift_services': services})

    rpc_server.processor = TAsyncProcessor(Service, Dispatcher())

    return rpc_server


def main(port=settings.RPC_SERVER_PORT):
    server = _make_server(port)
    server.serve()


if __name__ == '__main__':
    fire.Fire(main)
