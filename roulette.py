import random
from abc import ABCMeta, abstractmethod


class Roulette():
    def __init__(self, strategy):
        self.ranges = self.create_ranges()
        self.strategy = strategy

    def spin(self):
        spin_position = random.randint(1, 38)
        returned_value = 0 - self.strategy.dollars_per_spin

        if spin_position in self.strategy.inner_bet_map:
            for bet in self.strategy.inner_bet_map[spin_position]:
                returned_value += bet.bet_return

        for bet in self.strategy.outside_bets:
            for number in bet.numbers:
                if number == spin_position:
                    returned_value += bet.bet_return

        return returned_value

    def play(self, num_trips):
        trips_to_tl = []
        for i in range(0, num_trips):
            trips_to_tl.append(self.head_to_tl())

        percent_returns = self.initialize_returns_map()

        # start of non-checked changes
        max_winnings = 0
        total_omgs = 0
        sum_of_omgs = 0

        for trip_to_tl in trips_to_tl:
            percent_return = trip_to_tl.result / float(self.strategy.starting_balance)
            if trip_to_tl.result > max_winnings:
                max_winnings = trip_to_tl.result
            total_omgs += trip_to_tl.omgs
            sum_of_omgs += trip_to_tl.omg_total

            self.add_total_to_ranges(percent_returns, self.ranges, percent_return)

        chances_of_losing_money = 0
        chances_of_breaking_even = 0
        chances_of_doubling = 0
        chances_of_winning = 0

        for r in self.ranges:
            percent_of_pot = percent_returns[r.label] / float(num_trips)
            if r.min < .9:
                chances_of_losing_money += percent_of_pot
            if r.min >= 1.1:
                chances_of_winning += percent_of_pot
            if r.min >= 2:
                chances_of_doubling += percent_of_pot
            if r.label == "-10+10%":
                chances_of_breaking_even = percent_of_pot
            print(r.label + " = " + str(percent_returns[r.label]) + "; {:.2%}".format(percent_of_pot))

        print("")
        print("Best trip to Turtle lake results in: " + str(max_winnings))
        print("")
        print("Chances of losing money: {:.2%}".format(chances_of_losing_money))
        print("Chances of breaking even: {:.2%}".format(chances_of_breaking_even))
        print("Chances of winning: {:.2%}".format(chances_of_winning))
        print("Chances of doubling: {:.2%}".format(chances_of_doubling))
        if total_omgs > 0:
            print("Average OMG Moments: {:.2}".format(total_omgs / float(num_trips)) + " with an average OMG payout of $" + str(sum_of_omgs / float(total_omgs)))

    def initialize_returns_map(self):
        range_map = {}
        for r in self.ranges:
            range_map[r.label] = 0

        return range_map

    def head_to_tl(self):
        current_balance = self.strategy.starting_balance
        spins = 0
        omgs = 0
        sum_of_omgs = 0

        for j in range(60):
            spins = j + 1
            dollar_adjustment = self.spin()
            current_balance += dollar_adjustment
            if dollar_adjustment >= 5 * self.strategy.dollars_per_spin:
                omgs += 1
                sum_of_omgs += dollar_adjustment
            if current_balance < self.strategy.dollars_per_spin: # current_balance > 2 * self.strategy.starting_balance:
                break

        return NightAtTL(spins, current_balance, omgs, sum_of_omgs)

    def add_total_to_ranges(self, pct_returns, all_ranges, result):
        bucketed = False
        for r in all_ranges:
            if r.min <= result < r.max:
                pct_returns[r.label] = pct_returns[r.label] + 1
                bucketed = True
        if not bucketed:
            print("Did not bucket: " + str(result))

    def create_ranges(self):
        ranges = []
        ranges.append(Range("-100-90%", 0, .1))
        ranges.append(Range("-90-80%", .1, .2))
        ranges.append(Range("-80-70%", .2, .3))
        ranges.append(Range("-70-60%", .3, .4))
        ranges.append(Range("-60-50%", .4, .5))
        ranges.append(Range("-50-40%", .5, .6))
        ranges.append(Range("-40-30%", .6, .7))
        ranges.append(Range("-30-20%", .7, .8))
        ranges.append(Range("-20-10%", .8, .9))
        ranges.append(Range("-10+10%", .9, 1.1))
        ranges.append(Range("10-20%", 1.1, 1.2))
        ranges.append(Range("20-30%", 1.2, 1.3))
        ranges.append(Range("30-40%", 1.3, 1.4))
        ranges.append(Range("40-50%", 1.4, 1.5))
        ranges.append(Range("50-60%", 1.5, 1.6))
        ranges.append(Range("60-70%", 1.6, 1.7))
        ranges.append(Range("70-80%", 1.7, 1.8))
        ranges.append(Range("80-90%", 1.8, 1.9))
        ranges.append(Range("90-100%", 1.9, 2))
        ranges.append(Range("100-120%", 2, 2.2))
        ranges.append(Range("120-150%", 2.2, 2.5))
        ranges.append(Range("150-200%", 2.5, 3))
        ranges.append(Range("200-300%", 3, 4))
        ranges.append(Range("300%+", 4, 1000))

        return ranges


class NightAtTL():
    def __init__(self, spins, result, omg_moments, omg_total):
        self.spins = spins
        self.result = result
        self.omgs = omg_moments
        self.omg_total = omg_total


class RouletteStrategy():
    def __init__(self, insides, outsides, num_spins, starting_balance):
        self.inside_bets = insides
        self.outside_bets = outsides
        self.num_spins = num_spins
        self.starting_balance = starting_balance
        self.dollars_per_spin = self.compute_dollars_per_spin(self.inside_bets, self.outside_bets)
        self.inner_bet_map = self.generate_inside_bet_map(self.inside_bets)

    def compute_dollars_per_spin(self, inner_bets, outer_bets):
        total_dps = len(inner_bets)
        for outer_bet in outer_bets:
            total_dps += outer_bet.num_bets

        print("Each spin costs $" + str(total_dps))
        return total_dps

    def generate_inside_bet_map(self, inner_bet_list):
        inner_bet_map = {}

        for bet in inner_bet_list:
            for num in bet.numbers:
                bet_list = inner_bet_map.get(num, [])
                bet_list.append(bet)
                inner_bet_map[num] = bet_list

        return inner_bet_map


class Range():
    def __init__(self, label, min_val, max_val):
        self.label = label
        self.min = min_val
        self.max = max_val


# The bet class and its subclasses
class Bet():
    __metaclass__ = ABCMeta

    @abstractmethod
    def compute_bet_return(self): pass


class OutsideBet(Bet):
    def __init__(self, dollar_value, numbers):
        self.num_bets = dollar_value
        self.numbers = numbers
        self.bet_return = self.compute_return(dollar_value, numbers)

    def compute_bet_return(self):
        split_across = len(self.numbers)
        if split_across == 12:
            bet_return = 3
        elif split_across == 18:
            bet_return = 2

        return bet_return * self.num_bets


class InsideBet(Bet):
    def __init__(self, numbers):
        self.numbers = numbers
        self.bet_return = self.compute_bet_return()

    def compute_bet_return(self):
        split_across = len(self.numbers)
        bet_return = 0
        if split_across == 1:
            bet_return = 36
        elif split_across == 2:
            bet_return = 18
        elif split_across == 3:
            bet_return = 12
        elif split_across == 4:
            bet_return = 9
        elif split_across == 5:
            bet_return = 7
        elif split_across == 6:
            bet_return = 6
        elif split_across == 12:
            bet_return = 3
        elif split_across == 18:
            bet_return = 2

        return bet_return


if __name__ == "__main__":
    print("whatever")

    inners = []
    inners.extend([InsideBet([17]), InsideBet([16, 17, 13, 14]), InsideBet([17, 18, 14, 15]), InsideBet([17, 20, 16, 19]), InsideBet([17, 20, 18, 21])])
    inners.extend([InsideBet([22, 23, 25, 26]), InsideBet([23, 24, 26, 27]), InsideBet([25, 26, 28, 29]), InsideBet([26, 27, 29, 30]), InsideBet([26])])

    outers = []
    rs = RouletteStrategy(inners, outers, 60, 300)

    r = Roulette(rs)
    r.play(100000)