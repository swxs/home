import os
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


    def gen_dispatcher(self, path):
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

        thrifts_list = []
        dispatchers = []
        services_set = set()
        for root, dirs, files in os.walk(os.path.join(path, "apps")):
            for filename in files:
                if filename.endswith('.py') or filename.endswith('.PY'):
                    module_dispatchers = []
                    module = self._path_2_module(path=os.path.join(root, filename), root=path)    
                    for key, val in vars(module).items():
                        is_dispatcher = False
                        try:
                            is_dispatcher = issubclass(val, BaseDispatcher)
                        except TypeError:
                            pass
                        if is_dispatcher:
                            module_dispatchers.append(val)
                        elif hasattr(val, '__thrift_meta__'):
                            (thrifts, services) = find_services(val)
                            thrifts_list.extend(thrifts)
                            services_set.update(services)

            base_dispatchers = []
            for idx, d1 in enumerate(module_dispatchers, 1):
                for d2 in module_dispatchers[idx:]:
                    if issubclass(d1, d2):
                        base_dispatchers.append(d2)
                    elif issubclass(d2, d1):
                        base_dispatchers.append(d1)
            dispatchers.extend(list(set(module_dispatchers) - set(base_dispatchers)))

        Dispatcher = type('Dispatcher', tuple(dispatchers), {})
        Service = type('Service', tuple(thrifts_list), {'thrift_services': services_set})
        
        self.processor = TAsyncProcessor(Service, Dispatcher())
        return self