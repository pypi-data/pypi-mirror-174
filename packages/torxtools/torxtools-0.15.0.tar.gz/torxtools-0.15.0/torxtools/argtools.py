"""
Parser types for command-line options, arguments and sub-commands

"""

from argparse import ArgumentTypeError

__all__ = [
    "is_int_positive",
    "is_int_positive_or_zero",
    "is_int_negative",
    "is_int_negative_or_zero",
]


def _get_int_number(value: int, message: str) -> int:
    try:
        return int(value)
    except (ValueError, TypeError):
        raise ArgumentTypeError(message) from None


def is_int_positive(value: int) -> int:
    """
    Verify that argument passed is a positive integer.

    Parameters
    ----------
    value: int
        value passed from argparser

    Example
    -------

    .. code-block::

        parser.add_argument(
            "--size", "-s",
            dest="size",
            help="[MB] Minimal size of attachment",
            type=torxtools.argtools.is_int_positive,
            default=100,
        )
    """
    message = f"value '{value}' must be positive"
    number = _get_int_number(value, message)
    if number <= 0:
        raise ArgumentTypeError(message) from None
    return number


def is_int_positive_or_zero(value: int) -> int:
    """
    Verify that argument passed is a positive integer or zero.

    Parameters
    ----------
    value: int
        value passed from argparser

    Example
    -------

    .. code-block::

        parser.add_argument(
            "--size", "-s",
            dest="size",
            help="[MB] Minimal size of attachment",
            type=torxtools.argtools.is_int_positive_or_zero,
            default=100,
        )
    """
    message = f"value '{value}' must be positive or zero"
    number = _get_int_number(value, message)
    if number < 0:
        raise ArgumentTypeError(message) from None
    return number


def is_int_negative(value: int) -> int:
    """
    Verify that argument passed is a negative integer.

    Parameters
    ----------
    value: int
        value passed from argparser

    Example
    -------

    .. code-block::

        parser.add_argument(
            "--temperature", "-t",
            dest="temperature",
            help="[C] Temperature colder than freezing point",
            type=torxtools.argtools.is_int_negative,
            default=-50,
        )
    """
    message = f"value '{value}' must be negative"
    number = _get_int_number(value, message)
    if number >= 0:
        raise ArgumentTypeError(message) from None
    return number


def is_int_negative_or_zero(value: int) -> int:
    """
    Verify that argument passed is a negative integer or zero.

    Parameters
    ----------
    value: int
        value passed from argparser

    Example
    -------

    .. code-block::

        parser.add_argument(
            "--temperature", "-t",
            dest="temperature",
            help="[C] Temperature colder than freezing point",
            type=torxtools.argtools.is_int_negative_or_zero,
            default=-50,
        )
    """
    message = f"value '{value}' must be negative or zero"
    number = _get_int_number(value, message)
    if number > 0:
        raise ArgumentTypeError(message) from None
    return number
