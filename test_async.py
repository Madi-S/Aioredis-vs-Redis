import asyncio
import aioredis

from uuid import uuid4
from time import time


class TestAsync:
    def __init__(self, requests):
        self.requests = requests

    async def test_all(self):
        self.client = await aioredis.create_redis_pool('redis://localhost')

        await asyncio.gather(self.test_sg(), self.test_hashes(), self.test_lists(), self.test_sets(), self.test_zsets())

        await self.flushall()

        self.client.close()
        await self.client.wait_closed()

    async def test_sg(self):
        for _ in range(self.requests * 100):
            key = str(uuid4())
            val = str(uuid4())
            await self.client.set(key, val)
            await self.client.get(key)

    async def test_hashes(self):
        for _ in range(5000):
            await self.client.hmset('secret_info', str(uuid4()), str(uuid4()))

        for _ in range(self.requests * 5):
            await self.client.hlen('secret_info')
            await self.client.hvals('secret_info')
            keys = await self.client.hkeys('secret_info')

            for val in keys[:500]:
                await self.client.hexists('secret_info', str(uuid4()))
                await self.client.hdel('secret_info', val)

    async def test_lists(self):
        vals = [str(uuid4()) for _ in range(2500)]

        for val in vals:
            await self.client.lpush('my_list', val)
            await self.client.rpush('my_list', val)

        for i in range(self.requests):
            await self.client.lindex('my_list', i+500)
            await self.client.lrange('my_list', i+500, 2000)
            await self.client.lpop('my_list')
            await self.client.lrem('my_list', 1, vals[i])

    async def test_sets(self):
        await self.client.sadd('my_set', *(str(uuid4()) for _ in range(5000)))
        await self.client.sadd('other_set', *(str(uuid4()) for _ in range(5000)))
        await self.client.sadd('another_set', *(str(uuid4()) for _ in range(5000)))

        for _ in range(self.requests):
            await self.client.sinter('my_set', 'other_set', 'another_set')
            await self.client.sunion('my_set', 'other_set', 'another_set')
            await self.client.sdiff('my_set', 'ohter_set', 'another_set')
            await self.client.smembers('my_set')
            await self.client.scard('other_set')
            await self.client.srandmember('another_set')

    async def test_zsets(self):
        for i in range(5000):
            await self.client.zadd('records', i*i, str(uuid4()))

        for i in range(self.requests * 2):
            await self.client.zrangebyscore('records', i, i+2000, withscores=True)
            await self.client.zincrby('records', i*i, i*2000)
            await self.client.zrange('records', i, i+2000, withscores=True)
            await self.client.zcount('records', i*i, (i+2000)*(i+2000))
            await self.client.zremrangebyrank('records', i+500, i+510)

    async def flushall(self):
        await self.client.flushall()


if __name__ == '__main__':
    t = TestAsync(2000)
    start = time()
    asyncio.run(t.test_all())
    finish = time()

    print(finish-start)

# *** in seconds ***
# 500 req:
# 37.1 and 55.5
# 62.9 and 66.6
# 68.3 and 73.9
# 58.8 and 64.2

# 1 req:
# 6.1 and 5.6
# 5.2 and 7.2
# 6.3 and 7.2
# 6.0 and 6.9


# 2000 req:
# 189.7 and 206.6
# 218.3 and 236.4 