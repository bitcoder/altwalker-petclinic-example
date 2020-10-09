from selenium.webdriver.common.by import By

from .base import BasePage


class VeterinariansPage(BasePage):
    """veterinarian"""

    _search_input_locator = (By.CSS_SELECTOR, "input[type=\"search\"]")
    _vets_table_cel_locator = (By.XPATH, "//table[@id='vets']/tbody/tr/td")
    _vets_table_rows_locator = (By.XPATH, "//table[@id='vets']/tbody/tr")

    def search_for(self, text=""):
        self.find_element(*self._search_input_locator).clear()
        self.find_element(*self._search_input_locator).send_keys(text)

    @property
    def is_text_present_in_vets_table(self, text=""):
       return self.is_element_present(*self._vets_table_cel_locator)
    
    @property
    def number_of_vets_in_table(self):
        return len(self.find_elements(*self._vets_table_rows_locator))