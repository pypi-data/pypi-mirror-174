import asyncio
import json
import logging

import aioredis
import async_timeout

from adsocket.core.signals import new_broker_message
from . import Broker
from adsocket.core.message import Message

_logger = logging.getLogger(__name__)


class RedisBroker(Broker):

    _redis = None
    _db = None
    _subscribe = None
    _loop = None
    _channels = None
    _app = None
    _reading = False

    def __init__(self, host, db,  app, channels):
        self._host = host
        self._db = db
        self._loop = asyncio.get_event_loop()
        self._app = app
        self._channels = channels

    @property
    def redis(self) -> aioredis.Redis:
        if not self._redis:
            _logger.info(f"Connecting to redis {self._host} - DB: {self._db}")

            redis = aioredis.Redis.from_url(
                url=self._host,
                db=self._db,
                encoding="utf-8",
                decode_responses=True
            )
            self._redis = redis
            _logger.info("Connection to redis seems to be solid")
        return self._redis

    async def _reader(self, channel: aioredis.client.PubSub):
        if self._reading:
            raise RuntimeError("Already reading messages")
        self._reading = True
        m = f"Waiting for messages for channels: {', '.join(self._channels)}"
        _logger.info(m)
        while self._reading:
            try:
                async with async_timeout.timeout(5):
                    msg = await channel.get_message(ignore_subscribe_messages=True)
                    if msg is not None:
                        msg = Message.from_json(json.loads(msg.get('data')))
                        await self.ventilate(msg)
                        self._loop.create_task(
                            new_broker_message.send(message=msg))
                    await asyncio.sleep(0.01)
            except asyncio.TimeoutError:
                pass
            except Exception as e:
                _logger.exception(e)
        _logger.info("No longer reading message from redis")

    async def read(self):
        psub = self.redis.pubsub()
        async with psub as p:
            for channel in self._channels:
                await p.subscribe(channel)
            await self._reader(p)
            await p.reset()

    async def get_authentication_credentials(self, key):
        redis = await self.redis
        return redis.get(key)

    async def write(self, message):
        pass

    async def close(self, app):
        self._reading = False
        redis = self.redis
        await redis.close()
