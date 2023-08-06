import logging

from .AbstractOutputAdaptor import AbstractOutputAdaptor


class OutputTextFileAdaptor(AbstractOutputAdaptor):

  @staticmethod
  def formatHandling() -> str:
    return 'txt'

  def save(self, data:list[dict]) -> bool:
    logging.debug(f'OutputTextFileAdaptor activated')
    with open(self.filePath, 'w') as f:
      f.writelines(data)
    
    return True