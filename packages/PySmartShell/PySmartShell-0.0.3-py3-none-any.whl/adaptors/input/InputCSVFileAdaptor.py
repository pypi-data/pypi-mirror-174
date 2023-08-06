import pandas
import logging
from os import path

from .AbstractInputAdaptor import AbstractInputAdaptor


class InputCSVFileAdaptor(AbstractInputAdaptor):

  def canHandle(input) -> bool:
    return path.isfile(input) and path.exists(input) and input.endswith('.csv')

  def getContent(self) -> list[str]:
    logging.debug(f'InputCSVFileAdaptor activated for input: {self.inputData}')
    return pandas.read_csv(self.inputData)