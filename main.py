# -*- coding: utf-8 -*-

import os
import sys
import logging
import logging.config
import click

import settings
from web import main as web_main
from rpc import main as rpc_main
from mq import main as mq_main

logging.config.fileConfig('logging.ini')
logger = logging.getLogger("main")


def main():
    web_main.main(settings.SITE_PORT)



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

    @property
    def task_id(self):
        return self._task_id

if __name__ == "__main__":
    main()
