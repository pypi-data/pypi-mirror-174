"""
Chrome Module for py_bots.This module contains functions for browser manupulation

Examples:
    >>> browser = ChromeBrowser()
    >>> browser.open_browser()
    

The module contains the following functions:

` open_browser(dummy_browser: bool = True, profile: str = "Default", incognito: bool = False)`: Opens a chrome browser with given settings
` navigate(url)`: Navigates to given url
` write(string, field_name)`: Writes text to given element
` mouse(element to search, no. of clicks, element type)`: Clicks on given element
` scroll(direction, weight): Scrolls to webpage by given weight
` key_press(key1,key2): Press the keys in browser
` hit_enter(): Presses enter key
` refresh_page(): Refreshes the webpage
` set_waiting_time(time): Sets waiting time for browser
` get_text(element): Gets text from given element
` close(): Closes the browser

"""


import logging
from dost.CrashHandler import text_to_speech_error
from selenium.common.exceptions import TimeoutException
import os

output_folder_path = os.path.join(
    os.path.abspath(r'C:\Users\Public\PyBots'), 'My-DOST', 'Converters Folder')

if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)


class DisableLogger():

    def __enter__(self):
        logging.disable(logging.CRITICAL)

    def __exit__(self, exit_type, exit_value, exit_traceback):
        logging.disable(logging.NOTSET)


class ChromeBrowser:
    def __init__(self):
        self.browser_driver = None

    def open_browser(self, dummy_browser: bool = True, profile: str = "Default", incognito: bool = False, ):
        """This function starts browser

        Args:
            dummy_browser (bool, optional): Choose browser type. Defaults to True.
            profile (str, optional): Which profile should browser start with. Defaults to "Default".
            incognito (bool, optional): Whether to start in incognito mode or normal. Defaults to False.

        Returns:
            browser driver: Browser's driver

        Example:
            >>> browser = ChromeBrowser()
            >>> browser.open_browser()

        """
        # Import Section
        import selenium.webdriver as webdriver
        from webdriver_manager.chrome import ChromeDriverManager
        import os
        from selenium.webdriver.chrome.options import Options
        import helium

        # Code Section
        self.options = Options()

        self.options.add_argument("--start-maximized")
        self.options.add_experimental_option(
            'excludeSwitches', ['enable-logging', 'enable-automation'])

        with DisableLogger():
            if not dummy_browser:
                self.options.add_argument(
                    "user-data-dir=C:\\Users\\{}\\AppData\\Local\\Google\\Chrome\\User Data".format(os.getlogin()))
                self.options.add_argument(
                    f"profile-directory={profile}")

            if incognito:
                self.options.add_argument("--incognito")
            self.browser_driver = webdriver.Chrome(
                ChromeDriverManager().install(), options=self.options)

            helium.set_driver(self.browser_driver)
            helium.Config.implicit_wait_secs = 60
        return self.browser_driver

    def navigate(self, url: str) -> None:
        """This function navigates to given url

        Args:
            url (str): Url to navigate to

        Returns:
            None

        Example:
            >>> browser.navigate("https://www.google.com")

        """
        import helium
        helium.set_driver(self.browser_driver)
        if not url:
            helium.go_to("https://www.pybots.ai")
        else:
            helium.go_to(url)

    def write(self, text: str = '', user_visible_text_element: str = "") -> None:
        """This function writes text to given element

        Args:
            text (str, optional): Text to write. Defaults to ''.
            user_visible_text_element (str, optional): Element to write text to. Defaults to "".

        Example:
            >>> browser.write("Hello World", "Search")

        """
        # Import Section
        import helium
        import time
        from selenium.common.exceptions import WebDriverException

        # Code Section
        helium.set_driver(self.browser_driver)

        if text and str(user_visible_text_element).strip():
            if self.check_if(user_visible_text_element, "t")[0]:
                helium.write(text, into=user_visible_text_element)

        if text and not str(user_visible_text_element).strip():
            helium.write(text)

    def mouse(self, value: str = "", action_type: str = "single", value_type: str = "t") -> None:
        """This function performs mouse actions

        Args:
            value (str, optional): Element to perform mouse action on. Defaults to "".
            action_type (str, optional): Action type. Defaults to "single".
            value_type (str, optional): Type of element. Defaults to "t".

        Example:
            >>> browser.mouse("Search", "single", "t")

        """
        # Import Section
        import helium
        import sys
        from selenium.common.exceptions import WebDriverException
        import time

        # Code Section
        helium.set_driver(self.browser_driver)

        if not action_type:
            text_to_speech_error("Please provide click type", show=False)
        if not value:
            text_to_speech_error("Please provide value", show=False)
        if not value_type:
            text_to_speech_error("Please provide type", show=False)

        possible_value_types = ["t", "b", "l", "cb",
                                "rb", "i", "xp", "li"]
        possible_clicks = ["single", "double", "right", "hover"]

        if not value_type in possible_value_types:
            text_to_speech_error(
                "Value type is invalid for function mouse.", show=False)
        if not action_type in possible_clicks:
            text_to_speech_error(
                "Click type is invalid for function mouse", show=False)

        if value_type == "xp":
            if action_type == "single":
                self.browser_driver.find_element_by_xpath(
                    value).click()
            elif action_type == "double":
                _element = self.browser_driver.find_element_by_xpath(
                    value)
                helium.doubleclick(_element)
            elif action_type == "right":
                _element = self.browser_driver.find_element_by_xpath(
                    value)
                helium.rightclick(_element)
            elif action_type == "hover":
                _element = self.browser_driver.find_element_by_xpath(
                    value)
                helium.hover(_element)
        else:
            if self.check_if(value, value_type)[0]:
                if value_type == "t":
                    if action_type == "single":
                        helium.click(value)
                    elif action_type == "double":
                        helium.doubleclick(value)
                    elif action_type == "right":
                        helium.rightclick(value)
                    elif action_type == "hover":
                        helium.hover(value)
                elif value_type == "l":
                    if action_type == "single":
                        helium.click(helium.Link(value))
                    elif action_type == "double":
                        helium.doubleclick(helium.Link(value))
                    elif action_type == "right":
                        helium.rightclick(helium.Link(value))
                    elif action_type == "hover":
                        helium.hover(helium.Link(value))
                elif value_type == "li":
                    if action_type == "single":
                        helium.click(helium.ListItem(value))
                    elif action_type == "double":
                        helium.doubleclick(helium.ListItem(value))
                    elif action_type == "right":
                        helium.rightclick(helium.ListItem(value))
                    elif action_type == "hover":
                        helium.hover(helium.ListItem(value))
                elif value_type == "b":
                    if action_type == "single":
                        helium.click(helium.Button(value))
                    elif action_type == "double":
                        helium.doubleclick(helium.Button(value))
                    elif action_type == "right":
                        helium.rightclick(helium.Button(value))
                    elif action_type == "hover":
                        helium.hover(helium.Button(value))
                elif value_type == "i":
                    if action_type == "single":
                        helium.click(helium.Image(value))
                    elif action_type == "double":
                        helium.doubleclick(helium.Image(value))
                    elif action_type == "right":
                        helium.rightclick(helium.Image(value))
                    elif action_type == "hover":
                        helium.hover(helium.Image(value))
                elif value_type == "tf":
                    if action_type == "single":
                        helium.click(helium.TextField(value))
                    elif action_type == "double":
                        helium.doubleclick(helium.TextField(value))
                    elif action_type == "right":
                        helium.rightclick(helium.TextField(value))
                    elif action_type == "hover":
                        helium.hover(helium.TextField(value))
                elif value_type == "cob":
                    if action_type == "single":
                        helium.click(helium.ComboBox(value))
                    elif action_type == "double":
                        helium.doubleclick(helium.ComboBox(value))
                    elif action_type == "right":
                        helium.rightclick(helium.ComboBox(value))
                    elif action_type == "hover":
                        helium.hover(helium.ComboBox(value))
                elif value_type == "chb":
                    if action_type == "single":
                        helium.click(helium.Checkbox(value))
                    elif action_type == "double":
                        helium.doubleclick(helium.Checkbox(value))
                    elif action_type == "right":
                        helium.rightclick(helium.Checkbox(value))
                    elif action_type == "hover":
                        helium.hover(helium.Checkbox(value))
                elif value_type == "rb":
                    if action_type == "single":
                        helium.click(helium.RadioButton(value))
                    elif action_type == "double":
                        helium.doubleclick(helium.RadioButton(value))
                    elif action_type == "right":
                        helium.rightclick(helium.RadioButton(value))
                    elif action_type == "hover":
                        helium.hover(helium.RadioButton(value))

    def scroll(self, direction: str = "down", weight=3) -> None:
        """This function is used to scroll the page up or down.

        Args:
            direction (str, optional): Direction of the scroll. Defaults to "down".
            weight (int, optional): Weight of the scroll. Defaults to 3.

        Returns:
            bool: True if the scroll is successful, False otherwise.

        Example:
            >>> scroll("down", 3)

        """
        # Import Section
        import helium

        # Code Section
        helium.set_driver(self.browser_driver)
        scroll_pixs = int(weight)
        # try:
        if direction.lower() == "down":
            helium.scroll_down(scroll_pixs)
        elif direction.lower() == "up":
            helium.scroll_up(scroll_pixs)
        elif direction.lower() == "left":
            helium.scroll_left(scroll_pixs)
        elif direction.lower() == "right":
            helium.scroll_right(scroll_pixs)

    def key_press(self, key_1: str = "", key_2: str = "") -> None:
        """This function is used to press a key or a combination of keys.

        Args:
            key_1 (str, optional): First key to press. Defaults to "".
            key_2 (str, optional): Second key to press. Defaults to "".

        Returns:
            bool: True if the key press is successful, False otherwise.

        Example:
            >>> key_press("a")
            >>> key_press("ctrl", "a")
            >>> key_press("ctrl", "shift", "t")

        """
        # Import Section
        import sys
        import helium
        helium.set_driver(self.browser_driver)

        # Code Section
        if not key_1:
            text_to_speech_error("Please select the text to type")

        if key_1 and not key_2:
            helium.press(key_1)
        elif key_1 and key_2:
            helium.press(key_1 + key_2)

    def hit_enter(self) -> None:
        """This function is used to press the enter key.

        Example:
            >>> hit_enter()

        """
        # Import Section
        import helium

        # Code Section
        helium.set_driver(self.browser_driver)
        helium.press(helium.ENTER)

    def refresh_page(self) -> None:
        """This function is used to refresh the page.

        Example:
            >>> refresh_page()

        """
        # Code Section
        self.browser_driver.refresh()

    def set_waiting_time(self, time: int = 10) -> None:
        """This function is used to set the waiting time for the browser.

        Args:
            time (int, optional): Time in seconds. Defaults to 10.

        Example:
            >>> set_waiting_time(10)

        """
        # Import Section
        import helium

        # Code Section
        helium.set_driver(self.browser_driver)
        helium.Config.implicit_wait_secs = int(time)

    def get_text(self, element_xpath: str = "") -> str:
        """This function is used to get the text of an element.

        Args:
            element_xpath (str, optional): The xpath of the element. Defaults to "".

        Returns:
            str: The text of the element.

        Example:
            >>> get_text("//div[@id='some_id']")

        """
        # Code Section
        element = self.browser_driver.find_element_by_xpath(element_xpath)
        data = element.text
        return data

    def close(self) -> None:
        """This function is used to close the browser.

        Example:
            >>> close()

        """
        # Code Section
        self.browser_driver.close()
        self.browser_driver.quit()

    def __str__(self):
        return f"Chrome Browser with options: {self.options}"

# def main():
#     browser = ChromeBrowser()
#     browser.open_browser()
#     browser.navigate("https://www.google.com")

    # print(browser.get_value_relatively(element_type="Button", to_right_of="Google Search"))
    # print(browser.get_value_relatively(element_type="Text", to_left_of="Images"))
    # print(browser.get_value_relatively(element_type="Text", above="About"))
    # print(browser.get_value_relatively(element_type="Text", below="India"))

    # browser.close()

# main()
