import uuid


class Card(object):
    def __init__(self, value, sign, identifier=None):
        self._value = str(value)
        self._sign = sign
        self._id = identifier or str(uuid.uuid4())

    @property
    def value(self):
        return self._value

    @property
    def sign(self):
        return self._sign

    @property
    def id(self):
        return self._id

    def __str__(self):
        return self.value + self.sign

    def __eq__(self, other):
        return False if other is None else self.id == other.id

    def weight(self):
        card_values = {
            'J': 11,
            'Q': 12,
            'K': 13,
            'A': 14
        }

        return card_values.get(self.value) or int(self.value)

    def order_level(self):
        return 15 if self.value == '2' else self.weight()

    def to_dict(self):
        return {
            'id': self._id,
            'value': self._value,
            'sign': self._sign
        }

    @classmethod
    def from_dict(cls, card_dict):
        if not card_dict:
            return None

        return cls(card_dict['value'], card_dict['sign'], card_dict['id'])
