import asyncio

import aiohttp.web_request
from aiohttp import web

from adsocket.core.utils import get_task_by_name


async def ping_handler(request: aiohttp.web_request.Request, **kwargs):
    """
    Alive test
    :param request:
    :type request:
    :param kwargs:
    :type kwargs:
    :return:
    :rtype:
    """

    broker_task_name = request.app['settings'].BROKER.get('broker_task_name')
    broker_task = get_task_by_name(broker_task_name)
    if not broker_task or broker_task.cancelled():
        return web.Response(
            status=503, text='message broker background task not available')
    return web.Response(text='pong')
