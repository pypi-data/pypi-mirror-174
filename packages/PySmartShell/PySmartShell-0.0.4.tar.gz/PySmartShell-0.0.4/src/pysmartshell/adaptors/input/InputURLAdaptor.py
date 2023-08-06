import logging
import requests
import validators

from .AbstractInputAdaptor import AbstractInputAdaptor


class InputURLAdaptor(AbstractInputAdaptor):

  def canHandle(input) -> bool:
    return validators.url(input)

  def getContent(self) -> list[str]:
    logging.debug(f'InputURLAdaptor activated for input: {self.inputData}')
    url = requests.get(self.inputData)
    return url.text