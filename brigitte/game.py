from brigitte.card import Card
from brigitte.deck import Deck
from brigitte.player import Player
from brigitte.commands.pile import add_cards


class Game(object):
    def __init__(self):
        self._active_players = []
        self._pile = []
        self._removed_cards = []
        self._winners = []
        self._stock = Deck().cards
        self._game_over = False
        self._current_player = None

    @property
    def active_players(self):
        return self._active_players

    @property
    def pile(self):
        return self._pile

    @property
    def removed_cards(self):
        return self._removed_cards

    @property
    def winners(self):
        return self._winners

    @property
    def stock(self):
        return self._stock

    @property
    def current_player(self):
        return self._current_player

    @property
    def game_over(self):
        return self._game_over

    def start_new_game(self, players, player_name_key=None, player_id_key=None):
        if player_name_key and player_id_key:
            for player_dict in players:
                self._active_players.append(Player(player_dict[player_name_key], player_dict[player_id_key]))
        else:
            for player_name in players:
                self._active_players.append(Player(player_name))

        self.__deal_cards()

        return self

    def play(self):
        if not all(active_player.is_ready for active_player in self._active_players):
            return False
        if self._current_player:
            return self._current_player

        self._current_player = min(
            self._active_players,
            key=lambda active_player: min(
                active_player.hand, key=lambda hand_card: hand_card.order_value
            )
        )
        return self._current_player

    def throw_cards(self, actor, thrown_cards):
        if actor != self._current_player:
            return False
        if not add_cards(actor, thrown_cards, self.pile, self._removed_cards):
            return False

        self.__take_cards(actor)
        self.__take_visible_cards(actor)
        self.__player_won(actor)
        self.__select_next_player()

        return True

    def take_cards_from_pile(self, actor):
        if actor != self._current_player:
            return False

        actor.hand.extend(self._pile)
        actor.sort_hand()
        self._pile.clear()

        if not self._game_over:
            self.__select_next_player(True)

    def take_blind_card(self, actor, blind_card_index):
        if actor != self._current_player:
            return False
        if self._stock:
            return False
        if actor.visible_cards:
            return False
        if actor.hand:
            return False

        actor.pull_blind_card(blind_card_index)

    def to_dict(self):
        return {
            'active_players': list(map(lambda active_player: active_player.to_dict(), self._active_players)),
            'stock': list(map(lambda stock_card: stock_card.to_dict(), self._stock)),
            'pile': list(map(lambda pile_card: pile_card.to_dict(), self._pile)),
            'removed_cards': list(map(lambda removed_card: removed_card.to_dict(), self._removed_cards)),
            'current_player': self._current_player.to_dict(),
            'winners': list(map(lambda winner: winner.to_dict(), self._winners)),
            'game_over': self._game_over
        }

    @classmethod
    def from_dict(cls, game_dict):
        game = cls()
        game._active_players = list(
            map(lambda player_dict: Player.from_dict(player_dict), game_dict['active_players']))
        game._stock = list(map(lambda card_dict: Card.from_dict(card_dict), game_dict['stock']))
        game._pile = list(map(lambda card_dict: Card.from_dict(card_dict), game_dict['pile']))
        game._removed_cards = list(map(lambda card_dict: Card.from_dict(card_dict), game_dict['removed_cards']))
        game._current_player = Player.from_dict(game_dict['current_player'])
        game._winners = list(map(lambda player_dict: Player.from_dict(player_dict), game_dict['winners']))
        game._game_over = game_dict['game_over']

    def __deal_cards(self):
        for active_player in self._active_players:
            active_player.blind_cards.extend(self._stock[-3:])
            del self._stock[-3:]
            active_player.visible_cards.extend(self._stock[-3:])
            del self._stock[-3:]
            active_player.hand.extend(self._stock[-3:])
            del self._stock[-3:]

    def __take_cards(self, actor):
        if not self._stock:
            return None
        if len(actor.hand) >= 3:
            return None

        amount_of_cards_to_take = (len(actor.hand) - 3)
        actor.hand.extend(self._stock[amount_of_cards_to_take:])
        del self._stock[amount_of_cards_to_take:]
        actor.sort_hand()

    def __take_visible_cards(self, actor):
        if self._stock:
            return None
        if actor.hand:
            return None
        if not actor.visible_cards:
            return None

        actor.hand.extend(actor.visible_cards)
        actor.visible_cards.clear()
        actor.sort_hand()

    def __select_next_player(self, force=False):
        if self._game_over:
            return None
        if not force and self.__player_can_throw_again(self._current_player):
            return None

        current_player_index = self._active_players.index(self._current_player)
        next_player_index = (current_player_index + 1) % len(self._active_players)

        self._current_player = self._active_players[next_player_index]
        if self._current_player in self._winners:
            self.__select_next_player()

    def __player_can_throw_again(self, actor):
        if actor in self._winners:
            return False

        return len(self._pile) == 0

    def __player_won(self, actor):
        if actor in self._winners:
            return None
        if not list(filter(None, actor.blind_cards)):
            return None
        if actor.hand:
            return None

        self._winners.append(actor)
        self.__verify_and_set_game_over()

    def __verify_and_set_game_over(self):
        remaining_players = list(filter(lambda p: p not in self._winners, self._active_players))
        if len(remaining_players) > 1:
            return None

        if remaining_players[0]:
            self._winners.append(remaining_players[0])

        self._game_over = True
