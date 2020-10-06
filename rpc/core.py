import os
import asyncio
from thriftpy2.contrib.aio.processor import TAsyncProcessor as TProcessor, TApplicationException
from .dispatcher import BaseDispatcher


class TAsyncProcessor(TProcessor):
    """
    简介
    ----------
    主入口， 尝试加载所有的Handler， 并运行

    参数
    ----------
    Application :

    """

    async def process(self, iprot, oprot):
        self.current_api = None
        api, seqid, result, call = await self.process_in(iprot)

        if isinstance(result, TApplicationException):
            return await self.send_exception(oprot, api, result, seqid)

        try:
            result.success = await asyncio.wait_for(call(), timeout=3)
        except asyncio.TimeoutError as e:
            self.handle_exception(e, result)
        except Exception as e:
            # raise if api don't have throws
            self.handle_exception(e, result)

        if not result.oneway:
            await self.send_result(oprot, api, result, seqid)

    def register(self, path):
        thrifts = set()
        services = set()
        dispatchers = set()
        for root, dirs, files in os.walk(os.path.join(path, "rpc")):
            for filename in files:
                if filename.endswith('.py') or filename.endswith('.PY'):
                    module_dispatchers = []
                    module = self._path_2_module(path=os.path.join(root, filename), root=path)
                    if module:
                        for key, val in vars(module).items():
                            is_dispatcher = False
                            try:
                                is_dispatcher = issubclass(val, BaseDispatcher)
                            except TypeError:
                                pass
                            if is_dispatcher:
                                dispatchers.add(val)
                            elif hasattr(val, '__thrift_meta__'):
                                (__thrifts, __services) = self.find_services(val)
                                thrifts.update(__thrifts)
                                services.update(__services)

        Dispatcher = type('Dispatcher', tuple(dispatchers), {})
        Service = type('Service', tuple(services), {'thrift_services': services})

        self.processor = TAsyncProcessor(Service, Dispatcher())
        return self

    @staticmethod
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

    @staticmethod
    def _path_2_module(path='', root=''):
        if path:
            module = path.replace('\\', '/').replace(root.replace('\\', '/'), '')
            if module.startswith('/'):
                module = module[1:]
            module = module.replace('.py', '').replace('.PY', '')
            if set('.#~') & set(module):
                return None
            module = module.replace('/', '.').strip()
            if module:
                return module
        return None
