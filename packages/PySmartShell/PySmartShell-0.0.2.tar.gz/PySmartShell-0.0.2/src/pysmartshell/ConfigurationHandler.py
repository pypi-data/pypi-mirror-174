from os import path

from src.adaptors.input.InputJSONFileAdaptor import InputJSONFileAdaptor
from src.adaptors.output.OutputJSONFileAdaptor import OutputJSONFileAdaptor

FILE_PATH = path.abspath(path.join(path.dirname(__file__), '../conf.json'))

class ConfigurationHandler:
  __key:str = None
  
  def __init__(self, key:str=None) -> None:
    self.__key = key

  def set(self, args:str):
    configurations = self.__getConf()

    vals = args.split('=')
    if not self.__key:
      configurations[vals[0]] = vals[1]
    else:
      if not self.__key in configurations:
        configurations[self.__key] = {}
      
      configurations[self.__key][vals[0]] = vals[1]

    OutputJSONFileAdaptor(FILE_PATH).save(configurations)

  def get(self, fieldName:str):
    configurations = self.__getConf()
    fieldNameSplitted = fieldName.split(':')
    if len(fieldNameSplitted) == 0: return configurations.get(fieldName)

    confValue = configurations.get(fieldNameSplitted[0], {})
    for key in fieldNameSplitted[1:]:
      confValue = confValue.get(key, {})

    return confValue

  def __getConf(self) -> dict:
    if not path.exists(FILE_PATH): 
      return {}

    return InputJSONFileAdaptor(FILE_PATH).getContent() or {}