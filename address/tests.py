from django.test import TestCase
from selenium import webdriver
from django.contrib.auth.models import User
from .models import UserAddress
from faker import Faker

fake = Faker()


class FunctionalTests(TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        # self.browser = webdriver.Firefox()

    def test_cards_page_loads(self):
        self.browser.get('http://localhost:8000/address')
        self.assertIn('Address Form', self.browser.page_source)

    def tearDown(self):
        self.browser.quit()


class UnitTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testuser')

    def test_address_minimal_address_can_be_saved(self):
        address_count = UserAddress.objects.count()
        address = UserAddress(
            user=self.user,
            name=fake.name(),
            street_address=fake.street_name(),
            city=fake.city())
        address.save()
        self.assertEqual(UserAddress.objects.count(), address_count + 1)
