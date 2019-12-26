from django.test import TestCase
from selenium import webdriver
from .models import Card
from .forms import CardForm

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
        card.card_name = 'ABC Bank'
        card.card_number = VALID_CARD_NUMBER
        card.save()
        self.assertEqual(Card.objects.count(), total_cards + 1)

    def test_card_form_is_valid(self):
        card_form = CardForm(data={
            'card_name': 'ABC Bank',
            'card_number': VALID_CARD_NUMBER
            })
        self.assertTrue(card_form.is_valid())
