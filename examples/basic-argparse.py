from argparse import ArgumentParser

parser = ArgumentParser()

subparsers1 = parser.add_subparsers(dest = 'subcommand')

command1parser = subparsers1.add_parser('command1')

command1parser.add_argument("arg1")

def command1_handler(args):
    return int(args.arg1) / 2

command1parser.set_defaults(func = command1_handler)

command2parser = subparsers1.add_parser('command2')

command2parser.add_argument("arg1")

def command2_handler(args):
    return int(args.arg1) * 2

command2parser.set_defaults(func = command2_handler)

args = parser.parse_args()

print(args.func(args))
