# -*- coding: utf-8 -*-

import os
import sys
import typing
import click
import logging
import logging.config
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
import settings


logging.config.fileConfig('logging.ini')
logger = logging.getLogger("main")


@click.command()
@click.option(
    '-m',
    '--mode',
    required=True,
    type=click.Choice(['WEB', 'RPC'], case_sensitive=False),
    default='WEB',
    show_default=True,
)
@click.option(
    '-t',
    '--task',
    required=True,
    type=click.Choice(['START', 'STOP'], case_sensitive=False),
    default='START',
    show_default=True,
)
@click.argument('ports', nargs=1, type=int)
def main(mode, task, ports):
    if mode == "WEB" and task == "START":
        from web import main as web_main

        if not ports:
            ports = settings.SITE_PORT

        web_main.main(ports)


if __name__ == "__main__":
    main()
