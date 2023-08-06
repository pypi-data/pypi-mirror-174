"""Module for handy using of selenium."""

import time
from typing import Optional

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.selenium_loader import SeleniumLoader


class SeleniumBase:
    """
    Base class for handy selenium usage.
    """

    def __init__(self, driver: webdriver.Chrome = None):
        if driver is not None:
            self.driver = driver

    def setup_driver(
        self,
        driver_path: Optional[str] = None,
        user_options: Optional[webdriver.ChromeOptions] = None,
    ):
        self.driver = SeleniumLoader(driver_path, user_options).driver

    def click(self, xpath: str):
        """
        Wrapper function of clicking DOM element
        """
        element = self.wait_until(xpath)
        self._click(element)

    def double_click(self, xpath: str):
        """
        Wrapper function of clicking DOM element
        """
        element = self.wait_until(xpath)
        self._double_click(element)

    def context_click(self, xpath: str):
        """
        Wrapper function of context clicking DOM element
        """
        element = self.wait_until(xpath)
        self._context_click(element)

    def _context_click(self, element: WebElement):
        action = ActionChains(self.driver)
        action.context_click(element).perform()

    def _click(self, element: WebElement):
        webdriver.ActionChains(self.driver).move_to_element(element).click(
            element
        ).perform()

    def _double_click(self, element: WebElement):
        webdriver.ActionChains(self.driver).move_to_element(
            element
        ).double_click(element).perform()

    def click_and_send_key(self, xpath: str, key: str):
        """
        Wrapper function of clicking DOM element and a key.
        """
        time.sleep(0.5)
        element = self.wait_until(xpath)
        self._click(element)
        element.send_keys(key)

    def wait_until(
        self, xpath: str, wait_time: int = 3
    ) -> Optional[WebElement]:
        """
        Wait until certain element is attached to the document.
        """
        element = WebDriverWait(self.driver, wait_time).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element

    def scroll_down(self, height: Optional[int] = None, bottom: bool = True):
        """
        Wrapper function for scrolling down the page. It will goes to the bottom
        of the page by default.
        """
        if bottom and height is None:
            height = "document.body.scrollHeight"
            if height is not None:
                print("'height' parameter is ignored due to 'bottom' parameter")

        self.driver.execute_script(f"window.scrollTo(0, {height});")

    def scroll_up(self, height: Optional[int] = None):
        """
        Wrapper function for scrolling up the page. It will goes to the top of
        the page by default.
        """
        self.driver.execute_script(f"window.scrollTo(0, {height});")

    def __del__(self):
        self.driver.close()
