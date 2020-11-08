import argparse



class LimitValue(Exception):
    pass
    # def __init__(self, message, errors):
    #
    #     super(LimitValue, self).__init__(message)
    #     self.errors = errors


parser = argparse.ArgumentParser(
    description='Compare the speed between aioredis and redis frameworks')

parser.add_argument('-r', '--requests',
                    help='Specify the integer amount of requests from client to server to server', default=500, type=int)
parser.add_argument(
    'type', help='Type of commands to be executed:\n\nl - lists commands\nh - hashes commands\ns - sets commands\nzs - sorted sets commands\nsg - set/get commands\n\nBy default requests number will be allocated by all commands will be tested',
    default='all', choices=['l, h, s, zs, sg, all'])
parser.add_argument('tests', help='Specify the number of tests',
                    type=int, choices=[i for i in range(1, 10)])

args = parser.parse_args()

if args.requests > 2000:
    raise LimitValue('Specify requests number not more than 2000')

t = args.t
