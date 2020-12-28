from typing import List, Any

import player
import deck
import commands.pile


class Game(object):
    def __init__(self):
        self._active_players = []
        self._pile = []
        self._removed_cards = []
        self._winners = []
        self._cards = deck.Deck().cards
        self._game_over = False
        self._current_player = None

    def start_new_game(self, players, player_name_key=None, player_id_key=None):
        if player_name_key and player_id_key:
            for player_dict in players:
                self._active_players.append(player.Player(player_dict[player_name_key], player_dict[player_id_key]))
        else:
            for player_name in players:
                self._active_players.append(player_name)

        self.__deal_cards()

        return self

    def play(self):
        if not all(player.is_ready for player in self._active_players): return False
        if self._current_player: return self._current_player

        self._current_player = min(self._active_players, key=lambda p: min(p.hand, key=lambda c: c.order_value))
        return self._current_player

    def throw_cards(self, player, thrown_cards):
        if player != self._current_player: return False
        if not commands.pile.add_cards(player, thrown_cards, self._removed_cards): return False

        self.__take_cards(player)
        self.__take_visible_cards(player)
        self.__player_won(player)
        self.__select_next_player()

        return True

    def take_cards_from_pile(self, player):
        if player != self._current_player: return False

        player.hand.extend(self._pile)
        player.sort_hand()
        self._pile.clear()

        if not self._game_over: self.__select_next_player(True)

    def take_blind_card(self, player, blind_card_index):
        if player != self._current_player: return False
        if self._cards: return False
        if player.visible_cards: return False
        if player.hand: return False

        player.pull_blind_card(blind_card_index)

    def to_dict(self):
        return {
            'active_players': list(map(lambda player: player.to_dict(), self._active_players)),
            'cards': list(map(lambda card: card.to_dict(), self._cards)),
            'pile': list(map(lambda card: card.to_dict(), self._pile)),
            'removed_cards': list(map(lambda card: card.to_dict(), self._removed_cards)),
            'current_player': self._current_player.to_dict(),
            'winners': list(map(lambda player: player.to_dict(), self._winners)),
            'game_over': self._game_over
        }

    def __deal_cards(self):
        for player in self._active_players:
            player.blind_cards.extend(self._cards[-3:])
            del self._cards[-3:]
            player.visible_cards.extend(self._cards[-3:])
            del self._cards[-3:]
            player.hand.extend(self._cards[-3:])
            del self._cards[-3:]

    def __take_cards(self, player):
        if not self._cards: return None
        if len(player.hand) >= 3: return None

        amount_of_cards_to_take = (len(player.hand) - 3)
        player.hand.extend(self._cards[amount_of_cards_to_take:])
        del self._cards[amount_of_cards_to_take:]
        player.sort_hand()

    def __take_visible_cards(self, player):
        if self._cards: return None
        if player.hand: return None
        if not player.visible_cards: return None

        player.hand.extend(player.visible_cards)
        player.visible_cards.clear()
        player.sort_hand()

    def __select_next_player(self, force=False):
        if self._game_over: return None
        if not force and self.__player_can_throw_again(self._current_player): return None

        current_player_index = self._active_players.index(self._current_player)
        next_player_index = (current_player_index + 1) % len(self._active_players)

        self._current_player = self._active_players[next_player_index]
        if self._current_player in self._winners: self.select_next_player()

    def __player_can_throw_again(self, player):
        if player in self._winners: return False

        return len(self._pile) == 0

    def __player_won(self, player):
        if player in self._winners: return None
        if not list(filter(None, player.blind_cards)): return None
        if player.hand: return None

        self._winners.append(player)
        self.__verify_and_set_game_over()

    def __verify_and_set_game_over(self):
        remaining_players = filter(lambda p: p not in self._winners, self._active_players)
        if len(remaining_players) > 1: return None

        if remaining_players[0]:self._winners.append(remaining_players[0])
        self._game_over = True

