import argparse

import asyncio
import aioredis
import redis

import math
import numpy as np

from time import time

from test_async import TestAsync
from test_sync import TestSync


class RequestsLimit(Exception):
    pass
    # def __init__(self, message, errors):
    #
    #     super(LimitValue, self).__init__(message)
    #     self.errors = errors


parser = argparse.ArgumentParser(
    description='Compare the speed between aioredis and redis frameworks')

parser.add_argument('type',
                    help='Type of commands to be executed:\n\nl - lists commands\nh - hashes commands\ns - sets commands\nzs - sorted sets commands\nsg - set/get commands\n\nBy default requests number will be allocated by all commands will be tested',
                    default='all',
                    choices=['l', 'h', 's', 'zs', 'sg', 'all'])

parser.add_argument('tests',
                    help='Specify the number of tests',
                    type=int,
                    choices=[i for i in range(1, 11)])

parser.add_argument('-r', '--requests',
                    help='Specify the integer amount of requests from client to server to server',
                    default=500,
                    type=int)


args = parser.parse_args()
reqs = args.requests
type_ = args.type
tests = args.tests


def count(time_: list):
    len_ = len(time_)
    sum_ = round(sum(time_), 5)
    min_ = round(min(time_), 5)
    max_ = round(max(time_), 5)
    avg_ = round(sum_/len_, 5)

    time_ = np.sort(time_)
    Q1 = round(np.percentile(time_, 25), 5)
    Q2 = round(np.percentile(time_, 50), 5)
    Q3 = round(np.percentile(time_, 75), 5)
    IQR = round(Q3 - Q1, 5)
    low_limit = round(Q1 - 1.5 * IQR, 5)
    up_limit = round(Q3 + 1.5 * IQR, 5)

    return {
        'len': len_,
        'sum': sum_,
        'avg': avg_,
        'min': min_,
        'max': max_,
        'Q1': Q1,
        'Q2': Q2,
        'Q3': Q3,
        'IQR': IQR,
        'low_limit': low_limit,
        'up_limit': up_limit,
    }


def print_stats(stats, package):
    print(f'''
    Tests taken {stats["len"]}
    Statistics for {package.__name__}
    ---     Overall time taken {stats["sum"]}
    ---     Average time taken {stats["avg"]}
    ---     Minimum time taken {stats["min"]}
    ---     Maximum time taken {stats["max"]}
    ---     First quartile {stats["Q1"]}
    ---     Second quartile {stats["Q2"]}
    ---     Third quartile {stats["Q3"]}
    ---     Interquartile range {stats["IQR"]}
    ---     Low limit {stats["low_limit"]}
    ---     Up limit {stats["up_limit"]}
    ''')


def main():

    a = TestAsync(reqs)
    s = TestSync(reqs)

    def test_all_a():
        asyncio.run(a.test_all())

    def test_sg_a():
        asyncio.run(a.test_sg())

    def test_lists_a():
        asyncio.run(a.test_lists())

    def test_hashes_a():
        asyncio.run(a.test_hashes())

    def test_sets_a():
        asyncio.run(a.test_sets())

    def test_zsets_a():
        asyncio.run(a.test_zsets())

    def test_all_s():
        s.test_all()

    def test_sg_s():
        s.test_sg()

    def test_lists_s():
        s.test_lists()

    def test_hashes_s():
        s.test_hashes()

    def test_sets_s():
        s.test_sets()

    def test_zsets_s():
        s.test_zsets()

    if type_ == 'all':
        test_a = test_all_a
        test_s = test_all_s

    elif type_ == 'sg':
        test_a = test_sg_a
        test_s = test_sg_s

    elif type_ == 'l':
        test_a = test_lists_a
        test_s = test_lists_s

    elif type_ == 'h':
        test_a = test_hashes_a
        test_s = test_hashes_s

    elif type_ == 's':
        test_a = test_sets_a
        test_s = test_sets_s

    else:
        test_a = test_zsets_a
        test_s = test_zsets_s

    time_a = []
    time_s = []

    for _ in range(tests):
        start = time()
        test_a()
        finish = time()
        time_a.append(finish-start)

        start = time()
        test_s()
        finish = time()
        time_s.append(finish-start)

    print(f'Test finished\n\nCounting results for {reqs} requests {tests} times\n\n{time_a}\n{time_s}')

    data_a = count(time_a)
    data_s = count(time_s)

    print_stats(data_a, aioredis)
    print_stats(data_s, redis)


if __name__ == '__main__':

    if reqs > 2000:
        raise RequestsLimit('Specify requests number not more than 2000')
    else:
        main()
