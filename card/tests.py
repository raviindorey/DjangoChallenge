from django.test import TestCase
from selenium import webdriver
import time
from error_report.models import Error
from django.core.exceptions import ValidationError
from faker import Faker
from .models import Card
from .forms import CardForm
from .utils import create_hyphen_string


VALID_CARD_NAME = 'ABC Bank'
VALID_CARD_NUMBER = 'GR96 0810 0010 0000 0123 4567 890'
INVALID_CARD_NUMBER = VALID_CARD_NUMBER * 2

fake = Faker()


class FunctionalTests(TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        # self.browser = webdriver.Firefox()

    def test_cards_page_loads(self):
        self.browser.get('http://localhost:8000/cards')
        self.assertIn('Add a new card', self.browser.page_source)

    def test_cards_page_has_form(self):
        self.browser.get('http://localhost:8000/cards')
        self.assertIn('card-form', self.browser.page_source)

    def submit_card_form(self):
        self.browser.get('http://localhost:8000/cards')
        card_name_field = self.browser.find_element_by_id('id_card_name')
        card_number_field = self.browser.find_element_by_id('id_card_number')
        temp_card_name = fake.company()[:20] + ' Bank'
        temp_card_number = fake.iban()
        card_name_field.send_keys(temp_card_name)
        card_number_field.send_keys(temp_card_number)
        self.browser.find_element_by_class_name('card-submit').click()

        return (temp_card_name, temp_card_number)

    def test_card_form_page_submit_adds_a_card(self):
        temp_card_name, temp_card_number = self.submit_card_form()
        table = self.browser.find_element_by_class_name('table').text
        self.assertIn(temp_card_name, table)

    def test_card_card_list_page_not_contain_card_numbers(self):
        temp_card_name_1, temp_card_number_1 = self.submit_card_form()
        temp_card_name_2, temp_card_number_2 = self.submit_card_form()
        temp_card_name_3, temp_card_number_3 = self.submit_card_form()
        time.sleep(2)
        table = self.browser.find_element_by_class_name('table').text
        self.assertNotIn(temp_card_number_1, table)
        self.assertNotIn(temp_card_number_2, table)
        self.assertNotIn(temp_card_number_3, table)

    def test_card_card_list_page__contain_card_name(self):
        temp_card_name_1, temp_card_number_1 = self.submit_card_form()
        temp_card_name_2, temp_card_number_2 = self.submit_card_form()
        temp_card_name_3, temp_card_number_3 = self.submit_card_form()
        time.sleep(2)
        table = self.browser.find_element_by_class_name('table').text
        self.assertIn(temp_card_name_1, table)
        self.assertIn(temp_card_name_2, table)
        self.assertIn(temp_card_name_3, table)

    def tearDown(self):
        self.browser.quit()


class UnitTests(TestCase):
    def test_card_add_a_card(self):
        card = Card()
        total_cards = Card.objects.count()
        card.card_name = VALID_CARD_NAME
        card.card_number = VALID_CARD_NUMBER
        card.save()
        self.assertEqual(Card.objects.count(), total_cards + 1)

    def get_card_form(self):
        return CardForm(data={
            'card_name': VALID_CARD_NAME,
            'card_number': VALID_CARD_NUMBER
            })

    def test_card_form_is_valid(self):
        card_form = self.get_card_form()
        self.assertTrue(card_form.is_valid())

    def test_card_form_submit_adds_a_card(self):
        response = self.client.post('/cards', data={
            'card_name': VALID_CARD_NAME,
            'card_number': VALID_CARD_NUMBER,
        })
        self.assertEqual(response.status_code, 200)

    def test_card_invalid_card_raise_error(self):
        def bad_card():
            invalid_card = Card(
                card_name=VALID_CARD_NAME,
                card_number=INVALID_CARD_NUMBER,
            )
            invalid_card.full_clean()
        self.assertRaises(ValidationError, bad_card)

    def bad_request(self):
        self.client.post('/cards', data={
            'card_name': VALID_CARD_NAME,
            'card_number': INVALID_CARD_NUMBER,
        })

    def raise_and_return_report_html(self):
        self.assertRaises(ValidationError, self.bad_request)
        return Error.objects.last().html

    def test_card_form_submit_does_not_add_invalid_card(self):
        self.assertRaises(ValidationError, self.bad_request)

    def test_card_card_name_present_in_error_report(self):
        report_html = self.raise_and_return_report_html()
        self.assertTrue(VALID_CARD_NAME in report_html)

    def test_card_full_card_number_not_in_error_report(self):
        report_html = self.raise_and_return_report_html()
        self.assertFalse(INVALID_CARD_NUMBER in report_html)

    def test_card_hyphenated_card_number_is_in_error_report(self):
        report_html = self.raise_and_return_report_html()
        self.assertTrue(
            create_hyphen_string(INVALID_CARD_NUMBER) in report_html
        )
