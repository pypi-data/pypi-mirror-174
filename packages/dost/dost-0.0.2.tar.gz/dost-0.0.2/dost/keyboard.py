"""
Keyboard module for dost.This module contains functions for keyboard input and output.

Examples:
    >>> from dost import keyboard
    >>> keyboard.key_pressed('a')
    >>> keyboard.key_write_enter('Hello World!')
    >>> keyboard.key_hit_enter()


This module contains the following functions:

`key_pressed(key)`: Check if a key is pressed.
`key_write_enter(text)`: Write text and press enter.
`key_hit_enter()`: Press enter.

"""


from dost.helpers import dostify


@dostify(errors=[])
def key_press(write_to_window: str, key_1: str, key_2: str = '', key_3: str = '') -> None:
    """Press a key or a combination of keys.
    Args:
        write_to_window (str): The window to write to.
        key_1 (str): The first key to press.
        key_2 (str): The second key to press.
        key_3 (str): The third key to press.
    Examples:
        >>> key_press('Notepad', 'a')
        >>> key_press('Notepad', '{VK_CONTROL}', 'S')
        >>> key_press('Notepad', '{VK_CONTROL}', 'S',"enter")
    """
    # Import Section
    import pywinauto as pwa
    from windows import window_activate_window

    # Code Section
    if key_1 == '':
        raise Exception("Key 1 is empty.")

    special_keys = ['{SCROLLLOCK}', '{VK_SPACE}', '{VK_LSHIFT}', '{VK_PAUSE}', '{VK_MODECHANGE}',
                    '{BACK}', '{VK_HOME}', '{F23}', '{F22}', '{F21}', '{F20}', '{VK_HANGEUL}', '{VK_KANJI}',
                    '{VK_RIGHT}', '{BS}', '{HOME}', '{VK_F4}', '{VK_ACCEPT}', '{VK_F18}', '{VK_SNAPSHOT}',
                    '{VK_PA1}', '{VK_NONAME}', '{VK_LCONTROL}', '{ZOOM}', '{VK_ATTN}', '{VK_F10}', '{VK_F22}',
                    '{VK_F23}', '{VK_F20}', '{VK_F21}', '{VK_SCROLL}', '{TAB}', '{VK_F11}', '{VK_END}',
                    '{LEFT}', '{VK_UP}', '{NUMLOCK}', '{VK_APPS}', '{PGUP}', '{VK_F8}', '{VK_CONTROL}',
                    '{VK_LEFT}', '{PRTSC}', '{VK_NUMPAD4}', '{CAPSLOCK}', '{VK_CONVERT}', '{VK_PROCESSKEY}',
                    '{ENTER}', '{VK_SEPARATOR}', '{VK_RWIN}', '{VK_LMENU}', '{VK_NEXT}', '{F1}', '{F2}',
                    '{F3}', '{F4}', '{F5}', '{F6}', '{F7}', '{F8}', '{F9}', '{VK_ADD}', '{VK_RCONTROL}',
                    '{VK_RETURN}', '{BREAK}', '{VK_NUMPAD9}', '{VK_NUMPAD8}', '{RWIN}', '{VK_KANA}',
                    '{PGDN}', '{VK_NUMPAD3}', '{DEL}', '{VK_NUMPAD1}', '{VK_NUMPAD0}', '{VK_NUMPAD7}',
                    '{VK_NUMPAD6}', '{VK_NUMPAD5}', '{DELETE}', '{VK_PRIOR}', '{VK_SUBTRACT}', '{HELP}',
                    '{VK_PRINT}', '{VK_BACK}', '{CAP}', '{VK_RBUTTON}', '{VK_RSHIFT}', '{VK_LWIN}', '{DOWN}',
                    '{VK_HELP}', '{VK_NONCONVERT}', '{BACKSPACE}', '{VK_SELECT}', '{VK_TAB}', '{VK_HANJA}',
                    '{VK_NUMPAD2}', '{INSERT}', '{VK_F9}', '{VK_DECIMAL}', '{VK_FINAL}', '{VK_EXSEL}',
                    '{RMENU}', '{VK_F3}', '{VK_F2}', '{VK_F1}', '{VK_F7}', '{VK_F6}', '{VK_F5}', '{VK_CRSEL}',
                    '{VK_SHIFT}', '{VK_EREOF}', '{VK_CANCEL}', '{VK_DELETE}', '{VK_HANGUL}', '{VK_MBUTTON}',
                    '{VK_NUMLOCK}', '{VK_CLEAR}', '{END}', '{VK_MENU}', '{SPACE}', '{BKSP}', '{VK_INSERT}',
                    '{F18}', '{F19}', '{ESC}', '{VK_MULTIPLY}', '{F12}', '{F13}', '{F10}', '{F11}', '{F16}',
                    '{F17}', '{F14}', '{F15}', '{F24}', '{RIGHT}', '{VK_F24}', '{VK_CAPITAL}', '{VK_LBUTTON}',
                    '{VK_OEM_CLEAR}', '{VK_ESCAPE}', '{UP}', '{VK_DIVIDE}', '{INS}', '{VK_JUNJA}',
                    '{VK_F19}', '{VK_EXECUTE}', '{VK_PLAY}', '{VK_RMENU}', '{VK_F13}', '{VK_F12}', '{LWIN}',
                    '{VK_DOWN}', '{VK_F17}', '{VK_F16}', '{VK_F15}', '{VK_F14}']

    def make_down(key):
        return key.replace('}', ' down}')

    def make_up(key):
        return key.replace('}', ' up}')

    case_0 = True if not key_2 and not key_3 else False
    case_1 = True if key_1 in special_keys and key_2 not in special_keys and key_3 not in special_keys else False  # Only 1 Special Key
    case_2 = True if key_1 in special_keys and key_2 in special_keys and key_3 not in special_keys else False  # 2 Special Keys

    if write_to_window:
        window_activate_window(write_to_window)

    if case_0:
        pwa.keyboard.send_keys(str(key_1))
    elif case_1:
        key_1_down = make_down(key_1)
        key_1_up = make_up(key_1)
        pwa.keyboard.send_keys(str(key_1_down + key_2 + key_3 + key_1_up))
    elif case_2:
        key_1_down = make_down(key_1)
        key_1_up = make_up(key_1)
        key_2_down = make_down(key_2)
        key_2_up = make_up(key_2)
        pwa.keyboard.send_keys(
            str(key_1_down + key_2_down + key_3 + key_2_up + key_1_up))


@dostify(errors=[])
def key_write_enter(write_to_window: str, text_to_write: str, key: str = "e") -> None:
    """Write text to window and press enter key

    Args:
        write_to_window (str): Window to write to
        text_to_write (str): Text to write
        key (str, optional): Key to press. Defaults to "e".

    Examples:
        >>> key_write_enter("Notepad", "Hello World")
    """

    # Import Section
    import time
    import pywinauto as pwa
    from windows import window_activate_window

    # Code Section
    if not text_to_write:
        raise Exception("Text to write is empty.")

    if write_to_window:
        window_activate_window(write_to_window)

    time.sleep(0.2)
    pwa.keyboard.send_keys(
        text_to_write, with_spaces=True, with_tabs=True, with_newlines=True)
    if key.lower() == "e":
        pwa.keyboard.send_keys('{ENTER}')
    if key.lower() == "t":
        pwa.keyboard.send_keys('{TAB}')


@dostify(errors=[])
def key_hit_enter(write_to_window: str) -> None:
    """Hit enter key

    Args:
        write_to_window (str): Window to write to

    Examples:
        >>> key_press(write_to_window=write_to_window, key="enter",)
        """

    # Import Section
    import pywinauto as pwa
    from windows import window_activate_window

    # Code Section
    if write_to_window:
        window_activate_window(write_to_window)

    pwa.keyboard.send_keys('{ENTER}')
