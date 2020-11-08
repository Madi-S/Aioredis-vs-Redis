import argparse
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

if reqs > 2000:
    raise RequestsLimit('Specify requests number not more than 2000')


else:
    a = TestAsync(reqs)
    s = TestSync(reqs)

    if type_ == 'all':
        a.test_all()
        s.test_all()

    elif type_ == 'l':
        a.test_lists()
        s.test_lists()

    elif type_ == 'h':
        a.test_hashes()
        s.test_hashes()

    elif type_ == 's':
        a.test_sets()
        s.test_sets()

    elif type_ == 'zs':
        a.test_zsets()
        s.test_zsets()

    elif type_ == 'sg':
        a.test_sg()
        s.test_sg()

