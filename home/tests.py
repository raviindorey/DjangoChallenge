from django.test import TestCase
from selenium import webdriver


class FunctionalTests(TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        # self.browser = webdriver.Firefox()

    def test_home_loads(self):
        self.browser.get('http://localhost:8000/')
        self.assertIn('The task is', self.browser.page_source)

    def test_card_link_navigation_works(self):
        self.browser.get('http://localhost:8000/')
        self.browser.find_element_by_class_name('card-link').click()
        self.assertIn('Add a new card', self.browser.page_source)

    def test_address_link_navigation_works(self):
        self.browser.get('http://localhost:8000/')
        self.browser.find_element_by_class_name('address-link').click()
        self.assertIn('Need an existing user first', self.browser.page_source)
        self.assertIn('<input type="hidden" name="next" value="/address">',
                      self.browser.page_source)

    def tearDown(self):
        self.browser.quit()
