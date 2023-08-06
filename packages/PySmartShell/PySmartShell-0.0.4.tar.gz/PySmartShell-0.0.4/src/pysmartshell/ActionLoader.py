import sys
import logging
import pkgutil

from .AbstractAction import AbstractAction

class ActionLoader:

  @staticmethod
  def loadFrom(directoryPath:str) -> list[AbstractAction]:
    sys.path.append(directoryPath)

    packages = []
    for package in pkgutil.iter_modules([directoryPath]):
      if not package.ispkg: continue

      packages.append( 
        getattr(
          getattr(
            __import__( package.name, fromlist = [package.name]),
            package.name
          ),
          package.name
        )()
      )
      logging.debug(f'loaded action {package.name}')

    sys.path.pop()
    return packages
