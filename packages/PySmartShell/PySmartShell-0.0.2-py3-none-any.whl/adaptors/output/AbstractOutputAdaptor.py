from abc import abstractstaticmethod


class AbstractOutputAdaptor:
  filePath = None

  def __init__(self, filePath):
    self.filePath = filePath

  @abstractstaticmethod
  def formatHandling() -> str:
    raise NotImplementedError

  @abstractstaticmethod
  def save(self, data:list[dict]) -> bool:
    raise NotImplementedError