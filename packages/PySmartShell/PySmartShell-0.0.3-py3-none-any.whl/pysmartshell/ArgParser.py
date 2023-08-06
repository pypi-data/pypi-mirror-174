import os
import argparse

from .AbstractAction import AbstractAction

class ArgParser:
  parser = None

  def __init__(self, actions:list[AbstractAction]):
    self.parser = argparse.ArgumentParser(os.path.basename(__file__), description='AI processor')

    self.parser.add_argument(
      '--log-level',
      default = 'INFO', 
      choices = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
    )

    self.parser.add_argument('--set-conf')
    self.parser.add_argument('--get-conf')

    sub_parsers = self.parser.add_subparsers(dest='action')
    for action in actions:
      subcommand = sub_parsers.add_parser(action.name, help=action.helpInfo)
      for arg in action.getArgsSchema():
        if arg.shortCommand:
          subcommand.add_argument(arg.shortCommand, arg.longCommand, type=arg.type, help=arg.helpInfo)
        else:
          subcommand.add_argument(arg.longCommand, type=arg.type, help=arg.helpInfo)

  def getParser(self, args):
    return self.parser.parse_args()