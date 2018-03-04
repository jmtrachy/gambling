import random
import time
from abc import ABCMeta, abstractmethod


class Roulette:
    @staticmethod
    def __spin(strategy):
        spin_position = random.randint(1, 38)
        returned_value = 0 - strategy.dollars_per_spin

        returned_value += strategy.inside_bet_returns.get(spin_position)

        for bet in strategy.outside_bets:
            for number in bet.numbers:
                if number == spin_position:
                    returned_value += bet.bet_return

        return returned_value

    @staticmethod
    def play(strategy, num_trips = 100000):
        trips_to_tl = []
        print("Heading to the casino")
        for i in range(0, num_trips):
            trips_to_tl.append(Roulette.__head_to_tl(strategy, num_trips))
        print("Returning from the casino")

        ranges = Roulette.create_ranges()
        print("initializing return maps")
        percent_returns = Roulette.initialize_returns_map(ranges)
        print("return maps initialized")

        # start of non-checked changes
        max_winnings = 0
        total_omgs = 0
        sum_of_omgs = 0
        total_time_at_tl = 0
        total_times_max_win = 0

        print("putting results in buckets")
        for trip_to_tl in trips_to_tl:
            percent_return = trip_to_tl.result / float(strategy.starting_balance)
            if trip_to_tl.result > max_winnings:
                max_winnings = trip_to_tl.result
                total_times_max_win = 1
            elif trip_to_tl.result == max_winnings:
                total_times_max_win += 1
            total_omgs += trip_to_tl.omgs
            sum_of_omgs += trip_to_tl.omg_total

            total_time_at_tl += trip_to_tl.time_at_tl
            Roulette.add_total_to_ranges(percent_returns, ranges, percent_return)

        chances_of_losing_money = 0
        chances_of_breaking_even = 0
        chances_of_doubling = 0
        chances_of_winning = 0

        print("calculating aggregate totals")
        for r in ranges:
            percent_of_pot = percent_returns[r.label] / float(num_trips)
            if r.min < .9:
                chances_of_losing_money += percent_of_pot
            if r.min >= 1.1:
                chances_of_winning += percent_of_pot
            if r.min >= 2:
                chances_of_doubling += percent_of_pot
            if r.label == "-10+10%":
                chances_of_breaking_even = percent_of_pot
            if percent_of_pot > 0:
                print(r.label + " = " + str(percent_returns[r.label]) + "; {:.2%}".format(percent_of_pot))

        print("")
        print("Best trip to Turtle lake results in: " + str(max_winnings) + " - which happened " + str(total_times_max_win) + " times")
        print("")
        print("Chances of losing money: {:.2%}".format(chances_of_losing_money))
        print("Chances of breaking even: {:.2%}".format(chances_of_breaking_even))
        print("Chances of winning: {:.2%}".format(chances_of_winning))
        print("Chances of doubling: {:.2%}".format(chances_of_doubling))
        print("Total time at TL = " + str(total_time_at_tl))
        print("Average time at casino: " + str(format(total_time_at_tl / float(num_trips))))
        if total_omgs > 0:
            print("Average OMG Moments: {:.2}".format(total_omgs / float(num_trips)) + " with an average OMG payout of $" + str(sum_of_omgs / float(total_omgs)))

        return RouletteStrategyResult(trips_to_tl, max_winnings)

    @staticmethod
    def initialize_returns_map(ranges):
        range_map = {}
        for r in ranges:
            range_map[r.label] = 0

        return range_map

    @staticmethod
    def __head_to_tl(strategy, num_trips):
        start_head_to_tl_timer = current_time_millis()
        current_balance = strategy.starting_balance
        spins = 0
        omgs = 0
        sum_of_omgs = 0

        for j in range(strategy.num_spins):
            spins = j + 1
            dollar_adjustment = Roulette.__spin(strategy)
            current_balance += dollar_adjustment
            if dollar_adjustment >= 5 * strategy.dollars_per_spin:
                omgs += 1
                sum_of_omgs += dollar_adjustment
            if current_balance < strategy.dollars_per_spin: # current_balance > 2 * self.strategy.starting_balance:
                break

        end_head_to_tl_timer = current_time_millis()
        return NightAtTL(spins, current_balance, omgs, sum_of_omgs, end_head_to_tl_timer - start_head_to_tl_timer)

    @staticmethod
    def add_total_to_ranges(pct_returns, all_ranges, result):
        bucketed = False
        for r in all_ranges:
            if r.min <= result < r.max:
                pct_returns[r.label] = pct_returns[r.label] + 1
                bucketed = True
        if not bucketed:
            print("Did not bucket: " + str(result))

    @staticmethod
    def create_ranges():
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
        ranges.append(Range("300-400%", 4, 5))
        ranges.append(Range("400-500%", 5, 6))
        ranges.append(Range("500%+", 6, 7000))

        # temporary ranges for $20 17 bets
        #ranges.append(Range("single hit", 5, 10))
        #ranges.append(Range("double hit", 10, 16))
        #ranges.append(Range("triple hit", 16, 25))
        #ranges.append(Range("quads!!!", 25, 30))
        #ranges.append(Range("ALL FIVE", 30, 50))

        return ranges


class NightAtTL:
    def __init__(self, spins, result, omg_moments, omg_total, time_at_tl):
        self.spins = spins
        self.result = result
        self.omgs = omg_moments
        self.omg_total = omg_total
        self.time_at_tl = time_at_tl


class RouletteStrategy:
    def __init__(self, insides, outsides, num_spins, starting_balance):
        self.inside_bets = insides
        self.outside_bets = outsides
        self.num_spins = num_spins
        self.starting_balance = starting_balance
        self.dollars_per_spin = self.compute_dollars_per_spin()
        self.inner_bet_map = self.generate_inside_bet_map()
        self.inside_bet_returns = self.generate_inside_bet_returns()

    def compute_dollars_per_spin(self):
        total_dps = len(self.inside_bets)
        for outer_bet in self.outside_bets:
            total_dps += outer_bet.num_bets

        print("Each spin costs $" + str(total_dps))
        return total_dps

    def generate_inside_bet_map(self):
        inner_bet_map = {}

        for bet in self.inside_bets:
            for num in bet.numbers:
                bet_list = inner_bet_map.get(num, [])
                bet_list.append(bet)
                inner_bet_map[num] = bet_list

        return inner_bet_map

    def generate_inside_bet_returns(self):
        inside_bet_returns = {}
        for num in range(1, 39):
            inside_bet_returns[num] = self.compute_inside_spin_return(num)
            print("Return for spinning a " + str(num) + " = " + str(self.compute_inside_spin_return(num)))

        return inside_bet_returns

    def compute_inside_spin_return(self, spin_position):
        returned_value = 0
        if spin_position in self.inner_bet_map:
            for bet in self.inner_bet_map[spin_position]:
                returned_value += bet.bet_return

        return returned_value


class RouletteStrategyResult:
    def __init__(self, trips_to_tl, max_winnings):
        self.trips_to_tl = trips_to_tl
        self.max_winnings = max_winnings


class Range:
    def __init__(self, label, min_val, max_val):
        self.label = label
        self.min = min_val
        self.max = max_val


# The bet class and its subclasses
class Bet:
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


def current_time_millis():
    return int(round(time.time() * 1000))


def add_bets_to_single_number(num_bets, number, bet_collection):
    for j in range(0, num_bets):
        bet_collection.append(InsideBet([number]))


#def add_bets_to_two_numbers(num_bets)

if __name__ == "__main__":
    start_millis = current_time_millis()

    inners = []

    bet_size = 50
    # $20 on 17
    add_bets_to_single_number(bet_size, 17, inners)
    # $20 on 20
    add_bets_to_single_number(bet_size, 26, inners)
    # $20 on 20
    #add_bets_to_single_number(bet_size, 5, inners)
    # $20 on 20
    #add_bets_to_single_number(bet_size, 14, inners)


    # inners.extend([InsideBet([17]), InsideBet([16, 17, 13, 14]), InsideBet([17, 18, 14, 15]), InsideBet([17, 20, 16, 19]), InsideBet([17, 20, 18, 21])])
    # inners.extend([InsideBet([22, 23, 25, 26]), InsideBet([23, 24, 26, 27]), InsideBet([25, 26, 28, 29]), InsideBet([26, 27, 29, 30]), InsideBet([26])])
    # inners.extend([InsideBet([26]), InsideBet([22, 23, 25, 26]), InsideBet([23, 24, 26, 27]), InsideBet([25, 26, 28, 29]), InsideBet([26, 27, 29, 30]), InsideBet([26, 23]), InsideBet([26, 25]), InsideBet([26, 27]), InsideBet([26, 29])])


    outers = []
    rs = RouletteStrategy(inners, outers, 4, 400)
    Roulette.play(rs, 1000000)

    end_millis = current_time_millis()
    print("Execution took " + str(end_millis - start_millis) + " milliseconds.")
