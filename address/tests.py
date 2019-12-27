from django.test import TestCase
from selenium import webdriver
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
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

    # By default post valid data
    def post_address_data(self, user=None, name=None,
                          street_address=None, city=None):
        response = self.client.post('/address', data={
                'user': user or self.user,
                'name': name or fake.name(),
                'street_address': street_address or fake.street_name(),
                'city': city or fake.city(),
            })
        return response

    def test_address_post_request_require_login(self):
        response = self.post_address_data()
        self.assertNotEqual(response.status_code, 200)
        self.login()
        response = self.post_address_data()
        self.assertEqual(response.status_code, 200)

    def test_address_post_request_add_address_to_page(self):
        self.login()
        self.client.get('/address')
        temp_name = fake.name()
        self.post_address_data(name=temp_name)
        response = self.client.get('/address')
        self.assertContains(response, temp_name)

    def test_address_auto_update_or_add_address_with_ajax(self):
        # add1 = UserAddress(name="Max", city="Giventown")
        # add2 = UserAddress(
        #           name="Max Mustermann", street_address="Randomstreet",
        #           city="Giventown")
        # add3 = UserAddress(
        #           name="Max Mustermann", street_address="456 Randomstreet",
        #           city="Giventown")
        # add4 = UserAddress(
        #           name="Max Mustermann", street_address="789 Otherstreet",
        #           city="Giventown", country="NL")

        self.login()
        address_count = UserAddress.objects.count()

        # add1
        def bad_address():
            add1 = UserAddress(name="Max", city="Giventown")
            add1.full_clean()
        self.assertRaises(ValidationError, bad_address)
        self.assertEqual(UserAddress.objects.count(), address_count)

        # add2
        response = self.client.post('/address', data={
            'name': "Max",
            'city': "Giventown",
            'street_address': "Randomstreet",
            'request_type': "ajax",
            'changing_field': "street_address",
            'changing_value': "Randomstreet",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(UserAddress.objects.count(), address_count + 1)

        # add3
        response = self.client.post('/address', data={
            'name': "Max",
            'city': "Giventown",
            'street_address': "456 Randomstreet",
            'request_type': "ajax",
            'changing_field': "street_address",
            'changing_value': "Randomstreet",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(UserAddress.objects.count(), address_count + 1)

        # add4
        response = self.client.post('/address', data={
            'name': "Max",
            'city': "Giventown",
            'street_address': "789 Randomstreet",
            'country': "NL",
            'request_type': "ajax",
            'changing_field': "country",
            'changing_value': "NL",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(UserAddress.objects.count(), address_count + 2)

    def tearDown(self):
        self.client.logout()
