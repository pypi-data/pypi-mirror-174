""" 
Utility module for dost. This module contains utility functions. 

Examples:
    >>> import dost.utility as utility
    >>> utility.pause_program(5)
    >>> utility.api_request("https://google.com")
    >>> utility.clipboard_set_data("Hello World")
    >>> utility.GetClipboardFormats()
    >>> utility.clipboard_get_data()
    >>> utility.clear_output()
    >>> utility.install_module("requests")
    >>> utility.uninstall_module("requests")


This module contains the following functions:

- `pause_program(seconds:int="5")`: Pauses the program for the specified number of seconds
- `api_request(url: str, method='GET', body: dict = None, headers: dict = None)->dict`: Makes an API request to the specified URL
- `clipboard_set_data(data:str, format_id=win32clipboard.CF_UNICODETEXT)`: Sets the clipboard data to the specified data
- `GetClipboardFormats()`: Returns a list of all the formats available in the clipboard
- `clipboard_get_data(format_id=win32clipboard.CF_UNICODETEXT)->typing.Any`: Gets the data from the clipboard
- `clear_output()`: Clears the output of the console
- `install_module(module_name:str)`: Installs the specified module
- `uninstall_module(module_name:str)`: Uninstalls the specified module 

"""


from pathlib import WindowsPath
import win32clipboard
import typing as typing
from typing import List
from dost.helpers import dostify

dostify(errors=[()])


def pause_program(seconds: int = "5") -> None:
    """Pauses the program for the specified number of seconds

    Args:
        seconds (int, optional): Number of seconds to pause the program. Defaults to "5".

    Examples:
        >>> pause_program(5)
    """

    # Import Section
    import time

    # Code Section
    time.sleep(seconds)


dostify(errors=[()])


def api_request(url: str, method='GET', body: dict = None, headers: dict = None) -> dict:
    """Makes an API request to the specified URL

    Args:
        url (str): URL to make request to
        method (str, optional): HTTP method to use. Defaults to 'GET'.
        body (dict, optional): Body of the request. Defaults to None.
        headers (dict, optional): Headers of the request. Defaults to None.

    Returns:
        dict: Response from the API

    Examples:
        >>> api_request("https://google.com")
    """

    # Import Section
    import requests
    import json

    # Code Section
    if headers is None:
        headers = {"charset": "utf-8", "Content-Type": "application/json"}

    if method == 'GET':
        response = requests.get(
            url, headers=headers, params=body)
    elif method == 'POST':
        response = requests.post(
            url, data=json.dumps(body), headers=json.dumps(headers))
    elif method == 'PUT':
        response = requests.put(
            url, data=json.dumps(body), headers=json.dumps(headers))
    elif method == 'DELETE':
        response = requests.delete(
            url, data=json.dumps(body), headers=json.dumps(headers))
    else:
        raise Exception("Invalid method")
    if response.status_code in [200, 201, 202, 203, 204]:
        data = response.json()
    else:
        raise Exception(response.text)
    return data


# api request todos free api
# print(api_request("https://todos.free.beeceptor.com/todos", body='', headers={}))
# print(api_request(url='https://todos.free.beeceptor.com/todos'))

dostify(errors=[()])


def clipboard_set_data(data: str, format_id=win32clipboard.CF_UNICODETEXT) -> None:
    """Sets the clipboard data to the specified data

    Args:
        data (str): Data to set the clipboard to
        format_id (int, optional): Format ID of the data. Defaults to win32clipboard.CF_UNICODETEXT.

    Examples:
        >>> clipboard_set_data("Hello World")
    """
    # Import Section

    import win32clipboard

    # Code Section
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(format_id, data)
    win32clipboard.CloseClipboard()


dostify(errors=[()])


def GetClipboardFormats() -> list:
    """Returns a list of all the formats available in the clipboard

    Returns:
        list: List of formats in the clipboard

    Examples:
        >>> GetClipboardFormats()
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


dostify(errors=[()])


def clipboard_get_data(format_id=win32clipboard.CF_UNICODETEXT) -> typing.Any:
    """Gets the data from the clipboard

    Returns:
        string:the data from the clipboard

    Examples:
        >>> clipboard_get_data()
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


dostify(errors=[()])


def clear_output() -> None:
    """Clears the output of the console

    Examples:
        >>> clear_output()
    """

    # Import Section
    import os

    # Code Section
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


dostify(errors=[()])


def install_module(module_name: str) -> None:
    """Installs the specified module

    Args:
        module_name (str): Name of the module to install

    Examples:
        >>> install_module("requests")
    """
    # Code Section
    if module_name != "dost":
        import subprocess
        import sys
        subprocess.call([sys.executable, "-m", "pip",
                        "install", module_name])


dostify(errors=[()])


def uninstall_module(module_name: str) -> None:
    """Uninstalls the specified module

    Args:
        module_name (str): Name of the module to uninstall

    Examples:
        >>> uninstall_module("requests")
    """
    # Code Section
    if module_name != "dost":
        import subprocess
        import sys
        subprocess.call([sys.executable, "-m", "pip",
                        "uninstall", "-y", module_name])
    else:
        raise Exception(
            "You cannot uninstall dost from here.")


dostify(errors=[()])


def image_to_text(image_path: WindowsPath) -> str:
    """Converts the specified image to text

    Args:
        image_path (WindowsPath): Path to the image

    Returns:
        string: Text from the image

    Examples:
        >>> image_to_text("tests\demo2.png")
    """
    # Import Section
    from PIL import Image
    import pytesseract

    # Code Section
    image = Image.open(image_path)
    data = pytesseract.image_to_string(image)

    return data
