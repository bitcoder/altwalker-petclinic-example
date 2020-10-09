from selenium.webdriver.common.by import By

from .base import BasePage


class FindOwnersPage(BasePage):
    """finds owners"""

    _submit_button_locator = (By.CSS_SELECTOR, "button[type=\"submit\"]")
    _xicon_search_locator = (By.CLASS_NAME, "icon-search")
    _add_owner_locator = (By.LINK_TEXT, "Add Owner")

    _footer_logo_locator = (By.XPATH, "/html/body/div/table/tbody/tr/td[2]/img")
    
    @property
    def is_footer_present(self):
       return self.is_element_present(*self._footer_logo_locator)

    def click_submit(self):
        self.find_element(*self._submit_button_locator).click()

    def xclick_search(self):
        self.find_element(*self._icon_search_locator).click()

    def click_add_owner(self):
        self.find_element(*self._add_owner_locator).click()



