import uuid
import card


class Player(object):
    def __init__(self, name, id=None):
        self._name = name
        self._id = id or str(uuid.uuid4())
        self._hand = []
        self._blind_cards = []
        self._visible_cards = []
        self._ready = False

    def __eq__(self, other):
        return False if other is None else self.id == other.id

    def swap(self, hand_card, visible_card):
        if self.is_ready: return

        hand_card_index = self.hand.index(hand_card)
        visible_card_index = self.visible_cards.index(visible_card)
        if hand_card_index or visible_card_index: return

        self.visible_cards[visible_card_index] = hand_card
        self.hand[hand_card_index] = visible_card


    def pull_blind_card(self, index):
        if self.hand: return False
        if self.visible_cards: return False

        blind_card = self.blind_cards[index]
        if not blind_card: return False

        self.blind_cards[index] = None
        self.hand.append(blind_card)

        return True

    def sort_hand(self):
        self._hand.sort(key=lambda card: card.value)

    def throw(self, card):
        try:
            self._hand.remove(card)
            return card
        except ValueError:
            return None

    def set_ready(self):
        self.sort_hand()
        self._ready = True

    @property
    def ready(self):
        return self._ready
    is_ready = ready

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @property
    def hand(self):
        return self._hand

    @property
    def blind_cards(self):
        return self._blind_cards

    @property
    def visible_cards(self):
        return self._visible_cards

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'hand': list(map(lambda card: card.to_dict(), self.hand)),
            'blind_cards': self.blind_cards,
            'visible_cards': self.visible_cards,
            'ready': self.ready
        }

    @classmethod
    def from_dict(cls, player_dict):
        if not player_dict: return None

        player = cls(player_dict['name'], player_dict['id'])
        player._hand = list(map(lambda card_dict: card.Card.from_dict(card_dict), player_dict['hand']))
        player._blind_cards = list(map(lambda card_dict: card.Card.from_dict(card_dict), player_dict['blind_cards']))
        player._visible_cards = list(map(lambda card_dict: card.Card.from_dict(card_dict), player_dict['visible_cards']))
        player._ready = player_dict['ready']

        return player