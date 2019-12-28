from django.test import TestCase
from selenium import webdriver
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from faker import Faker
import json
from .models import UserAddress

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
    def post_address_minimal_data(self, user=None, name=None,
                                  street_address=None, city=None):
        response = self.client.post('/address', data={
                'user': user or self.user,
                'name': name or fake.name(),
                'street_address': street_address or fake.street_name(),
                'city': city or fake.city(),
            })
        return response

    def post_address(self, data):
        response = self.client.post('/address', data)
        return response

    def test_address_post_request_require_login(self):
        response = self.post_address_minimal_data()
        self.assertNotEqual(response.status_code, 200)
        self.login()
        response = self.post_address_minimal_data()
        self.assertEqual(response.status_code, 200)

    def test_address_post_request_add_address_to_page(self):
        self.login()
        self.client.get('/address')
        temp_name = fake.name()
        self.post_address_minimal_data(name=temp_name)
        response = self.client.get('/address')
        self.assertContains(response, temp_name)

    def test_address_run_objective_samples(self):
        self.login()

        """
            This test task related. We are using single test
            because of their inter-depency
            We will try to add or update the logged in user address.
            Form is save or updated as user types in the form, so requests are
            ajax and responses are JsonResponse object.

            add1 = UserAddress(name="Max", city="Giventown")
            add2 = UserAddress(
                    name="Max Mustermann", street_address="Randomstreet",
                    city="Giventown")
            add3 = UserAddress(
                    name="Max Mustermann", street_address="456 Randomstreet",
                    city="Giventown")
            add4 = UserAddress(
                    name="Max Mustermann", street_address="789 Otherstreet",
                    city="Giventown", country="NL")
        """

        # add1
        def bad_address():
            add1 = UserAddress(name="Max", city="Giventown")
            add1.full_clean()

        def bad_post():
            self.client.post('/address', {
                'name': "Max",
                'city': "Giventown",
            })
        self.assertRaises(ValidationError, bad_post)
        self.assertRaises(ValidationError, bad_address)

        # add2
        response = self.post_address(data={
            'name': "Max Mustermann",
            'city': "Giventown",
            'street_address': "Randomstreet",
            'request_type': "ajax",
            'changing_field': "street_address",
            'changing_value': "Randomstreet",
        })
        status = json.loads(response.content)['status']
        self.assertEqual(status, 'created')
        self.assertEqual(response.status_code, 200)

        # add3
        response = self.client.post('/address', data={
            'name': "Max Mustermann",
            'city': "Giventown",
            'street_address': "456 Randomstreet",
            'request_type': "ajax",
            'changing_field': "street_address",
            'changing_value': "456 Randomstreet",
        })
        status = json.loads(response.content)['status']
        self.assertEqual(status, 'updated')
        self.assertEqual(response.status_code, 200)

        # add4
        response = self.client.post('/address', data={
            'name': "Max Mustermann",
            'city': "Giventown",
            'street_address': "789 Randomstreet",
            'country': "NL",
            'request_type': "ajax",
            'changing_field': "country",
            'changing_value': "NL",
        })
        status = json.loads(response.content)['status']
        self.assertEqual(status, 'created')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.client.logout()
