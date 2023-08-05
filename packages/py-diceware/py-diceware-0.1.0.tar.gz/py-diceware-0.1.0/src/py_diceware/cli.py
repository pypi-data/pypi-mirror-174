import click

from py_diceware.config import PassphraseDefaults
from py_diceware.passphrase import Passphrase
from py_diceware.roll_dice import Dice, roll_dice

TITLE_BANNER = r"""
    _______
  /\       \                            _ _
 /()\   ()  \     _ __  _   _        __| (_) ___ _____      ____ _ _ __ ___
/    \_______\   | '_ \| | | |_____ / _` | |/ __/ _ \ \ /\ / / _` | '__/ _ \
\    /()     /   | |_) | |_| |_____| (_| | | (_|  __/\ V  V / (_| | | |  __/
 \()/   ()  /    | .__/ \__, |      \__,_|_|\___\___| \_/\_/ \__,_|_|  \___|
  \/_____()/     |_|    |___/

"""


def deactivate_prompts(ctx, param, value):
    if value:
        for p in ctx.command.params:
            if isinstance(p, click.Option) and p.prompt is not None:
                p.prompt = None
    return value


@click.command()
@click.option(
    "-w",
    "--words",
    type=click.IntRange(min=1),
    default=PassphraseDefaults.number_of_words,
    prompt="Number of words",
    help="Number of words for passphrase.",
    show_default=True,
)
@click.option(
    "-d",
    "--delimiter",
    default=PassphraseDefaults.delimiter,
    prompt=True,
    prompt_required=False,
    help="Delimiter to separate words in passphrase.",
    show_default=True,
)
@click.option(
    "--caps/--no-caps",
    default=PassphraseDefaults.capitalisation,
    help="Capitalise words in passphrase.",
    show_default=True,
)
@click.option(
    "-q",
    "--quiet",
    is_flag=True,
    is_eager=True,
    callback=deactivate_prompts,
    help="Only output the passphrase. Silence prompts and other output.",
    show_default=True,
)
def main(words, delimiter, caps, quiet):
    """Diceware passphrase generator."""
    if not quiet:
        click.echo(TITLE_BANNER)

    if not quiet:
        click.echo(f"Rolling dice {words} times...")

    dice_rolls: list[Dice] = roll_dice(words)

    if not quiet:
        for dice in dice_rolls:
            click.echo(dice)

    if not quiet:
        click.echo("\nLooking up words...")

    wordlist = PassphraseDefaults.wordlist
    passphrase = Passphrase(
        words,
        delimiter,
        caps,
        dice_rolls,
        wordlist,
    )

    if not quiet:
        for idx, word in enumerate(passphrase.words):
            click.echo(f"{dice_rolls[idx]}  {word}")

    if not quiet:
        click.echo("\nYour passphrase is:")

    click.echo(passphrase)
