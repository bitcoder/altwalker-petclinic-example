from selenium.webdriver.common.by import By

from .base import BasePage


class HomePage(BasePage):
    """homepage"""

    _home_locator = (By.CLASS_NAME, "icon-home")
    _veterinarians_locator = (By.CLASS_NAME, "icon-th-list")
    _find_owners_locator = (By.CLASS_NAME, "icon-search")

    def click_home(self):
        self.find_element(*self._home_locator).click()

    def click_find_owners(self):
        self.find_element(*self._find_owners_locator).click()

    def click_veterinarians(self):
        self.find_element(*self._veterinarians_locator).click()
