"""
Folder module for dost. This module contains functions for working with folders and files.

Examples:
    >>> from dost import folder
    >>> folder.read_text_file('tests\\demo.txt')
    'This is a demo text file.'


The module contains the following functions:

- `read_text_file(path)`: Read a text file and return the content as a string.
- `write_text_file(path, content)`: Write a text file with the given content.

"""

import os
from pathlib import WindowsPath
from typing import List, Union
from dost.helpers import dostify


@dostify(errors=[(FileNotFoundError, '')])
def read_text_file(path: Union[str, List[str], WindowsPath, List[WindowsPath]]) -> Union[str, List[str]]:
    """Reads a text file and returns its contents as a string.

    Args:
        path (Union[str, List[str], WindowsPath, List[WindowsPath]]): The path to the text file.

    Returns:
         The contents of the text file. If a list of paths is provided, a list of strings is returned. 

    Examples:
        >>> read_text_file('tests\\demo.txt')
        'This is a demo text file.'

        >>> read_text_file(['tests\\demo.txt', 'tests\\demo2.txt'])
        ['This is a demo text file.', 'This is a demo2 text file.']

    """
    if isinstance(path, list):
        return [read_text_file(path) for path in path]

    file_path = os.path.abspath(path)

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f'File not found: {file_path}')
    with open(path, 'r') as f:
        return f.read()


@dostify(errors=[])
def write_text_file(path: Union[str, WindowsPath], contents: str) -> None:
    """ Write a text file with the given contents.

    Args:
        path (Union[str, WindowsPath]): The path to the text file.
        contents (str): The contents of the text file.

    Examples:
        >>> write_text_file('tests\\demo.txt', 'This is a demo text file.')
        >>> read_text_file('tests\\demo.txt')
        'This is a demo text file.'
    """
    # Body section
    path = os.path.abspath(path)
    with open(path, 'w') as f:
        f.write(contents)
