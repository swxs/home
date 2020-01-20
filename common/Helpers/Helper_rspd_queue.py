# File    : Helper_rspd_queue.py
# Author  : gorden
# Time    : 2018/9/11 23:54
from copy import copy

import settings
from apps.consts.const import undefined
from apps.utils.survey.rspd_data import RspdData
from common.Helpers.DBHelper_Redis import RedisDBHelper
from common.Helpers.Helper_msgqueue import MessageQueueFactory
from common.Metaclass.Singleton import Singleton
from common.Utils.utils import serialize


class RspdQueue(metaclass=Singleton):
    """
        答卷处理业务逻辑
    """

    # cmd 和对应的处理函数的映射
    CMD_WHAT_SURVEY_START = "survey_start"
    CMD_WHAT_SURVEY_END = "survey_end"
    CMD_HANDLER_DICT = {
        CMD_WHAT_SURVEY_START: "survey_start_handler",
        CMD_WHAT_SURVEY_END: "survey_end_handler"
    }

    def __init__(self, channel="rspd_queue"):
        factory = MessageQueueFactory()
        engine = settings.MESSAGE_QUEUE_CONFIG.get("engine", None)
        storage = settings.MESSAGE_QUEUE_CONFIG.get("storage", None)
        self.channel = channel
        self.queue = factory.create(engine, storage)
        self.redis_helper = RedisDBHelper()
        self.redis_client = self.redis_helper.client

    def prepare_rspd(self, **kwargs):
        """
            开始答卷接口调用此函数，发出处理rspd队列的消息
        :param kwargs:
            {
                "source": source,
                "survey_code": survey_code,
                "store_id": store_id,
                "seq": seq,
                "timestamp": timestamp,
                "signature": signature
            }
        :return: seq
        """
        kwargs['seq'] = self.redis_helper.get_next_seq(f"rspd_seq")
        cmd = copy(self.queue.CMD)
        cmd['what'] = self.CMD_WHAT_SURVEY_START
        cmd['channel'] = self.channel
        cmd['data'] = kwargs
        self.queue.send_command(cmd)
        return kwargs['seq']

    def prepare_save_rspd(self, **kwargs):
        """
            完成答卷调用此函数，发出处理rspd队列的消息
        :param kwargs:
            {
                "seq": seq,
                "survey_id": survey_id,
                "wx_img": wx_img,
                "weixin_nickname": weixin_nickname,
                "weixin_sex": weixin_sex,
                "weixin_addr": weixin_addr,
                "weixin_openId": weixin_openId,
                "weixin_refresh_token": weixin_refresh_token,
                "os": os,
                "browser": browser,
                "source": source,
                "ip": ip,
                "answers": answers,
                "status": status,
                "ticket_status": ticket_status,
                "finish": finish,
                "start": start,
                "time_used": time_used,
            }
        :return:
        """
        cmd = copy(self.queue.CMD)
        cmd['what'] = self.CMD_WHAT_SURVEY_END
        cmd['channel'] = self.channel

        # 预处理，msgpack无法转换undefined
        cmd['data'] = {k: v for k, v in kwargs.copy().items() if v != undefined}
        self.queue.send_command(cmd)

    def handle_rspd(self):
        self.queue.subscribe(self.channel)
        return self.queue.receive_command(self.cmd_handler)

    def cmd_handler(self, cmd):
        return getattr(self, self.CMD_HANDLER_DICT.get(cmd.get('what')))(cmd)

    def survey_start_handler(self, cmd):
        return RspdData.create_rspd_data(**cmd.get('data'))

    def survey_end_handler(self, cmd):
        rspd = RspdData.get_rspd_data(seq=cmd.get('data')['seq'])
        return rspd.update_rspd_data(**cmd.get('data'))
        #
        # # 暂时不用
        # # utils.send_error_emails(rspd_data, settings.DEFAULT_SURVEY_CODE)
        # survey = survey_utils.get_survey(data.get("survey_id"))
        # if rspd_data.answers and utils.create_ticket_condition(rspd_data):
        #     ticket_utils.create_ticket(subject='低分报告', survey_id=survey.oid, rspd_data_id=rspd_data.oid)


def main():
    q = RspdQueue()
    data1 = {"survey_id": "1323232"}
    seq = q.prepare_rspd(**data1)
    data2 = {"seq": seq, "openid": "123456"}
    print(data2)
    q.prepare_save_rspd(**data2)

    data1 = {"survey_id": "1323232"}
    seq = RspdQueue().prepare_rspd(**data1)
    data2 = {"seq": seq, "openid": "123456"}
    print(data2)
    RspdQueue().prepare_save_rspd(**data2)


if __name__ == "__main__":
    main()