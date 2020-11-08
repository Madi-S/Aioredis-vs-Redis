import argparse
import asyncio

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


def main():

    a = TestAsync(reqs)
    s = TestSync(reqs)

    def test_all_():
        s1 = time()
        a.test_all()
        f1 = time()
        s2 = time() 
        asyncio.run(s.test_all())
        f2 = time()

        return 

    def test_sg_():
        a.test_sg()
        asyncio.run(s.test_sg())


    def test_lists_():
        a.test_lists()
        asyncio.run(s.test_lists())


    def test_hashes_():
        a.test_hashes()
        asyncio.run(s.test_hashes())


    def test_sets_():
        a.test_sets()
        asyncio.run(s.test_sets())


    def test_zsets_():
        a.test_zsets()
        asyncio.run(s.test_zsets())


    if type_ == 'all':
        func = test_all_

    elif type_ == 'sg':
        func = test_sg_

    elif type_ == 'l':
        func = test_lists_

    elif type_ == 'h':
        func = test_hashes_

    elif type_ == 's':
        func = test_sets_

    elif type_ == 'zs':
        func = test_zsets_

    for _ in range(tests):
        t1, t2 = func()
        avg = 



if reqs > 2000:
    raise RequestsLimit('Specify requests number not more than 2000')
else:
    main()
    

    
