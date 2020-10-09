from pypom import Page
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class BasePage(Page):
    """Interact with elements commnon on every page, which in this case are the top menu links."""

    _icon_find_owners_locator = (By.CLASS_NAME, "icon-search")

    _footer_logo_locator = (By.XPATH, "/html/body/div/table/tbody/tr/td[2]/img")
    _heading_locator = (By.TAG_NAME, "h2")
    
    @property
    def is_footer_present(self):
       return self.is_element_present(*self._footer_logo_locator)

    @property
    def heading_text(self):
        #e = self.find_element(*self._heading_locator)
        #e  = self.driver.find_elements_by_tag_name('h2')
        #print(e)
        #print(e.text)
        return self.find_element(*self._heading_locator).text
        #return self.driver.find_elements_by_tag_name('h2')[0].text

    def click_find_owners(self):
        self.find_element(*self._icon_find_owners_locator).click()