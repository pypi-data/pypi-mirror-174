import json
import logging

from .AbstractOutputAdaptor import AbstractOutputAdaptor


class OutputJSONFileAdaptor(AbstractOutputAdaptor):

  @staticmethod
  def formatHandling() -> str:
    return 'json'

  def save(self, data:dict) -> bool:
    logging.debug(f'OutputJSONFileAdaptor activated')
    with open(self.filePath, 'w') as f:
      json.dump(data, f)

    return True