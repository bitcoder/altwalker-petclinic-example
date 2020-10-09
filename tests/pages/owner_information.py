from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

from .base import BasePage



class OwnerInformationPage(BasePage):
    """owner information"""

    _submit_button_locator = (By.CSS_SELECTOR, "button[type=\"submit\"]")
    _add_new_pet_locator = (By.LINK_TEXT, "Add New Pet")
    _edit_pet_locator = (By.LINK_TEXT, "Edit Pet")
    _add_visit_locator = (By.LINK_TEXT, "Add Visit")

    _name_locator = (By.ID, "name")
    _birth_date_locator = (By.ID, "birthDate")
    _type_locator = (By.ID, "type")
    _datepicker_locator = (By.ID, "ui-datepicker-div")

    _description_locator = (By.ID, "description")
    _visit_locator = (By.ID, "visit")

    _pets_locator = (By.XPATH, "//table/tbody/tr/td//dl")


    def click_add_new_pet(self):
        self.find_element(*self._add_new_pet_locator).click()

    def click_edit_pet(self):
        self.find_element(*self._edit_pet_locator).click()

    def click_add_visit(self):
        self.find_element(*self._add_visit_locator).click()

    def fillout_pet(self, name="", birth_date="", type=""):
        self.find_element(*self._name_locator).clear()
        self.find_element(*self._name_locator).send_keys(name)
        self.find_element(*self._birth_date_locator).clear()
        self.find_element(*self._birth_date_locator).send_keys(birth_date + Keys.ENTER)
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(self._datepicker_locator)
        )
        select = Select(self.find_element(*self._type_locator))
        select.select_by_value(type)


    def click_submit(self):
        self.find_element(*self._submit_button_locator).click()

    def clear_description(self):
        self.find_element(*self._description_locator).clear()

    def set_description(self, text=""):
        self.find_element(*self._description_locator).send_keys(text)

    @property
    def is_visit_visible(self):
       return self.is_element_present(*self._visit_locator)

    @property
    def number_of_pets(self):
       return len(self.find_elements(*self._pets_locator))

       