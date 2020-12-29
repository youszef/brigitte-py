from brigitte import card
import random


class Deck(object):
    PREFIX = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    SIGNS = ['♣', '♦', '♥', '♠']

    def __init__(self):
        self._cards = []
        for value in self.PREFIX:
            for sign in self.SIGNS:
                self._cards.append(card.Card(value, sign))

        random.shuffle(self._cards)

    @property
    def cards(self):
        return self._cards
