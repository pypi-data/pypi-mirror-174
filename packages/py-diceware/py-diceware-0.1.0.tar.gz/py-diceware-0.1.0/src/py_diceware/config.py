from dataclasses import dataclass

from py_diceware.wordlist import WordList


@dataclass
class PassphraseDefaults:
    number_of_words: int = 6
    min_words: int = 1
    delimiter: str = ""
    capitalisation: bool = True
    wordlist: WordList = WordList("diceware.wordlist.asc")


@dataclass
class DiceDefaults:
    sides: int = 6
    num_dice: int = 5
