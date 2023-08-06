import json
import logging
from os import path

from .AbstractInputAdaptor import AbstractInputAdaptor


class InputJSONFileAdaptor(AbstractInputAdaptor):

  def canHandle(input) -> bool:
    return path.isfile(input) and path.exists(input) and input.endswith('.json')

  def getContent(self) -> dict:
    logging.debug(f'InputJSONFileAdaptor activated for input: {self.inputData}')
    
    if path.getsize(self.inputData) == 0: 
      return {}

    with open(self.inputData, 'r') as f:
      return json.load(f)