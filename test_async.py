import asyncio
import aioredis

from uuid import uuid4
from time import time


class TestAsync:
    def __init__(self, requests):
        self.requests = requests

    async def test_all(self):
        await asyncio.gather(self.test_sg(), self.test_hashes(), self.test_lists(), self.test_sets(), self.test_zsets())

    async def get_redis(self):
        redis = await aioredis.create_redis_pool('redis://localhost')
        return redis

    async def close_redis(self, redis):
        redis.close()
        await redis.wait_closed()

    async def test_sg(self):
        redis = await self.get_redis()
        for _ in range(self.requests * 100):
            key = str(uuid4())
            val = str(uuid4())
            await redis.set(key, val)
            await redis.get(key)

        await self.close_redis(redis)

    async def test_hashes(self):
        redis = await self.get_redis()

        for _ in range(5000):
            await redis.hmset('secret_info', str(uuid4()), str(uuid4()))

        for _ in range(self.requests * 5):
            await redis.hlen('secret_info')
            await redis.hvals('secret_info')
            keys = await redis.hkeys('secret_info')

            for val in keys[:500]:
                await redis.hexists('secret_info', str(uuid4()))
                await redis.hdel('secret_info', val)

        await self.close_redis(redis)

    async def test_lists(self):
        redis = await self.get_redis()

        vals = [str(uuid4()) for _ in range(2500)]

        for val in vals:
            await redis.lpush('my_list', val)
            await redis.rpush('my_list', val)

        for i in range(self.requests):
            await redis.lindex('my_list', i+500)
            await redis.lrange('my_list', i+500, 2000)
            await redis.lpop('my_list')
            await redis.lrem('my_list', 1, vals[i])

        await self.close_redis(redis)

    async def test_sets(self):
        redis = await self.get_redis()

        await redis.sadd('my_set', *(str(uuid4()) for _ in range(5000)))
        await redis.sadd('other_set', *(str(uuid4()) for _ in range(5000)))
        await redis.sadd('another_set', *(str(uuid4()) for _ in range(5000)))

        for _ in range(self.requests):
            await redis.sinter('my_set', 'other_set', 'another_set')
            await redis.sunion('my_set', 'other_set', 'another_set')
            await redis.sdiff('my_set', 'ohter_set', 'another_set')
            await redis.smembers('my_set')
            await redis.scard('other_set')
            await redis.srandmember('another_set')

        await self.close_redis(redis)

    async def test_zsets(self):
        redis = await self.get_redis()

        for i in range(5000):
            await redis.zadd('records', i*i, str(uuid4()))

        for i in range(self.requests * 2):
            await redis.zrangebyscore('records', i, i+2000, withscores=True)
            await redis.zincrby('records', i*i, i*2000)
            await redis.zrange('records', i, i+2000, withscores=True)
            await redis.zcount('records', i*i, (i+2000)*(i+2000))
            await redis.zremrangebyrank('records', i+500, i+510)

        await self.close_redis(redis)

    async def flushall(self):
        redis = await self.get_redis()
        await redis.flushall()
        await self.close_redis(redis)


if __name__ == '__main__':
    t = TestAsync(50)
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
