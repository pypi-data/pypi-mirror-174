import pandas
import logging
from os import path

from .AbstractInputAdaptor import AbstractInputAdaptor


class InputJSONLFileAdaptor(AbstractInputAdaptor):

  def canHandle(input) -> bool:
    return path.isfile(input) and path.exists(input) and input.endswith('.jsonl')

  def getContent(self) -> list[dict]:
    logging.debug(f'InputJSONLFileAdaptor activated for input: {self.inputData}')
    return pandas.read_json(path_or_buf=self.inputData, lines=True)