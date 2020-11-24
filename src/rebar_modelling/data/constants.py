"""List of possible rebars."""
# from typing import Final
import sys

if sys.version_info[:2] == (3, 7):
    # Running on 3.7 Python; use typing_extensions package
    from typing_extensions import Final
else:
    from typing import Final


class Constants:
    """Constants that will be used for reinforcement calculations."""

    LENGTH_OF_REBARS: Final = [
        950,
        1050,
        1150,
        1300,
        1450,
        1650,
        1950,
        2300,
        2900,
        3900,
        4850,
        5850,
        6850,
        7800,
        8800,
        11700,
    ]
