"""
Mouse module for dost. This module contains functions for mouse control.

Examples:
    >>> from dost import mouse
    >>> mouse.click(100, 100)
    >>> mouse.search('tests\\demo.png')
    (23, 17)


The module contains the following functions:

- `click(x, y, button, clicks, absolute)`: Click at the given coordinates.
- `search(img, wait, left_click)`: Search for an image on the screen and return the coordinates of the top-left corner of the image.
"""

from typing import List, Tuple, Union
from dost.helpers import dostify
from pathlib import WindowsPath


@dostify(errors=[(ValueError, '')])
def click(x: int, y: int, button: str = "left", clicks: int = 1, absolute: bool = True):
    """Clicks the mouse at the given co-ordinates.
    Args:
        x (int): X co-ordinate.
        y (int): Y co-ordinate.
        button (str): The button to click. Can be "left", "right" or "middle". Defaults to "left". Possible values: "left", "l", "right", "r", "middle", "m".
        clicks (int): Number of times to click the mouse button. Defaults to 1.
        absolute (bool): Whether the co-ordinates are absolute or relative to the current position. Defaults to True.

    Examples:
        >>> click(100, 100)
        >>> click(100, 100, button="right")
        >>> click(100, 100, button="middle")
        >>> click(100, 100, button="left", clicks=2)
        >>> click(100, 100, button="left", clicks=2, absolute=False)

    """

    # import section
    import pywinauto as pwa
    import win32api

    if button not in ["left", "right", "middle", "l", "r", "m"]:
        raise ValueError(
            f'Invalid button: {button}. Possible values: "left", "l", "right", "r", "middle", "m".')

    if not absolute:
        current_x, current_y = win32api.GetCursorPos()
        x, y = (current_x + x), (current_y + y)

    if button in {"left", "l"}:
        button = "left"
    elif button in {"right", "r"}:
        button = "right"
    elif button in {"middle", "m"}:
        button = "middle"

    for _ in range(clicks):
        pwa.mouse.click(coords=(x, y), button=button)


@dostify(errors=[(FileNotFoundError, ''), (ValueError, '')])
def search(img: Union[str, List[str], WindowsPath, List[WindowsPath]], wait: int = 10, left_click: bool = False) -> Union[Tuple[int, int], List[Tuple[int, int]], None]:
    """Searches for the given image and returns the co-ordinates of the image.

    Args:
        img (Union[str, List[str], WindowsPath, List[WindowsPath]]): The path to the image.
        wait (int): The time to wait for the image to appear. Defaults to 10.
        left_click (bool): Whether to left click on the image. Defaults to False.

    Returns:
        A tuple containing the X and Y co-ordinates of the image.

    Examples:
        >>> search('tests\\demo.png')
        (23, 17)
        >>> search('tests\\demo.png', wait=20, left_click=True)
        >>> search(['tests\\demo.png', 'tests\\demo2.png'])
        [(23, 17), (67, 16)]
        >>> search('tests\\demo2.pdf')
        You got ValueError error: Invalid image file: D:\PyBOTs\dost\\tests\demo2.pdf. Supported image formats: .png, .jpg, .jpeg, .bmp, .gif
    """
    # import section
    import pyscreeze as ps
    import os

    # List case handling
    if isinstance(img, list):
        return [search(i, wait=wait) for i in img]

    # Validation section
    path = os.path.abspath(img)
    if not os.path.isfile(path):
        raise FileNotFoundError(f'File not found: {path}')

    # check whether given image is a valid image file or not
    ext = os.path.splitext(path)[1]
    if ext not in ['.png', '.jpg', '.jpeg', '.bmp', '.gif']:
        raise ValueError(
            f'Invalid image file: {path}. Supported image formats: .png, .jpg, .jpeg, .bmp, .gif')

    # Body section
    point = ps.locateCenterOnScreen(path,  minSearchTime=wait)
    if point is None:
        raise ValueError(f'Image not found: {path}')
    if left_click:
        click(point.x, point.y)
        return None
    return (point.x, point.y)
