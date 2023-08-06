from abc import ABC


class Argument(ABC):
  __type:int|float|str
  __longCommand:str
  __shortCommand:str
  __helpInfo:str
  __isRequired:bool

  def __init__(self, longCommand, shortCommand, type, helpInfo, isRequired) -> None:
    super().__init__()
    self.__type = type
    self.__helpInfo = helpInfo
    self.__isRequired = isRequired
    self.__longCommand = longCommand
    self.__shortCommand = shortCommand

  @property
  def type(self) -> int|float|str:
    return self.__type

  @property
  def shortCommand(self) -> str:
    return self.__shortCommand

  @property
  def longCommand(self) -> str:
    return self.__longCommand

  @property
  def helpInfo(self) -> str:
    return self.__helpInfo

  @property
  def isRequired(self) -> bool:
    return self.__isRequired

  @staticmethod
  def create(longCommand:str, shortCommand:str='', type:int|float|str=str, helpInfo:str='', isRequired:bool=True):
    return Argument(
      type = type, 
      helpInfo = helpInfo, 
      isRequired = isRequired,
      longCommand = longCommand,
      shortCommand = shortCommand,
    )
