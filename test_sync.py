import redis

from uuid import uuid4
from time import time


# def timeit(f):
#
#     def timed(*args, **kwargs):
#
#         start = time()
#         result = f(*args, **kwargs)
#         finish = time()
#
#         print(f'{f.__name__} took {finish-start} sec')
#         return result
#
#     return timed


class TestSync:
    def __init__(self, requests):
        self.requests = requests

    def test_all(self):
        start = time()

        self.client = redis.Redis(host='localhost', port=6379)

        self.test_sg()
        self.test_hashes()
        self.test_lists()
        self.test_sets()
        self.test_zsets()
        self.flushall()

        self.client.close()

        end = time()

        return end-start

    @timeit
    def test_sg(self):
        for _ in range(self.requests * 100):
            key = str(uuid4())
            val = str(uuid4())
            self.client.set(key, val)
            self.client.get(key)

    @timeit
    def test_hashes(self):
        self.client.hmset(
            'secret_info', {str(uuid4()): str(uuid4()) for _ in range(5000)})

        for _ in range(self.requests * 5):
            self.client.hlen('secret_info')
            self.client.hvals('secret_info')
            keys = self.client.hkeys('secret_info')

            for val in keys[:500]:
                self.client.hexists('secret_info', str(uuid4()))
                self.client.hdel('secret_info', val)

    @timeit
    def test_lists(self):
        vals = [str(uuid4()) for _ in range(2500)]

        for val in vals:
            self.client.lpush('my_list', val)
            self.client.rpush('my_list', val)

        for i in range(self.requests):
            self.client.lindex('my_list', i+500)
            self.client.lrange('my_list', i+500, 2000)
            self.client.lpop('my_list')
            self.client.lrem('my_list', 1, vals[i])

    @timeit
    def test_sets(self):
        self.client.sadd('my_set', *(str(uuid4()) for _ in range(5000)))
        self.client.sadd('other_set', *(str(uuid4()) for _ in range(5000)))
        self.client.sadd('another_set', *(str(uuid4()) for _ in range(5000)))

        for _ in range(self.requests):
            self.client.sinter('my_set', 'other_set', 'another_set')
            self.client.sunion('my_set', 'other_set', 'another_set')
            self.client.sdiff('my_set', 'ohter_set', 'another_set')
            self.client.smembers('my_set')
            self.client.scard('other_set')
            self.client.srandmember('another_set')

    @timeit
    def test_zsets(self):
        self.client.zadd('records', {str(uuid4()): i*i for i in range(5000)})

        for i in range(self.requests * 2):
            self.client.zrangebyscore('records', i, i+2000, withscores=True)
            self.client.zincrby('records', i*i, i*2000)
            self.client.zrange('records', i, i+2000, withscores=True)
            self.client.zcount('records', i*i, (i+2000)*(i+2000))
            self.client.zremrangebyrank('records', i+500, i+510)

    def flushall(self):
        self.client.flushall()


if __name__ == '__main__':
    t = TestSync(2000)
    print(t.test_all())
