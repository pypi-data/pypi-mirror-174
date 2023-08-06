"""
Windows module for dost.This module contains functions that are specific to Windows.

Examples:
    >>> from dost import windows
    >>> windows._window_find_exact_name('Notepad')
    'Notepad'
    >>> windows.show_desktop()
    >>> windows.window_get_active_window()
    'Notepad'
    >>> window.window_get_all_opened_titles_windows()
    ['Notepad', 'Program Manager', 'Desktop']
    >>> windows.window_maximize_windows('Notepad')
    >>> windows.window_minimize_windows('Notepad')
    >>> windows.window_close_windows('Notepad')
    >>> windows.launch_any_exe_bat_application('notepad.exe')


The module contains the following functions:

- `_window_find_exact_name(window_name)`: Find a window by its exact name.
- `show_desktop()`: Show the desktop.
- `window_get_active_window()`: Get the active window.
- `window_get_all_opened_titles_windows()`: Get all opened windows.
- `window_maximize_windows(window_name)`: Maximize a window.
- `window_minimize_windows(window_name)`: Minimize a window.
- `window_close_windows(window_name)`: Close a window.
- `launch_any_exe_bat_application(application_name)`: Launch any exe or bat application.

"""


from multiprocessing.sharedctypes import Value
from pathlib import WindowsPath
from typing import List, Union
from xml.etree.ElementTree import QName
from dost.helpers import dostify


@dostify(errors=[ValueError, ''])
def _window_find_exact_name(windowName: str) -> str:
    """Find window by exact name
    Args:
        windowName (str): Window name
    Returns:
        str: Window handle
    Examples:
        >>> _window_find_exact_name('Notepad')

    """
    # Import Section
    import pygetwindow as gw

    # Code Section
    if not windowName:
        raise ValueError(f'Window name cannot be empty')

    lst = gw.getAllTitles()
    win = ""
    for item in lst:
        if str(item).strip():
            if str(windowName).lower() in str(item).lower():
                win = item
                break
    return win


@dostify(errors=[])
def window_show_desktop() -> None:
    """Show desktop
    Examples:
        >>> window_show_desktop()
    """

    # Import Section
    import pywinauto as pwa

    # Code Section
    pwa.keyboard.send_keys('{VK_RWIN down} d {VK_RWIN up}')


@dostify(errors=[])
def window_get_active_window() -> str:
    """Get active window

    Returns:
        Union[str,List[str]]: Active window

    Examples:
        >>> window_get_active_window()
    """

    # Import Section
    import win32gui
    import pygetwindow as gw

    # Code Section
    _title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    data = _title

    return data


@dostify(errors=[(ValueError, '')])
def window_activate_window(window_title: str) -> None:
    """Activate window

    Args:
        window_title (str): Window title

    Examples:
        >>> window_activate_window('Notepad')
    """

    # Import Section
    import pygetwindow as gw

    # Code Section
    if not window_title:
        raise ValueError('Window title name is empty.')

    item = _window_find_exact_name(window_title)
    if item != "":
        windw = gw.getWindowsWithTitle(item)[0]

        try:
            windw.activate()
        except:
            windw.minimize()
            windw.maximize()
    else:
        raise ValueError(f'Window title name {window_title} not found')


@dostify(errors=[])
def window_get_all_opened_titles_windows() -> Union[str, List[str]]:
    """Get all opened titles windows

    Returns:
        Union[str, List[str]]: All opened titles windows

    Examples:
        >>> window_get_all_opened_titles_windows()
    """

    # Import Section
    import pygetwindow as gw

    # Code Section
    allTitles_lst = []
    lst = gw.getAllTitles()
    for item in lst:
        if str(item).strip() != "" and str(item).strip() not in allTitles_lst:
            allTitles_lst.append(str(item).strip())
    data = allTitles_lst
    return data


@dostify(errors=[(ValueError, '')])
def window_maximize_windows(windowName: str) -> None:
    """Maximize windows
    Args:
        windowName (str, optional): Window name. Defaults to "".
    Examples:
        >>> window_maximize_windows()
    """

    # Import Section
    import time
    import pygetwindow as gw

    # Code Section
    if not windowName:
        raise ValueError('Window title name is empty.')
    item = _window_find_exact_name(windowName)
    if item != "":
        windw = gw.getWindowsWithTitle(item)[0]
        windw.maximize()
    else:
        raise ValueError(f'Window title name {windowName} not found')


@dostify(errors=[(ValueError, '')])
def window_minimize_windows(windowName: str) -> None:
    """Minimize windows
    Args:
        windowName (str): Window name
    Examples:
        >>> window_minimize_windows('Notepad')
    """

    # Import Section
    import pygetwindow as gw

    # Code Section
    if not windowName:
        raise ValueError(f'Window title name is empty.')

    item = _window_find_exact_name(windowName)
    if item != "":
        windw = gw.getWindowsWithTitle(item)[0]
        windw.minimize()
    else:
        raise ValueError(f'Window title name {windowName} not found')


@dostify(errors=[(ValueError, '')])
def window_close_windows(windowName: str) -> None:
    """Close windows
    Args:
        windowName (str): Window name
    Examples:
        >>> window_close_windows('Notepad')
    """

    # Import Section
    import pygetwindow as gw

    # Code Section
    if not windowName:
        raise ValueError('Window title name is empty.')

    item = _window_find_exact_name(windowName)
    if item != "":
        windw = gw.getWindowsWithTitle(item)[0]
        windw.close()
    else:
        raise ValueError(f'Window title name {windowName} not found')


@dostify(errors=[(FileNotFoundError, ''), (ValueError, '')])
def launch_any_exe_bat_application(pathOfExeFile: Union[str, WindowsPath]) -> None:
    """Launch any exe/bat application
    Args:
        pathOfExeFile (Union[str,WindowsPath]): Path of exe/bat file
    Examples:
        >>> launch_any_exe_bat_application(WindowsPath('C:\\Windows\\System32\\notepad.exe'))
    """

    # Import Section
    import win32gui
    import win32con
    import os
    import time

    # Code Section
    if not pathOfExeFile:
        raise ValueError('Path of the exe file is empty.')

    try:
        pathOfExeFile = os.path.abspath(pathOfExeFile)
        os.startfile(pathOfExeFile)
        time.sleep(2)
        hwnd = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

    except Exception:
        raise FileNotFoundError(f'No file found at {pathOfExeFile}')
