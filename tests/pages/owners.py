from selenium.webdriver.common.by import By

from .base import BasePage

class OwnersPage(BasePage):
    """list owners"""

    _owners_rows_locator = (By.XPATH, "//table[@id='owners']/tbody/tr")

    @property
    def total_owners_in_list(self):
        return len(self.find_elements(*self._owners_rows_locator))
