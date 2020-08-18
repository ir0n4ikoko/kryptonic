"""
Module entrypoint. Ran with `python -m kryptonic
"""

from argparse import ArgumentParser
from . import main
import sys

base_executable = sys._base_executable.split('/')[-1:][0] if sys._base_executable else 'python'

parser = ArgumentParser(prog=f'{base_executable} -m kryptonic', description="Run UI tests")

parser.add_argument('-F', '--config-file', type=str, default=None, help='Name of json file containing configuration as key/value pairs')

group = parser.add_mutually_exclusive_group()
group.add_argument('-J', '--config-json', type=str, default=None, help='Inline json of arguments, overrides --config-file; can\'t be used '
                                                                        'with --config-args e.g. \'{"foo": "bar", "baz": "quix"')
group.add_argument('-C', '--config-args', type=str, default=None, help='Comma-delimited list of config arguments to override; can\'t be used with --config-json, e.g. foo=bar,baz=quix')

parser.add_argument('-p', '--pattern', type=str, help='Pattern to match tests', default='test*.py')
parser.add_argument('-s', '--start-directory', type=str, help='Directory to start discovery', default='.')

args = parser.parse_args()


print('args ', args )
main(pattern=args.pattern,
     start_directory=args.start_directory,
     config_file=args.config_file,
     config_json=args.config_json,
     config_args=args.config_args,)