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


if __name__ == "__main__":
    main()
