import argparse
import random
from operator import attrgetter


class Card():
    def __init__(self, name, suit, value, count_value):
        self.name = name
        self.suit = suit
        self.value = value
        self.count_value = count_value


class Deck():
    def __init__(self):
        self.cards = []

        for j in range(0, 4):
            self.cards.append(Card("A", j, 1, -2))
            self.cards.append(Card("2", j, 2, 1))
            self.cards.append(Card("3", j, 3, 1))
            self.cards.append(Card("4", j, 4, 1))
            self.cards.append(Card("5", j, 5, 1))
            self.cards.append(Card("6", j, 6, -2))
            self.cards.append(Card("7", j, 7, -3))
            self.cards.append(Card("8", j, 8, -2))
            self.cards.append(Card("9", j, 9, 1))
            self.cards.append(Card("10", j, 10, 1))
            self.cards.append(Card("J", j, 10, 1))
            self.cards.append(Card("Q", j, 10, 1))
            self.cards.append(Card("K", j, 10, 1))


class Shoe():
    def __init__(self):
        self.cards = []

        for j in range(1, 6):
            deck = Deck()
            self.cards.extend(deck.cards)

        #self.count = self.determine_count()
        self.count = 0

    def determine_count(self):
        the_count = 0
        for card in self.cards:
            the_count += card.count_value

        return the_count

    def deal_card(self):
        card_to_deal = self.cards.pop(random.randint(0, len(self.cards) - 1))
        self.count += card_to_deal.count_value

        return card_to_deal


class Game():
    def __init__(self, shoe, bet_size, bankroll, vary_betting=False):
        self.shoe = shoe
        self.bet_size = bet_size
        self.bankroll = bankroll
        self.vary_betting = vary_betting

    def play(self):
        while (len(self.shoe.cards) > 52 and self.bankroll > 0):
            self.deal_hand()

        return self.bankroll

    def deal_hand(self):
        current_count = self.shoe.count
        #print("current count = " + str(current_count))
        burn_card = self.shoe.deal_card()
        #print("burn card = " + str(burn_card.name) + "; remaining count = " + str(self.shoe.count))

        card1 = self.shoe.deal_card()
        card2 = self.shoe.deal_card()
        card3 = self.shoe.deal_card()

        value = self.compute_total(card1, card2, card3)

        bet = self.compute_bet(current_count)

        change_in_stack = self.compute_winnings(value, card1, card2, card3)
        #if change_in_stack > 50:
        #    print("WOW! Just hit a " + str(change_in_stack) + " return!")
        self.bankroll += bet * change_in_stack

    def compute_bet(self, current_count):
        bet = self.bet_size
        true_count = 0
        bet_threshold = 2

        if current_count > 0 and self.vary_betting:
            decks_remaining = len(self.shoe.cards) / 52
            actual_multiplier = current_count / decks_remaining
            floor = current_count // decks_remaining

            #print("decks = " + str(decks_remaining) + "; current count = " + str(current_count) + "; mtplr = " + str(actual_multiplier))

            if actual_multiplier - floor < 0.5:
                if floor != 0.0:
                    true_count = floor
            else:
                true_count = floor + 1

        if true_count < bet_threshold and self.vary_betting:
            bet = 0
        elif true_count >= bet_threshold and self.vary_betting:
            bet = self.bet_size * (true_count - bet_threshold)

        if bet > 25:
            bet = 25

        if bet > self.bankroll:
            bet = self.bankroll

        #print("true_count = " + str(true_count) + "; bet = " + str(bet))
        return bet

    def compute_winnings(self, card_total, card1, card2, card3):
        adjustment = -1
        is_flush = card1.suit == card2.suit == card3.suit
        is_six_seven_eight = self.equals_six_seven_eight(card1, card2, card3)
        is_sevens = card1.value == 7 and card2.value == 7 and card3.value == 7

        if card_total == 19 or card_total == 20:
            adjustment = 2
        elif card_total == 21 and not is_flush:
            if is_six_seven_eight:
                adjustment = 30
            elif is_sevens:
                adjustment = 50
            else:
                adjustment = 3
        elif card_total == 21 and is_flush:
            if is_six_seven_eight:
                adjustment = 100
            elif is_sevens:
                adjustment = 200
            else:
                adjustment = 15

        return adjustment

    def equals_six_seven_eight(self, card1, card2, card3):
        contains_six = False
        contains_seven = False
        contains_eight = False

        if card1.value == 6 or card2.value == 6 or card3.value == 6:
            contains_six = True
        if card1.value == 7 or card2.value == 7 or card3.value == 7:
            contains_seven = True
        if card1.value == 8 or card2.value == 8 or card3.value == 8:
            contains_eight = True

        return contains_six and contains_seven and contains_eight

    def compute_total(self, card1, card2, card3):
        num_aces = 0
        if card1.name == "A":
            num_aces += 1
        if card2.name == "A":
            num_aces += 1
        if card3.name == "A":
            num_aces += 1

        total_value = card1.value + card2.value + card3.value
        if num_aces > 0 and total_value < 12:
            total_value += 10

        return total_value


if __name__ == "__main__":
    num_iterations = 10000
    total_bankroll = 0
    starting_bankroll = 200
    vary_betting = True
    min_bet = 5

    parser = argparse.ArgumentParser(description='Gathering arguments')
    parser.add_argument("-v", required=False, dest="vary", action="store", help="Whether to vary betting or not - default True")
    parser.add_argument("-n", required=False, dest="iterations", action="store", help="Number of shoes - default is 10000")
    parser.add_argument("-b", required=False, dest="bankroll", action="store", help="Starting bankroll - default is 200")
    args = parser.parse_args()

    if args.vary == "False":
        vary_betting = False

    if args.iterations is not None:
        num_iterations = int(args.iterations)

    if args.bankroll is not None:
        starting_bankroll = int(args.bankroll)

    num_times_losing_everything = 0
    num_times_doubling = 0

    print("analysis for starting bankroll = " + str(starting_bankroll) + "; min bet = " + str(min_bet) + "; vary betting = " + str(vary_betting) + "; " + str(num_iterations) + " shoes")

    games = []
    games_map = {}
    made_money = 0
    even_money = 0
    lost_money = 0
    for j in range(0, num_iterations):
        game = Game(Shoe(), min_bet, starting_bankroll, vary_betting)
        end_bankroll = game.play()
        games.append(game)

        if end_bankroll > starting_bankroll:
            made_money += 1
        elif end_bankroll == starting_bankroll:
            even_money += 1
        else:
            lost_money += 1

        games_key = end_bankroll
        level_to_update = 0
        if games_key in games_map:
            level_to_update = games_map[games_key]

        level_to_update += 1
        games_map[games_key] = level_to_update

        if end_bankroll > 2 * starting_bankroll:
            num_times_doubling += 1
        elif end_bankroll == 0:
            num_times_losing_everything += 1

        total_bankroll += end_bankroll
        if j % 1000 == 0:
            print('.', end="", flush=True)

    games = sorted(games, key=attrgetter('bankroll'), reverse=True)
    print("avg ending bankroll = " + str(total_bankroll / num_iterations) + ". median = " + str(games[num_iterations // 2].bankroll) + ". Lost everything " + str(num_times_losing_everything) + " times and doubled up " + str(num_times_doubling))

    games_aggregate = sorted(games_map.keys())
    for key in games_aggregate:
        print("Ended with $" + str(key) + " dollars after a single shoe " + str(games_map[key]) + " times out of " + str(num_iterations) + " shoes.")

    print("Made money on " + str(made_money) + " out of " + str(num_iterations) + " shoes.")
    print("Even money on " + str(even_money) + " out of " + str(num_iterations) + " shoes.")
    print("Lost money on " + str(lost_money) + " out of " + str(num_iterations) + " shoes.")