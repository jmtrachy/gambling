from abc import ABCMeta, abstractmethod

class Hand(object):
    __metaclass__ = ABCMeta

    def __init__(self, first_card):
        self.up_card = first_card
        self.cards = [self.up_card]

    @abstractmethod
    def determine_action(self, hand):
        pass


class DealerHand(Hand):
    def determine_action(self, hand):
        print(str(hand))


class PlayerHand(Hand):
    def determine_action(self, hand):
        print(str(hand))