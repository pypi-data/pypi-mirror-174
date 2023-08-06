import logging
from argparse import Namespace

from .Argument import Argument
from .AbstractAction import AbstractAction
from .ConfigurationHandler import ConfigurationHandler


class AbstractActionWithConfiguration(AbstractAction):
  confHandler:ConfigurationHandler

  def __init__(self):
    super().__init__()
    self.confHandler = ConfigurationHandler(self.name)

  @staticmethod
  def getArgsSchema() -> list[Argument]:
    return [
      Argument.create(longCommand='--set-conf'),
      Argument.create(longCommand='--get-conf'),
    ]

  def execute(self, args:Namespace):
    logging.debug(f'{self.name}.execute started with args', self.getArgs(args))

    dictArgs = self.getArgs(args)
    if dictArgs.get('get_conf'):
      return self.getConfiguration(dictArgs.get('get_conf'))

    if dictArgs.get('set_conf'):
      return self.confHandler.set(dictArgs.get('set_conf'))
    
    return self.executeVertical(dictArgs)

  def getConfiguration(self, key:str):
    confValue = self.confHandler.get(f'{self.name}:{key}')
    if confValue: return confValue
    raise Exception(f'Missing required configuration for key {key}') 
