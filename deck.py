import random
from enum import Enum

Suit = Enum('Suit', 'Club Spade Diamond Heart')


class Card():
    def __init__(self, suit, name, value, is_ace=False):
        self.suit = suit
        self.name = name
        self.value = value
        self.is_ace = is_ace


class Deck():
    @staticmethod
    def create_deck():
        return Deck()

    def __init__(self):
        cards = []
        for s in Suit:
            cards.append(Card(s, 'Ace', 1, True))
            cards.append(Card(s, 'Deuce', 2))
            cards.append(Card(s, 'Three', 3))
            cards.append(Card(s, 'Four', 4))
            cards.append(Card(s, 'Five', 5))
            cards.append(Card(s, 'Six', 6))
            cards.append(Card(s, 'Seven', 7))
            cards.append(Card(s, 'Eight', 8))
            cards.append(Card(s, 'Nine', 9))
            cards.append(Card(s, 'Ten', 10))
            cards.append(Card(s, 'Jack', 10))
            cards.append(Card(s, 'Queen', 10))
            cards.append(Card(s, 'King', 10))

        self.cards = cards

    def shuffle(self):
        shuffled_cards = []
        for c in self.cards:
            random_location = random.randint(0, len(shuffled_cards))
            shuffled_cards.insert(random_location, c)

        self.cards = shuffled_cards


class Shoe():
    @staticmethod
    def create_shoe(num_decks=6):
        cards = []
        for j in range(num_decks):
            deck = Deck.create_deck()
            for c in deck.cards:
                random_location = random.randint(0, len(cards))
                cards.insert(random_location, c)

        return Shoe(cards)

    def __init__(self, cards):
        self.cards = cards

if __name__ == "__main__":
    shoe = Shoe.create_shoe(1)
    for c in shoe.cards:
        print(c.name + " of " + str(c.suit.name) + "; value=" + str(c.value))