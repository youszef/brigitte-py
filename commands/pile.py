def add_cards(player, cards, pile, removed_cards=[]):
    if not __valid(player, cards, pile): return False

    pile.extend(cards)
    player.hand = [hand_card for hand_card in player.hand if hand_card not in cards]
    if __clear_pile(pile):
        removed_cards.extend(pile)
        pile.clear()

    return True


def __valid(player, cards, pile):
    if not all(card in player.hand for card in cards): return False
    if not len(set(map(lambda card: card.weight(), cards))) == 1: return False
    if not pile: return True
    if cards[0] in [2, 10]: return True

    return __can_put_on_card(cards[0], pile[-1])


def __can_put_on_card(top_card, down_card):
    if down_card.weight == 7: return top_card.weight <= down_card.weight

    return top_card.weight >= down_card.weight


def __clear_pile(pile):
    if pile[-1].weight == 10: return True
    if not len(pile) >= 4: return False

    return len(set(map(lambda card: card.weight(), pile[-4:]))) == 1
