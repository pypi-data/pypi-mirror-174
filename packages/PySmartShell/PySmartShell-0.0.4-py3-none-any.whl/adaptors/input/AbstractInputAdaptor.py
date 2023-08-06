from abc import abstractstaticmethod


class AbstractInputAdaptor:
  inputData = None

  def __init__(self, inputData):
    self.inputData = inputData

  @abstractstaticmethod
  def canHandle(input) -> bool:
    raise NotImplementedError

  @abstractstaticmethod
  def getContent(self) -> list[str]:
    raise NotImplementedError