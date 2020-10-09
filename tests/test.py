import unittest

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from tests.pages.base import BasePage
from tests.pages.home import HomePage
from tests.pages.find_owners import FindOwnersPage
from tests.pages.owners import OwnersPage
from tests.pages.new_owner import NewOwnerPage
from tests.pages.veterinarians import VeterinariansPage
from tests.pages.owner_information import OwnerInformationPage

import sys
import pdb
from faker import Faker

debugger = pdb.Pdb(skip=['altwalker.*'], stdout=sys.stdout)
fake = Faker()

HEADLESS = False
BASE_URL = "http://localhost:9966/petclinic"

driver = None


def setUpRun():
    """Setup the webdriver."""

    global driver

    options = Options()
    if HEADLESS:
        options.add_argument('-headless')

    print("Create a new Firefox session")
    driver = webdriver.Firefox(options=options)

    print("Set implicitly wait")
    driver.implicitly_wait(15)
    print("Window size: {width}x{height}".format(**driver.get_window_size()))

def tearDownRun():
    """Close the webdriver."""

    global driver

    print("Close the Firefox session")
    driver.quit()

class BaseModel(unittest.TestCase):
	"""Contains common methods for all models."""

	def setUpModel(self):
		global driver
		print("Set up for: {}".format(type(self).__name__))
		self.driver = driver

	def v_HomePage(self):
		page = HomePage(self.driver)
		self.assertEqual(page.heading_text, "Welcome", "Welcome heading should be present")
		self.assertTrue(page.is_footer_present, "footer should be present")
	
	def v_FindOwners(self):
		page = FindOwnersPage(self.driver)
		self.assertEqual("Find Owners",page.heading_text, "Find Owners heading should be present")
		self.assertTrue(page.is_footer_present, "footer should be present")

	def v_NewOwner(self):
		page = NewOwnerPage(self.driver)
		self.assertEqual( "New Owner",page.heading_text, "New Owner heading should be present")
		#$x("/html/body/table/tbody/tr/td[2]/img").shouldBe(visible);
		self.assertTrue(page.is_footer_present, "footer should be present")

	def v_Owners(self):
		page = OwnersPage(self.driver)
		self.assertEqual("Owners",page.heading_text, "Owners heading should be present")
		self.assertGreater(page.total_owners_in_list, 9, "Owners in listing >= 10")

	def v_Veterinarians(self):
		page = VeterinariansPage(self.driver)
		self.assertEqual(page.heading_text,"Veterinarians", "Veterinarians heading should be present")
		self.assertTrue(page.is_footer_present, "footer should be present")

	def v_OwnerInformation(self, data):
		page = OwnerInformationPage(self.driver)
		self.assertEqual(page.heading_text, "Owner Information", "Owner Information heading should be present")
		data["numOfPets"] = page.number_of_pets
		print(f"numOfPets: {page.number_of_pets}")
		self.assertTrue(page.is_footer_present, "footer should be present")

	def e_DoNothing(self, data):
		#debugger.set_trace()
		pass

	def e_FindOwners(self):
		page = BasePage(self.driver)
		page.click_find_owners()


class PetClinic(BaseModel):
	def e_StartBrowser(self):
		page = HomePage(self.driver, BASE_URL)
		page.open()

	def e_HomePage(self):
		page = HomePage(self.driver)
		page.click_home()

	def e_Veterinarians(self):
		page = HomePage(self.driver)
		page.click_veterinarians()

	def e_FindOwners(self):
		page = HomePage(self.driver)
		page.click_find_owners()

class FindOwners(BaseModel):

	def e_AddOwner(self):
		page = FindOwnersPage(self.driver)
		page.click_add_owner()

	def e_Search(self):
		page = FindOwnersPage(self.driver)
		page.click_submit()


class OwnerInformation(BaseModel):
	def e_UpdatePet(self):
		page = OwnerInformationPage(self.driver)
		page.click_submit()

	def e_AddPetSuccessfully(self):
		page = OwnerInformationPage(self.driver)
		page.fillout_pet(fake.name(),fake.past_date().strftime("%Y/%m/%d"), "dog")
		page.click_submit()

	def e_AddPetFailed(self):
		page = OwnerInformationPage(self.driver)
		page.fillout_pet("",fake.past_date().strftime("%Y/%m/%d"), "dog")
		page.click_submit()

	def e_AddNewPet(self):
		page = OwnerInformationPage(self.driver)
		page.click_add_new_pet()

	def e_EditPet(self):
		page = OwnerInformationPage(self.driver)
		page.click_edit_pet()

	def e_AddVisit(self):
		page = OwnerInformationPage(self.driver)
		page.click_add_visit()

	def v_NewPet(self):
		page = OwnerInformationPage(self.driver)
		self.assertEqual(page.heading_text, "New Pet", "New Pet heading should be present")
		self.assertTrue(page.is_footer_present, "footer should be present")

	def v_NewVisit(self):
		page = OwnerInformationPage(self.driver)
		self.assertEqual(page.heading_text, "New Visit", "New Visit heading should be present")
		self.assertTrue(page.is_visit_visible, "visit should be present")
	
	def e_VisitAddedSuccessfully(self):
		page = OwnerInformationPage(self.driver)
		page.clear_description()
		page.set_description(fake.name())
		page.click_submit()

	def e_VisitAddedFailed(self):
		page = OwnerInformationPage(self.driver)
		page.clear_description()
		page.click_submit()

	def v_Pet(self):
		page = OwnerInformationPage(self.driver)
		self.assertEqual(page.heading_text, "Pet", "Pet heading should be present")

class Veterinarians(BaseModel):
	def e_Search(self):
		page = VeterinariansPage(self.driver)
		page.search_for("helen")

	def v_SearchResult(self):
		page = VeterinariansPage(self.driver)
		self.assertTrue(page.is_text_present_in_vets_table, "Helen Leary")
		self.assertTrue(page.is_footer_present, "footer should be present")

	def v_Veterinarians(self):
		page = VeterinariansPage(self.driver)
		self.assertEqual(page.heading_text,"Veterinarians", "Veterinarians heading should be present")
		self.assertGreater(page.number_of_vets_in_table, 0, "At least one Veterinarian should be listed in table")

class NewOwner(BaseModel):

	def e_CorrectData(self):
		page = NewOwnerPage(self.driver)
		page.fill_owner_data(first_name=fake.first_name(), last_name=fake.last_name(), address=fake.address(), city=fake.city(), telephone=fake.pystr_format('##########'))
		#page.fill_telephone(fake.pystr_format('##########'))
		page.click_submit()

	def e_IncorrectData(self):
		page = NewOwnerPage(self.driver)
		page.fill_owner_data()
		#page.fill_telephone("12345678901234567890")
		page.fill_telephone(fake.pystr_format('####################'))
		page.click_submit()

	def v_IncorrectData(self):
		page = NewOwnerPage(self.driver)
		self.assertTrue(page.error_message, "numeric value out of bounds (<10 digits>.<0 digits> expected")