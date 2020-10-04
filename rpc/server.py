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


class TAsyncServer(TServer):
    def __init__(self, *args, **kwargs):
        TServer.__init__(self, *args, **kwargs)
        self.loop = None
        self.closed = False
        self.num_processes = 0
        self._task_id = None
        self.children = {}
        self.num_restarts = 0
        self._exit_code = 0
        self._active_clients = 0
        self._last_grace_exit_time = 0
        self.max_restarts = 100

    def start(self) -> None:
        if os.name == 'nt':
            pass
        else:
            self.fork_processes(self.num_processes)
        self.loop = asyncio.get_event_loop()

    def on_quit(self):
        """
        退出所在工作进程，且不再重启
        """
        self.loop.create_task(self.close(0))

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


