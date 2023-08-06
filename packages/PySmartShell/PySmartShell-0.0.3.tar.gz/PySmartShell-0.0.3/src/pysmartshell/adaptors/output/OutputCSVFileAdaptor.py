import csv
import logging

from .AbstractOutputAdaptor import AbstractOutputAdaptor


class OutputCSVFileAdaptor(AbstractOutputAdaptor):

  @staticmethod
  def formatHandling() -> str:
    return 'csv'

  def save(self, data:list[dict]) -> bool:
    logging.debug(f'OutputCSVFileAdaptor activated')
    with open(self.filePath, 'w') as f:
      writer = csv.writer(f)
      for row in data:
        writer.write(row)
    
    return True