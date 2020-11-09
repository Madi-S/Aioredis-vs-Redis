import redis

from uuid import uuid4
from time import time


def ensure_conn(f):

    def inner(*args, **kwargs):

        with redis.Redis(host='localhost', port=6379) as client:
            #start = time()

            res = f(*args, client, **kwargs)

            #finish = time()
            client.flushall()
            #print(f'{f.__name__} took {finish-start} sec')

            return res

    return inner


class TestSync:
    def __init__(self, requests):
        self.requests = requests

    @ensure_conn
    def test_all(self, client):
        start = time()

        self.test_sg()
        self.test_hashes()
        self.test_lists()
        self.test_sets()
        self.test_zsets()

        end = time()

        return end-start

    @ensure_conn
    def test_sg(self, client):
        for _ in range(self.requests * 100):
            key = str(uuid4())
            val = str(uuid4())
            client.set(key, val)
            client.get(key)

    @ensure_conn
    def test_hashes(self, client):
        client.hmset(
            'secret_info', {str(uuid4()): str(uuid4()) for _ in range(5000)})

        for _ in range(self.requests * 5):
            client.hlen('secret_info')
            client.hvals('secret_info')
            keys = client.hkeys('secret_info')

            for val in keys[:500]:
                client.hexists('secret_info', str(uuid4()))
                client.hdel('secret_info', val)

    @ensure_conn
    def test_lists(self, client):
        vals = [str(uuid4()) for _ in range(2500)]

        for val in vals:
            client.lpush('my_list', val)
            client.rpush('my_list', val)

        for i in range(self.requests):
            client.lindex('my_list', i+500)
            client.lrange('my_list', i+500, 2000)
            client.lpop('my_list')
            client.lrem('my_list', 1, vals[i])

    @ensure_conn
    def test_sets(self, client):
        client.sadd('my_set', *(str(uuid4()) for _ in range(5000)))
        client.sadd('other_set', *(str(uuid4()) for _ in range(5000)))
        client.sadd('another_set', *(str(uuid4()) for _ in range(5000)))

        for _ in range(self.requests):
            client.sinter('my_set', 'other_set', 'another_set')
            client.sunion('my_set', 'other_set', 'another_set')
            client.sdiff('my_set', 'ohter_set', 'another_set')
            client.smembers('my_set')
            client.scard('other_set')
            client.srandmember('another_set')

    @ensure_conn
    def test_zsets(self, client):
        client.zadd('records', {str(uuid4()): i*i for i in range(5000)})

        for i in range(self.requests * 2):
            client.zrangebyscore('records', i, i+2000, withscores=True)
            client.zincrby('records', i*i, i*2000)
            client.zrange('records', i, i+2000, withscores=True)
            client.zcount('records', i*i, (i+2000)*(i+2000))
            client.zremrangebyrank('records', i+500, i+510)


if __name__ == '__main__':
    t = TestSync(50)
    print(t.test_all())
