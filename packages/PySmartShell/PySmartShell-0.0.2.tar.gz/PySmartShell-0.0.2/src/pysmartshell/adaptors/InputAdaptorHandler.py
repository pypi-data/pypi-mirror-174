from .input.AbstractInputAdaptor import AbstractInputAdaptor

from .input.InputURLAdaptor import InputURLAdaptor
from .input.InputCSVFileAdaptor import InputCSVFileAdaptor
from .input.InputTextFileAdaptor import InputTextFileAdaptor
from .input.InputJSONFileAdaptor import InputJSONFileAdaptor
from .input.InputHTMLFileAdaptor import InputHTMLFileAdaptor
from .input.InputJSONLFileAdaptor import InputJSONLFileAdaptor


ADAPTORS:list[AbstractInputAdaptor] = [
  InputURLAdaptor,
  InputCSVFileAdaptor,
  InputTextFileAdaptor,
  InputJSONFileAdaptor,
  InputHTMLFileAdaptor,
  InputJSONLFileAdaptor,
]

class InputAdaptorHandler:

  @staticmethod
  def withInput(inputData) -> AbstractInputAdaptor:
    for adaptor in ADAPTORS:
      if not adaptor.canHandle(inputData.strip()): continue
      return adaptor(inputData=inputData)

    raise Exception(f'no input handler for input {inputData}')