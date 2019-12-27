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

    def test_address_page_requires_login(self):
        self.browser.get('http://localhost:8000/address')
        self.assertIn('Need an existing user first', self.browser.page_source)

    def tearDown(self):
        self.browser.quit()


class UnitTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testuser')
        self.user.save()

    def login(self):
        self.client.login(username='testuser', password='testuser')

    def test_address_minimal_address_can_be_saved(self):
        address_count = UserAddress.objects.count()
        address = UserAddress(
            user=self.user,
            name=fake.name(),
            street_address=fake.street_name(),
            city=fake.city())
        address.save()
        self.assertEqual(UserAddress.objects.count(), address_count + 1)

    def post_valid_data(self):
        response = self.client.post('/address', data={
                'user': self.user,
                'name': fake.name(),
                'street_address': fake.street_name(),
                'city': fake.city(),
            })
        return response

    def test_address_post_request_require_login(self):
        response = self.post_valid_data()
        self.assertNotEqual(response.status_code, 200)
        self.login()
        response = self.post_valid_data()
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.client.logout()
