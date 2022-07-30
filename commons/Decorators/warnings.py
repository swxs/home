import asyncio
import logging
import functools

logger = logging.getLogger("helper.DHelper_warning")


def abandoned(function):
    if asyncio.iscoroutinefunction(function):

        @functools.wraps(function)
        async def wrapped_async(*args, **kwargs):
            logger.warning(
                f"{function.__code__.co_filename}:{function.__code__.co_firstlineno}[{function.__name__}] will be abandoned"
            )

            return await function(*args, **kwargs)

        return wrapped_async

    else:

        @functools.wraps(function)
        def wrapped_sync(*args, **kwargs):
            logger.warning(
                f"{function.__code__.co_filename}:{function.__code__.co_firstlineno}[{function.__name__}] will be abandoned"
            )

            return function(*args, **kwargs)

        return wrapped_sync
