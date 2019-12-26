from django.test import TestCase
from selenium import webdriver
from .models import Card
from .forms import CardForm

VALID_CARD_NAME = 'ABC Bank'
VALID_CARD_NUMBER = 'GR96 0810 0010 0000 0123 4567 890'


class FunctionalTests(TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        # self.browser = webdriver.Firefox()

    def test_home_loads(self):
        self.browser.get('http://localhost:8000/cards')
        self.assertIn('Add a new card', self.browser.page_source)

    def tearDown(self):
        self.browser.quit()


class UnitTest(TestCase):
    def test_add_a_card(self):
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
