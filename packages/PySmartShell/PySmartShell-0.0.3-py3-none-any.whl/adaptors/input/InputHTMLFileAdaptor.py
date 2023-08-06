import logging
from os import path

from .AbstractInputAdaptor import AbstractInputAdaptor


class InputHTMLFileAdaptor(AbstractInputAdaptor):

  def canHandle(input) -> bool:
    return path.isfile(input) and path.exists(input) and input.endswith('.html') 

  def getContent(self) -> list[str]:
    logging.debug(f'InputHTMLFileAdaptor activated for input: {self.inputData}')
    with open(self.inputData) as file:
      return file.readlines()