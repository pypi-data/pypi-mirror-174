import os
import sys
import logging
from os.path import join

from .ArgParser import ArgParser 
from .ActionLoader import ActionLoader
from .AbstractAction import AbstractAction
from .ConfigurationHandler import ConfigurationHandler

def ActionsLoader(unparsed_args):
  try:
    folderPath = join(os.getcwd(), ConfigurationHandler().get('actionsPath'))
  except:
    folderPath = join(os.getcwd(), 'actions')

  actions:list[AbstractAction] = ActionLoader.loadFrom(folderPath)
  args = ArgParser(actions).getParser(unparsed_args)

  __LOG_FILEPATH__  = join(os.getcwd(), 'logs/')
  os.makedirs(__LOG_FILEPATH__, exist_ok=True)

  logging.basicConfig(
    level = args.log_level,
    format = '%(asctime)s [%(levelname)s] %(name)s - %(message)s',
    handlers = [
      logging.FileHandler(join(__LOG_FILEPATH__, 'logger.log')),
      logging.StreamHandler()
    ],
    encoding='utf-8',
  )

  if args.log_level == 'INFO':
    sys.tracebacklimit = 0

  if args.action:
    availableActions = {}
    for action in actions:
      availableActions[action.name] = action
    return availableActions.get(args.action).execute(args)

  if args.set_conf:
    ConfigurationHandler().set(args.set_conf)
    logging.info('Requested configuration change done!')
    return

  if args.get_conf:
    confValue = ConfigurationHandler().get(args.get_conf)
    if confValue:
      logging.info('Requested configuration value is:', confValue, '.')
    else:
      logging.info('Requested key is not setted in configuration.')
    return
  
if __name__ == '__main__':
  loadActions( sys.argv[1:] )