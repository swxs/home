import os
import sys
import logging
import asyncio
import datetime
from typing import Optional
from importlib import import_module
from thriftpy2.server import TServer
from thriftpy2.transport import TTransportException
from thriftpy2.contrib.aio.protocol.binary import TAsyncBinaryProtocolFactory
from thriftpy2.contrib.aio.transport.buffered import TAsyncBufferedTransportFactory
from tornado.util import errno_from_exception
from .pipe import PipeCommand


logger = logging.getLogger("main.rpc.server")


class TAsyncServer(TServer):
    def __init__(
        self,
        processor,
        trans,
        itrans_factory=None,
        iprot_factory=None,
        otrans_factory=None,
        oprot_factory=None,
        loop=None,
    ):
        if itrans_factory is None:
            itrans_factory = TAsyncBinaryProtocolFactory()
        if iprot_factory is None:
            iprot_factory = TAsyncBufferedTransportFactory()
        TServer.__init__(
            self,
            processor,
            trans,
            itrans_factory=itrans_factory,
            iprot_factory=iprot_factory,
            otrans_factory=otrans_factory,
            oprot_factory=oprot_factory,
        )
        if loop is None:
            self.loop = asyncio.get_event_loop()
        else:
            self.loop = loop
        self.closed = False

    def serve(self):
        self.loop.run_until_complete(self.trans.accept(self.handle))

    async def handle(self, client):
        self.trans.listen()
        while not self.closed:
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
            except Exception as x:
                logger.exception(x)
            itrans.close()
            otrans.close()

    async def close(self):
        self.closed = True
