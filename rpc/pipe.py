#!/usr/bin/python

"""
进程间管道通信异步接口, 写管道为同步阻塞
"""

import os
import asyncio


class PipeProtocol(asyncio.Protocol):
    def __init__(self, pipecmd):
        super(PipeProtocol, self).__init__()
        self._pipecmd = pipecmd

    def data_received(self, data):
        for cmd in data:
            self._pipecmd.do_handler(cmd)

    def eof_received(self):
        exit()


class PipeCommand(object):
    Shutdown = 0
    Reload = 1

    def __init__(self):
        self._handlers = {}

    def register_handler(self, cmd, handler):
        assert isinstance(cmd, int) and 0 <= cmd <= 255
        self._handlers[cmd] = handler

    def do_handler(self, cmd):
        handler = self._handlers.get(cmd)
        if handler:
            handler()

    def create_protocol(self):
        return PipeProtocol(self)

    def start(self, pipe_fd):
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(loop.connect_read_pipe(self.create_protocol, open(pipe_fd)))
