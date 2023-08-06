import os

from .output.OutputCSVFileAdaptor import OutputCSVFileAdaptor
from .output.OutputHTMLFileAdaptor import OutputHTMLFileAdaptor
from .output.OutputTextFileAdaptor import OutputTextFileAdaptor
from .output.AbstractOutputAdaptor import AbstractOutputAdaptor
from .output.OutputJSONFileAdaptor import OutputJSONFileAdaptor
from .output.OutputJSONLFileAdaptor import OutputJSONLFileAdaptor

ADAPTORS = {
  OutputCSVFileAdaptor.formatHandling(): OutputCSVFileAdaptor,
  OutputJSONFileAdaptor.formatHandling(): OutputJSONFileAdaptor,
  OutputHTMLFileAdaptor.formatHandling(): OutputHTMLFileAdaptor,
  OutputTextFileAdaptor.formatHandling(): OutputTextFileAdaptor,
  OutputJSONLFileAdaptor.formatHandling(): OutputJSONLFileAdaptor,
}

class OutputAdaptorHandler:
  
  @staticmethod
  def withFile(filePath:str) -> AbstractOutputAdaptor:
    _, fileFormat = os.path.splitext(filePath)
    fileFormat = fileFormat.replace('.', '')
    if fileFormat not in ADAPTORS:
      raise Exception(f'no output handler for format {fileFormat}')

    destinationFolder = os.path.abspath( os.path.dirname(filePath))
    if not os.path.exists(destinationFolder):
      os.mkdir( destinationFolder )
      
    return ADAPTORS.get(fileFormat)(filePath)