import logging
from argparse import Namespace
from abc import ABC, abstractmethod

from .Argument import Argument
from .adaptors.InputAdaptorHandler import InputAdaptorHandler
from .adaptors.OutputAdaptorHandler import OutputAdaptorHandler

class AbstractAction(ABC):
  name:str
  helpInfo:str

  def getArgs(self, args:Namespace) -> dict:
    toRet = {}
    for key, value in args._get_kwargs():
      toRet[key] = value
    return toRet

  @staticmethod
  def getArgsSchema() -> list[Argument]:
    return []

  def execute(self, args:Namespace):
    dictArgs = self.getArgs(args)
    logging.debug(f'{self.name}.execute started with args', dictArgs)
    return self.executeVertical(dictArgs)

  @abstractmethod
  def executeVertical(self, args:dict):
    raise NotImplementedError

  def open(self, inputData):
    return InputAdaptorHandler.withInput(inputData).getContent()

  def saveAs(self, data, filePath:str):
    return OutputAdaptorHandler.withFile(filePath).save(data)

  
