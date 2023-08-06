import logging
import copy
from abc import ABC, abstractmethod
import asyncio

from adsocket.core.utils import import_module
from adsocket.core.message import Message
from adsocket.core.exceptions import InvalidChannelException, ChannelNotFoundException

_logger = logging.getLogger(__name__)


class Broker(ABC):

    _app = None

    async def ventilate(self, message: Message):
        try:
            await self._app['channels'].publish(message)
        except InvalidChannelException as e:
            msg = f"Received invalid channel type from Broker: " \
                  f"{message.channel}"
            _logger.error(msg)
        except ChannelNotFoundException:
            pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self, msg: Message):
        pass

    @abstractmethod
    async def close(self, app):
        pass


async def load_broker(app):

    params = copy.deepcopy(app['settings'].BROKER)
    task_name = params.pop('broker_task_name', 'broker')
    driver = params.pop('driver')
    broker_class = import_module(driver)
    params['app'] = app
    broker = broker_class(**params)
    app['broker'] = broker
    task = asyncio.create_task(app['broker'].read(), name=task_name)
    task.add_done_callback(_handle_broker_task)
    _logger.info(f"Broker task name: {task.get_name()}")
    return task


def _handle_broker_task(task: asyncio.Task) -> None:
    """
    Manage broker asyncio task to prevent program running
    when the task is not running
    """
    try:
        task.result()
    except asyncio.CancelledError:
        # Expected
        _logger.debug("Broker task cancelled")
        pass
    except Exception as e:
        msg = f'Exception by {task.get_name()}: '
        _logger.exception(msg)
        raise e
