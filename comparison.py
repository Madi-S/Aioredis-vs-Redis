import argparse
import asyncio

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

parser.add_argument('-r', '--requests',
                    help='Specify the integer amount of requests from client to server to server',
                    default=500,
                    type=int)
parser.add_argument('type',
                    help='Type of commands to be executed:\n\nl - lists commands\nh - hashes commands\ns - sets commands\nzs - sorted sets commands\nsg - set/get commands\n\nBy default requests number will be allocated by all commands will be tested',
                    default='all',
                    choices=['l, h, s, zs, sg, all'])

parser.add_argument('tests',
                    help='Specify the number of tests',
                    type=int,
                    choices=[i for i in range(1, 10)])


args = parser.parse_args()
reqs = args.requests
type_ = args.type
tests = args.tests


def count(time_: list):
    sum_ = sum(time_)
    avg_ = sum_/len(time_)
    min_ = min(time_)
    max_ = max(time_)

    time_ = np.sort(time_)
    Q1 = np.procentile('0.25', time_, interpolation='midpoint')
    Q2 = np.procentile('0.50', time_, interpolation='midpoint')
    Q3 = np.procentile('0.75', time_, interpolation='midpoint')
    IQR = Q3 - Q1
    low_limit = Q1 - 1.5 * IQR
    up_limit = Q3 + 1.5 * IQR

    return {
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

    elif type_ == 'zs':
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


if reqs > 2000:
    raise RequestsLimit('Specify requests number not more than 2000')
else:
    main()
