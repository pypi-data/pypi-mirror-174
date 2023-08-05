from dataclasses import dataclass

from importlib_resources import files

import py_diceware.wordlists


@dataclass
class WordList:
    filename: str
    path = files(py_diceware.wordlists)
