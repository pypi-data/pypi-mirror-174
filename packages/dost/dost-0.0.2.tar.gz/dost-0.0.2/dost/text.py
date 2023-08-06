"""
String Module for dost.This module contains functions for working with strings.

Examples:
    >>> from dost import string
    >>> string_extract_only_alphabets("hello123:l;,")
    'hellol'
    >>> string_extract_only_alphabets("hello123:l;,")
    '123
    >>> string_extract_only_alphabets("hello123:l;,")
    'hello123l'

The module contains the following functions:

- `string_extract_only_alphabets(string)`: Extract only alphabets from the given string.
- `string_extract_only_numbers(string)`: Extract only numbers from the given string.
- `string_remove_special_characters(string)`: Remove special characters from the given string.

"""


from dost.helpers import dostify


@dostify(errors=[])
def string_extract_only_alphabets(inputString: str) -> str:
    """Extracts alphabets from the given string.
    Args:
        inputString (str): The string from which alphabets are to be extracted.
    Examples:
        >>> string_extract_only_alphabets("hello123:l;,")
        'hellol'
    """
    # Code Section
    data = ''.join(e for e in inputString if e.isalpha())

    return data


@dostify(errors=[])
def string_extract_only_numbers(inputString: str) -> str:
    """Extracts alphabets from the given string.
    Args:
        inputString (str): The string from which numbers are to be extracted.
    Examples:
        >>> string_extract_only_alphabets("hello123:l;,")
        '123'
    """

    # Code Section
    data = ''.join(e for e in inputString if e.isnumeric())

    return data


@dostify(errors=[])
def string_remove_special_characters(inputStr: str) -> str:
    """Removes special characters from the given string.
    Args:
        inputString (str): The string from which special characters are to be removed.
    Examples:
        >>> string_extract_only_alphabets("hello123:l;,")
        'hello123l'
    """
    # Code Section
    data = ''.join(e for e in inputStr if e.isalnum())

    return data
