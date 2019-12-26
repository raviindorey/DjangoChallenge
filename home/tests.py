from django.test import TestCase
from selenium import webdriver


class FunctionalTests(TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        # self.browser = webdriver.Firefox()

    def test_home_loads(self):
        self.browser.get('http://localhost:8000/')
        self.assertIn('The task is', self.browser.page_source)

    def tearDown(self):
        self.browser.quit()
