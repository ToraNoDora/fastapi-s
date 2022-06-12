from typing import Optional
import json

from aioredis import Redis, from_url
from src.config.config import REDIS_DB_URL



class RedisCache:

    def __init__(self):
        self.redis_url = REDIS_DB_URL
        self.redis_cache: Optional[Redis] = from_url(self.redis_url, decode_responses=True)


    async def __aenter__(self):
        return self


    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        await self._close()
        return self


    async def _keys(self, pattern):
        return await self.redis_cache.keys(pattern)


    async def get_all_keys(self):
        return await self.redis_cache.keys("*")


    async def set(self, key, value):
        e = value.to_dict()
        val = await self._dict_to_binary(e)

        return await self.redis_cache.set(key, val)


    async def set_multi(self, key, value):
        val = [i.to_dict() for i in value]
        bin = await self._dict_to_binary(val)

        return await self.redis_cache.set(key, bin)


    async def get(self, key):
        value = await self.redis_cache.get(key)
        value = await self._binary_to_dict(value)

        return value


    async def delete(self, key):
        return await self.redis_cache.delete(key)


    async def delete_all_keys(self):
        return await self.redis_cache.delete("*")


    async def _dict_to_binary(self, the_dict):
        str = json.dumps(the_dict)
        binary = ' '.join(format(ord(letter), 'b') for letter in str)

        return binary


    async def _binary_to_dict(self, the_binary):
        jsn = ''.join(chr(int(x, 2)) for x in the_binary.split())
        dict_value = json.loads(jsn)

        return dict_value


    async def _close(self):
        await self.redis_cache.close()


