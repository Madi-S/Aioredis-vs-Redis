import asyncio
import aioredis


async def main():
    with await aioredis.create_redis_pool('redis://localhost') as redis:
        await redis.set('foo', 'bar')
        bar = await redis.get('foo')
        print(bar)

asyncio.run(main())
