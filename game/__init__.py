import random


class Game:
    def __init__(self):
        self.player1 = Player("Player1", True)
        self.player2 = Player("Player2", False)
        self.turn = 1


class Player:
    def __init__(self, name, first_turn):
        self.name = name
        self.first_turn = first_turn
        self.points = 0


class PlayerHand:
    """
    Class that for player cards in a hand
    """

    def __init__(self, cards, plays_first):
        self.cards = cards
        self.plays_first = plays_first
        self.envido = self.calc_envido()
        self.flor = False
        self.played_cards = []

    def calc_envido(self):
        suits = [x["suit"] for x in self.cards]
        suits_set = set(suits)
        unique_suits = list(suits_set)

        if len(unique_suits) == 1:
            self.flor = True

        elif len(unique_suits) == 2:
            repeated_suit = [x for x in suits if suits.count(x) > 1][0]
            envido_cards = [
                x["number"] for x in self.cards if x["suit"] == repeated_suit
            ]
            envido_cards = [0 if x > 7 else x for x in envido_cards]
            return sum(envido_cards) + 20
        else:
            return max([0 if x["number"] > 7 else x["number"] for x in self.cards])


def deal_cards(deck):
    """
    Recives deck of cards, picks 6, returns 2 hands of 3
    """
    deal = random.sample(deck, 6)
    return deal[:3], deal[3:]
