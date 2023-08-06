import asyncio
import json
import logging

import redis.asyncio as redis

from asyncredisrpc import REDIS_PREFIX, Error


class AsyncServer:
    def __init__(self, queue, host='localhost', port=6379):
        self.url = f'redis://{host}:{port}'
        self.redis = None
        self.queue = REDIS_PREFIX + queue
        self.tasks = {}

    def run(self):
        asyncio.run(self.async_run())

    async def async_run(self):
        if 'on_server_start' in self.tasks:
            await self.tasks['on_server_start']()
        self.redis = await redis.from_url(self.url)
        while True:
            _, elem = await self.redis.blpop(self.queue)
            req = json.loads(elem.decode())
            name = req['name']
            req_id = req['id']
            if name not in self.tasks:
                logging.error(f'received a unknown call: {name}')
                await self.response(req_id, Error.UNKNOWN_REMOTE_CALL.value, None)
                continue
            func = self.tasks[name]
            args = req['args']
            kwargs = req['kwargs']
            result = await func(*args, **kwargs)
            await self.response(req_id, Error.OK.value, result)

    async def response(self, req_id, error, result):
        data = {'error': error, 'result': result}
        await self.redis.rpush(f"{self.queue}:{req_id}", json.dumps(data))

    def task(self, func):
        self.tasks[func.__name__] = func

    def on_server_start(self, func):
        self.tasks['on_server_start'] = func
