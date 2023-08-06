"""
Clipboard module for dost. This module is used to interact with the Windows clipboard.

Examples:
    >>> from dost import clipboard
    >>> clipboard.clipboard_set_data('Hello World!')
    >>> clipboard.clipboard_get_data()


It contains the following functions:

` clipboard_set_data(data, format_id)`: Set the clipboard data to the given string.
` clipboard_get_data(format_id) -> str`: Get the clipboard data as a string.
` GetClipboardFormats()`: Get a list of all available clipboard formats.

"""


import win32clipboard
from dost.helpers import dostify


@dostify(errors=[])
def clipboard_set_data(data: str, format_id=win32clipboard.CF_UNICODETEXT) -> None:
    """Set the clipboard data to the given string.

    Args:
        data (str): The data to set the clipboard to.
        format_id (int): The format of the data. Defaults to CF_UNICODETEXT.

    Examples:
        >>> clipboard_set_data('Hello World!')
        >>> clipboard_get_data()
        'Hello World!'

    """
    # Import Section
    import win32clipboard

    # Code Section
    win32clipboard.OpenClipboard()
    try:
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(format_id, data)
    finally:
        win32clipboard.CloseClipboard()


@dostify(errors=[])
def GetClipboardFormats() -> list:
    """Get a list of all available clipboard formats.

    Returns:
        A list of all available clipboard formats.

    Examples:
        >>> GetClipboardFormats()
        [1,2,3]

    """
    # Import Section
    import win32clipboard

    # Code Section
    win32clipboard.OpenClipboard()
    available_formats = []
    current_format = 0
    while True:
        current_format = win32clipboard.EnumClipboardFormats(current_format)
        if not current_format:
            break
        available_formats.append(current_format)
    win32clipboard.CloseClipboard()
    return available_formats


@dostify(errors=[])
def clipboard_get_data(format_id=win32clipboard.CF_UNICODETEXT) -> str:
    """Get the clipboard data as a string.

    Args:
        format_id (int): The format of the data. Defaults to CF_UNICODETEXT.

    Returns:
        The clipboard data as a string.

    Examples:
        >>> clipboard_get_data()
        'Hello World!'
    """
    # Import Section
    import win32clipboard

    # Code Section
    if format_id not in GetClipboardFormats():
        raise RuntimeError("That format is not available")
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData(format_id)
    win32clipboard.CloseClipboard()

    return data
