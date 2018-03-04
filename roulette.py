import random
import time
from abc import ABCMeta, abstractmethod


class Roulette:
    @staticmethod
    def spin(strategy):
        spin_position = random.randint(1, 38)
        returned_value = 0 - strategy.dollars_per_spin

        returned_value += strategy.inside_bet_returns.get(spin_position)

        for bet in strategy.outside_bets:
            for number in bet.numbers:
                if number == spin_position:
                    returned_value += bet.bet_return

        return returned_value

    @staticmethod
    def play(strategy, num_trips=100000):
        trips_to_tl = []
        print('Heading to the casino')
        num_trips_counter = 0
        for i in range(0, num_trips):
            trips_to_tl.append(Roulette.__head_to_tl(strategy, num_trips))

            # Silly little printing
            num_trips_counter += 1
            if num_trips_counter == 10000:
                print('.', end='', flush=True)
                num_trips_counter = 0
        print('\nReturning from the casino')

        ranges = Roulette.create_ranges()
        percent_returns = Roulette.initialize_returns_map(ranges)

        # start of non-checked changes
        max_winnings = 0
        total_omgs = 0
        sum_of_omgs = 0
        total_time_at_tl = 0
        total_times_max_win = 0

        print('putting results in buckets')
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

        print('')
        for r in ranges:
            percent_of_pot = percent_returns[r.label] / float(num_trips)
            if r.min < .9:
                chances_of_losing_money += percent_of_pot
            if r.min >= 1.1:
                chances_of_winning += percent_of_pot
            if r.min >= 2:
                chances_of_doubling += percent_of_pot
            if r.label == '-10+10%':
                chances_of_breaking_even = percent_of_pot
            if percent_of_pot > 0:
                print('{} = {}; {:.2%}'.format(r.label, percent_returns[r.label], percent_of_pot))
                #print(r.label + ' = ' + str(percent_returns[r.label]) + '; {:.2%}'.format(percent_of_pot))

        print('\nBest trip to casino results in: {} - which happened {} times'.format(max_winnings, total_times_max_win))
        print('\nChances of losing money: {:.2%}'.format(chances_of_losing_money))
        print('Chances of breaking even: {:.2%}'.format(chances_of_breaking_even))
        print('Chances of winning: {:.2%}'.format(chances_of_winning))
        print('Chances of doubling: {:.2%}'.format(chances_of_doubling))
        # print('Total time at TL = ' + str(total_time_at_tl))
        # print('Average time at casino: ' + str(format(total_time_at_tl / float(num_trips))))
        # if total_omgs > 0:
        #    print('Average OMG Moments: {:.2}'.format(total_omgs / float(num_trips)) +
        #          ' with an average OMG payout of $' + str(sum_of_omgs / float(total_omgs)))

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
            dollar_adjustment = Roulette.spin(strategy)
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
                pct_returns[r.label] += 1
                bucketed = True
        if not bucketed:
            print('Did not bucket: {}'.format(result))

    @staticmethod
    def create_ranges():
        ranges = []
        ranges.append(Range('-100-90%', 0, .1))
        ranges.append(Range('-90-80%', .1, .2))
        ranges.append(Range('-80-70%', .2, .3))
        ranges.append(Range('-70-60%', .3, .4))
        ranges.append(Range('-60-50%', .4, .5))
        ranges.append(Range('-50-40%', .5, .6))
        ranges.append(Range('-40-30%', .6, .7))
        ranges.append(Range('-30-20%', .7, .8))
        ranges.append(Range('-20-10%', .8, .9))
        ranges.append(Range('-10+10%', .9, 1.1))
        ranges.append(Range('10-20%', 1.1, 1.2))
        ranges.append(Range('20-30%', 1.2, 1.3))
        ranges.append(Range('30-40%', 1.3, 1.4))
        ranges.append(Range('40-50%', 1.4, 1.5))
        ranges.append(Range('50-60%', 1.5, 1.6))
        ranges.append(Range('60-70%', 1.6, 1.7))
        ranges.append(Range('70-80%', 1.7, 1.8))
        ranges.append(Range('80-90%', 1.8, 1.9))
        ranges.append(Range('90-100%', 1.9, 2))
        ranges.append(Range('100-120%', 2, 2.2))
        ranges.append(Range('120-150%', 2.2, 2.5))
        ranges.append(Range('150-200%', 2.5, 3))
        ranges.append(Range('200-300%', 3, 4))
        ranges.append(Range('300-400%', 4, 5))
        ranges.append(Range('400-500%', 5, 6))
        ranges.append(Range('500%+', 6, 7000))

        # temporary ranges for $20 17 bets
        #ranges.append(Range('single hit', 5, 10))
        #ranges.append(Range('double hit', 10, 16))
        #ranges.append(Range('triple hit', 16, 25))
        #ranges.append(Range('quads!!!', 25, 30))
        #ranges.append(Range('ALL FIVE', 30, 50))

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

        print('Each spin costs ${}'.format(total_dps))
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
            if self.compute_inside_spin_return(num) > 0:
                print('Return for spinning a {} = {}'.format(num, self.compute_inside_spin_return(num)))

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
    def compute_bet_return(self):
        pass


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


# Adding bets to a single number. If num_bets = 5 and number = 17 then it will make a $5 on 17.
def add_bets_to_single_number(num_bets, number, bet_collection):
    for j in range(0, num_bets):
        bet_collection.append(InsideBet([number]))


# Adding bets to two numbers. If num_bets = 5, number_one = 17, and number_two = 20 it will bet $5 on
# the 17/20 split
def add_bets_to_two_numbers(num_bets, number_one, number_two, bet_collection):
    for j in range(0, num_bets):
        bet_collection.append(InsideBet([number_one, number_two]))


# Adding bets to three numbers. If num_bets = 5, number_one = 16, number_two = 17, and number_three = 18 then
# it will bet $5 on the row of 16/17/18.
def add_bets_to_three_numbers(num_bets, number_one, number_two, number_three, bet_collection):
    for j in range(0, num_bets):
        bet_collection.append(InsideBet([number_one, number_two, number_three]))


# Adding four-corner bets. If num_bets = 5, number_one = 17, number_two = 18, number_three = 20, number_four = 21
# then it will bet $5 on the corner that touches each of those four numbers.
def add_bets_to_four_numbers(num_bets, number_one, number_two, number_three, number_four, bet_collection):
    for j in range(0, num_bets):
        bet_collection.append(InsideBet([number_one, number_two, number_three, number_four]))


# Jimbob power number style bet. This bets five bets - one on the power number and one on each of its four corners
def add_jimbob_power(num_bets, power_num, corner_one, corner_two, corner_three, corner_four, corner_five, corner_six,
                     corner_seven, corner_eight, bet_collection):
    for j in range(0, num_bets):
        # Add the power number bet
        add_bets_to_single_number(1, power_num, bet_collection)
        # Add each of the other four corner bets
        add_bets_to_four_numbers(1, corner_one, corner_two, corner_four, power_num, bet_collection)
        add_bets_to_four_numbers(1, corner_two, corner_three, power_num, corner_five, bet_collection)
        add_bets_to_four_numbers(1, corner_four, power_num, corner_six, corner_seven, bet_collection)
        add_bets_to_four_numbers(1, power_num, corner_five, corner_seven, corner_eight, bet_collection)


# Convenience method for making a standard jimbob power bet
def add_jimbob_seventeen(num_bets, bet_collection):
    add_jimbob_power(num_bets, 17, 13, 14, 15, 16, 18, 19, 20, 21, bet_collection)


# Convenience method for making a standard rupp bet on jimbobs number
def add_rupp_seventeen(num_bets, bet_collection):
    add_rupp_power(num_bets, 17, 14, 16, 18, 20, bet_collection)


# Ruppinator power number style bet. This bets five bets - one on the power number and one on each of it's side splits
def add_rupp_power(num_bets, power_num, side_one, side_two, side_three, side_four, bet_collection):
    for j in range(0, num_bets):
        # Add the power number bet
        add_bets_to_single_number(1, power_num, bet_collection)
        # Add each of the other four side bets
        add_bets_to_two_numbers(1, power_num, side_one, bet_collection)
        add_bets_to_two_numbers(1, power_num, side_two, bet_collection)
        add_bets_to_two_numbers(1, power_num, side_three, bet_collection)
        add_bets_to_two_numbers(1, power_num, side_four, bet_collection)


# Convenience method for making a rupp bet on 26
def add_rupp_twosix(num_bets, bet_collection):
    add_rupp_power(num_bets, 26, 23, 25, 27, 29, bet_collection)


if __name__ == '__main__':
    start_millis = current_time_millis()

    inners = []  # Bets on the inside
    outers = []  # Bets on the outside

    # Bet 1 number all in - 5 spins - 12.5% chance of hitting
    # starting_balance = 400
    # spins = 5
    # add_bets_to_single_number(80, 17, inners)

    # Bet 2 numbers REAL hard, 4 spins - 18% chance of hitting once, 1.55% chance of hitting more than once
    # starting_balance = 400
    # spins = 4
    # add_bets_to_single_number(50, 17, inners)
    # add_bets_to_single_number(50, 20, inners)

    # Bet 3 numbers hard, 5 spins - 28.4% chance of hitting once, 5.3% chance of hitting more than once
    # starting_balance = 400
    # spins = 5
    # add_bets_to_single_number(26, 5, inners)
    # add_bets_to_single_number(27, 17, inners)
    # add_bets_to_single_number(27, 26, inners)

    # Bet 4 numbers, 4 spins - 30.1% chance of hitting once, 5.7% chance of hitting more than once
    # starting_balance = 400
    # spins = 4
    # add_bets_to_single_number(25, 5, inners)
    # add_bets_to_single_number(25, 17, inners)
    # add_bets_to_single_number(25, 26, inners)
    # add_bets_to_single_number(25, 14, inners)

    # Bet 4 numbers, traditional - 33.5% chance of hitting once, 9% chance of hitting more than once
    starting_balance = 400
    spins = 5
    add_bets_to_single_number(20, 5, inners)
    add_bets_to_single_number(20, 17, inners)
    add_bets_to_single_number(20, 26, inners)
    add_bets_to_single_number(20, 14, inners)

    # 2017 approach - 3 numbers, 5 spins - 28.4% chance of hitting once, 5.3% chance of hitting more than once
    # starting_balance = 300
    # spins = 5
    # add_bets_to_single_number(20, 14, inners)
    # add_bets_to_single_number(20, 17, inners)
    # add_bets_to_single_number(20, 20, inners)

    rs = RouletteStrategy(inners, outers, spins, starting_balance)
    Roulette.play(rs, 1000000)

    end_millis = current_time_millis()
    print('Execution took {} milliseconds.'.format(end_millis - start_millis))
