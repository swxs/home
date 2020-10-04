import yaml
import signal
from functools import partial
from tornado.util import ObjectDict

from rpc.main import make_server, force_exit


def run(port=None, module_list=None):
    assert port
    assert module_list
    server = make_server(port=port, module_list=module_list)
    signal.signal(signal.SIGINT, partial(force_exit, server))
    server.serve()


if __name__ == '__main__':
    with open("./rpc/config.yaml", 'r') as fp:
        rpc_settings = ObjectDict(yaml.safe_load(fp))

    port = rpc_settings.port
    module_list = rpc_settings.module_list
    run(port, module_list)
