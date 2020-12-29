import unittest

from brigitte.card import Card


class TestCard(unittest.TestCase):
    value = 2
    sign = '♣'

    def test_init(self):
        card = Card(self.value, self.sign)
        self.assertEqual(card.value, str(self.value))
        self.assertEqual(card.sign, self.sign)
        self.assertIsNotNone(card.id)

    def test_str(self):
        card = Card(self.value, self.sign)

        self.assertEqual(str(card), card.value + card.sign)

    def test_eq(self):
        card = Card(self.value, self.sign)

        self.assertEqual(card, Card(self.value, self.sign, card.id))
        self.assertNotEqual(card, Card(self.value, self.sign, '123'))

    def test_weight(self):
        for value, weight in {
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            '10': 10,
            'J': 11,
            'Q': 12,
            'K': 13,
            'A': 14
        }.items():
            self.assertEqual(Card(value, self.sign).weight(), weight)

    def test_order_level(self):
        for value, order_level in {
            '2': 15,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            '10': 10,
            'J': 11,
            'Q': 12,
            'K': 13,
            'A': 14
        }.items():
            self.assertEqual(Card(value, self.sign).order_level(), order_level)

    def test_to_dict(self):
        card = Card(self.value, self.sign)
        card_dict = card.to_dict()
        self.assertEqual(card_dict['id'], card.id)
        self.assertEqual(card_dict['value'], card.value)
        self.assertEqual(card_dict['sign'], card.sign)

    def test_from_dict(self):
        card = Card(self.value, self.sign)
        card_from_dict = Card.from_dict(card.to_dict())
        self.assertEqual(card_from_dict.id, card.id)
        self.assertEqual(card_from_dict.sign, card.sign)
        self.assertEqual(card_from_dict.value, card.value)

if __name__ == '__main__':
    unittest.main()
