from django.test import TestCase
from selenium import webdriver
import time
from faker import Faker
from .models import Card
from .forms import CardForm

VALID_CARD_NAME = 'ABC Bank'
VALID_CARD_NUMBER = 'GR96 0810 0010 0000 0123 4567 890'

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

    def test_card_form_page_submit_adds_a_card(self):
        self.browser.get('http://localhost:8000/cards')
        card_name_field = self.browser.find_element_by_id('id_card_name')
        card_number_field = self.browser.find_element_by_id('id_card_number')
        temp_card_name = fake.company()[:20] + ' Bank'
        temp_card_number = fake.iban()
        card_name_field.send_keys(temp_card_name)
        card_number_field.send_keys(temp_card_number)
        self.browser.find_element_by_class_name('card-submit').click()
        time.sleep(2)
        self.assertIn(temp_card_number, self.browser.page_source)
        self.assertIn(temp_card_name, self.browser.page_source)

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
