import json
import logging

from .AbstractOutputAdaptor import AbstractOutputAdaptor


class OutputJSONLFileAdaptor(AbstractOutputAdaptor):

  @staticmethod
  def formatHandling() -> str:
    return 'jsonl'

  def save(self, data:list[dict]) -> bool:
    logging.debug(f'OutputJSONLFileAdaptor activated')
    with open(self.filePath, 'w') as f:
      for item in data:
        f.write(json.dumps(item) + '\n')

    return True