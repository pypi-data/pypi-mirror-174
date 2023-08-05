from py_diceware.roll_dice import Dice
from py_diceware.wordlist import WordList


class Passphrase:
    def __init__(
        self,
        number_of_words: int,
        delimiter: str,
        capitalisation: bool,
        dice_rolls: list[Dice],
        wordlist: WordList,
    ) -> None:
        self.number_of_words: int = number_of_words
        self.delimiter: str = delimiter
        self.capitalisation: bool = capitalisation
        self.dice_rolls = dice_rolls
        self.wordlist: WordList = wordlist
        self.words: list[str] = [self.lookup_word(dice) for dice in dice_rolls]
        self.passphrase = self.generate_passphrase()

    def lookup_word(self, dice) -> str:
        wordlist = self.wordlist.path / self.wordlist.filename
        word = None
        with open(wordlist, "r") as f:
            for line in f:
                if line.startswith(str(dice)):
                    _, word = line.split()

        if word is None:
            raise (LookupError(f"{dice} not found in word list"))
        else:
            return word

    def generate_passphrase(self) -> str:
        words = self.words
        if self.capitalisation:
            words = [word.capitalize() for word in words]

        return self.delimiter.join(words)

    def __repr__(self) -> str:
        return self.passphrase
