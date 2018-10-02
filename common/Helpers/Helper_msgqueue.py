# File    : Helper_msgqueue.py
# Author  : gorden
# Time    : 2018/9/7 17:52
import traceback
from abc import ABCMeta, abstractmethod
from copy import copy

import time

from tornado.util import ObjectDict

import settings
from common.Utils.log_utils import getLogger
from common.Utils.utils import deserialize, serialize

log = getLogger("Helper_msgqueue.py")

ID = ":id"
JOBS = ":jobs"
PENDING = ":pending"
PROCESSING = ":processing"
FAILED = ":failed"
SUCCEEDED = ":succeeded"


class MessageQueueMix(object):
    __metaclass__ = ABCMeta
    """docstring for MessageQueueMix"""

    def __init__(self):
        pass

    @abstractmethod
    def _setup_client(self):
        pass

    @abstractmethod
    def _create_client(self):
        pass

    @abstractmethod
    def send_command(self, cmd):
        pass

    @abstractmethod
    def receive_command(self, handler):
        pass


class MessageQueueRedis(MessageQueueMix):
    client = None
    CMD = dict(what=None, channel=None, data=None)

    def __init__(self, settings):
        super(MessageQueueRedis, self).__init__()
        self.settings = settings
        self._setup_client()
        self.channel = None
        self.channel_jobs = None
        self.channel_pendding = None
        self.channel_processing = None
        self.channel_succeeded = None
        self.channel_failed = None

    def _setup_client(self):
        if self.client is None:
            self._create_client()

    def _create_client(self):
        import redis
        if 'max_connections' in self.settings:
            connection_pool = redis.ConnectionPool(**self.settings)
            settings = copy(self.settings)
            del settings['max_connections']
            settings['connection_pool'] = connection_pool
        else:
            settings = self.settings
        self.client = redis.Redis(**settings)

    def send_command(self, cmd):
        job_id = self.client.incr(f"{cmd.get('channel')}{ID}")
        pipe = self.client.pipeline()
        pipe.lpush(f"{cmd.get('channel')}{PENDING}", job_id)
        pipe.hset(f"{cmd.get('channel')}{JOBS}", job_id, serialize(cmd))
        pipe.execute()

    def subscribe(self, channel):
        self.channel = channel
        self.channel_jobs = f"{self.channel}{JOBS}"
        self.channel_pendding = f"{self.channel}{PENDING}"
        self.channel_processing = f"{self.channel}{PROCESSING}"
        self.channel_succeeded = f"{self.channel}{SUCCEEDED}"
        self.channel_failed = f"{self.channel}{FAILED}"

    def receive_command(self, handler):
        import redis
        job_id = self.client.brpoplpush(self.channel_pendding, self.channel_processing)
        try:
            cmd = self.client.hget(self.channel_jobs, job_id)

            result = handler(deserialize(cmd))
            self.client.lpush(self.channel_succeeded, job_id)
            return result
        except Exception:
            log.exception("ERROR while handling cmd")
            try:
                self.client.lpush(self.channel_failed, job_id)
            except redis.ResponseError:
                log.exception("ERROR while pushing to channel_failed")
        finally:
            try:
                self.client.lrem(self.channel_processing, 1, job_id)
            except redis.ResponseError:
                log.exception("ERROR while removing channel_processing")


class MessageQueueRabitMQ(MessageQueueMix):
    """docstring for MessageQueueRabitMQ"""

    def __init__(self, arg):
        super(MessageQueueRabitMQ, self).__init__()
        self.arg = arg


class MessageQueueFactory(object):
    def create(self, name, storage_settings):
        method = getattr(self, '_create_%s' % name, None)
        if method is None:
            raise ValueError('Engine "%s" is not supported' % name)
        return method(storage_settings)

    def _create_redis(self, storage_settings):
        storage_settings = copy(storage_settings)
        return MessageQueueRedis(storage_settings)

    def _create_rabbitmq(self, storage_settings):
        return MessageQueueRabitMQ(storage_settings)

