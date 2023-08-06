import logging

from .AbstractOutputAdaptor import AbstractOutputAdaptor


class OutputHTMLFileAdaptor(AbstractOutputAdaptor):

  @staticmethod
  def formatHandling() -> str:
    return 'html'

  def save(self, data:str) -> bool:
    logging.debug(f'OutputHTMLFileAdaptor activated')
    with open(self.filePath, 'w') as f:
      f.write(data)
    
    return True