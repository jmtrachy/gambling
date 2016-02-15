__author__ = 'jamest'

import random


class Range():
    def __init__(self, label, min_val, max_val):
        self.label = label
        self.min = min_val
        self.max = max_val


class OutsideBet():
    def __init__(self, dollar_value, numbers):
        self.num_bets = dollar_value
        self.numbers = numbers
        self.bet_return = compute_outside_bet_return(dollar_value, numbers)


class Bet():
    def __init__(self, numbers):
        self.numbers = numbers
        self.bet_return = compute_inside_bet_return(numbers)


class NightAtTL():
    def __init__(self, spins, result, omg_moments, omg_total):
        self.spins = spins
        self.result = result
        self.omgs = omg_moments
        self.omg_total = omg_total


def compute_dollars_per_spin(inner_bets, outer_bets):
    total_dps = len(inner_bets)
    for outer_bet in outer_bets:
        total_dps += outer_bet.num_bets

    print("Each spin costs $" + str(total_dps))
    return total_dps


def play_game(balance, total_dps, inner_bets, outer_bets):
    current_balance = balance
    spins = 0
    omgs = 0
    sum_of_omgs = 0

    for j in range(60):
        spins = j + 1
        dollar_adjustment = spin(total_dps, inner_bets, outer_bets)
        current_balance += dollar_adjustment
        if dollar_adjustment >= 5 * total_dps:
            omgs += 1
            sum_of_omgs += dollar_adjustment
        if current_balance < total_dps:# or current_balance > 2 * balance:
            break

    return NightAtTL(spins, current_balance, omgs, sum_of_omgs)


def spin(dps, inner_bets, outer_bets):
    spin_position = random.randint(1, 38)
    returned_value = 0 - dps

    if spin_position in inner_bets:
        for bet in inner_bets[spin_position]:
            returned_value += bet.bet_return

    for bet in outer_bets:
        for number in bet.numbers:
            if number == spin_position:
                returned_value += bet.bet_return

    return returned_value


def generate_inside_bet_map(inner_bet_list):
    inner_bet_map = {}

    for bet in inner_bet_list:
        for num in bet.numbers:
            bet_list = inner_bet_map.get(num, [])
            bet_list.append(bet)
            inner_bet_map[num] = bet_list

    return inner_bet_map


def compute_outside_bet_return(dollar_value, numbers):
    split_across = len(numbers)
    if split_across == 12:
        bet_return = 3
    elif split_across == 18:
        bet_return = 2

    return bet_return * dollar_value


def compute_inside_bet_return(numbers):
    split_across = len(numbers)
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


def initialize_returns_map(all_ranges):
    range_map = {}
    for r in all_ranges:
        range_map[r.label] = 0

    return range_map


def add_total_to_ranges(pct_returns, all_ranges, result):
    bucketed = False
    for r in all_ranges:
        if r.min <= result < r.max:
            pct_returns[r.label] = pct_returns[r.label] + 1
            bucketed = True
    if not bucketed:
        print("Did not bucket: " + str(result))


if __name__ == "__main__":
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

    # instantiating number of bets
    inside_bets = []
    outside_bets = []
    # starting balance
    starting_balance = 300
    num_trips = 100000

    # power number 17 - james' style
    inside_bets.extend([Bet([17]), Bet([16, 17, 13, 14]), Bet([17, 18, 14, 15]), Bet([17, 20, 16, 19]), Bet([17, 20, 18, 21])])

    # power number 26 - james' style
    inside_bets.extend([Bet([22, 23, 25, 26]), Bet([23, 24, 26, 27]), Bet([25, 26, 28, 29]), Bet([26, 27, 29, 30]), Bet([26])])

    # power number 17 - chris' style
    # inside_bets.extend([Bet([17]), Bet([14, 17]), Bet([16, 17]), Bet([17, 18]), Bet([17, 20])])

    # power number 26 - chris' style
    # inside_bets.extend([Bet([26]), Bet([23, 26]), Bet([25, 26]), Bet([26, 27]), Bet([26, 29])])

    # pummel on 17/20
    # inside_bets.extend([Bet([17]), Bet([20]), Bet([17, 20]), Bet([17, 20]), Bet([16, 17, 19, 20]), Bet([13, 14, 16, 17]),
    #                 Bet([14, 15, 17, 18]), Bet([17, 18, 20, 21]), Bet([19, 20, 22, 23]), Bet([20, 21, 23, 24])])

    # inside_bets.extend([Bet([17]), Bet([17, 20]), Bet([17, 14])])

    # Single number betting
    # inside_bets.extend([Bet([17, 20])])

    # 0 on one number per line
    #inside_bets.extend([Bet([17]), Bet([17]), Bet([17]), Bet([17]), Bet([17]), Bet([17]), Bet([17]), Bet([17]), Bet([17]), Bet([17]),
    #                    Bet([17]), Bet([17]), Bet([17]), Bet([17]), Bet([17]), Bet([17]), Bet([17]), Bet([17]), Bet([17]), Bet([17]),
    #                    Bet([17]), Bet([17]), Bet([17]), Bet([17]), Bet([17]), Bet([17]), Bet([17]), Bet([17]), Bet([17]), Bet([17])])

    # inside_bets.extend([Bet([15]), Bet([15]), Bet([15]), Bet([15]), Bet([15]), Bet([15]), Bet([15]), Bet([15]), Bet([15]), Bet([15])])
    # inside_bets.extend([Bet([16]), Bet([16]), Bet([16]), Bet([16]), Bet([16]), Bet([16]), Bet([16]), Bet([16]), Bet([16]), Bet([16])])
    # inside_bets.extend([Bet([17]), Bet([17]), Bet([17]), Bet([17]), Bet([17]), Bet([17]), Bet([17]), Bet([17]), Bet([17]), Bet([17])])
    # inside_bets.extend([Bet([18]), Bet([18]), Bet([18]), Bet([18]), Bet([18]), Bet([18]), Bet([18]), Bet([18]), Bet([18]), Bet([18])])
    # inside_bets.extend([Bet([19]), Bet([19]), Bet([19]), Bet([19]), Bet([19]), Bet([19]), Bet([19]), Bet([19]), Bet([19]), Bet([19])])
    # inside_bets.extend([Bet([20]), Bet([20]), Bet([20]), Bet([20]), Bet([20]), Bet([20]), Bet([20]), Bet([20]), Bet([20]), Bet([20])])

    # Betting black
    # outside_bets.extend([OutsideBet(30, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 15])])

    # Single number betting with multiple dollars
    # for i in range(20):
        # inside_bets.extend([Bet([17])])

    dollars_per_spin = compute_dollars_per_spin(inside_bets, outside_bets)
    inside_bet_map = generate_inside_bet_map(inside_bets)
    trips_to_tl = []

    print("Heading to casino...")
    for i in range(0, num_trips):
        trips_to_tl.append(play_game(starting_balance, dollars_per_spin, inside_bet_map, outside_bets))
    print("Calling it a night, computing results...")

    percent_returns = initialize_returns_map(ranges)

    max_winnings = 0
    total_omgs = 0
    sum_of_omgs = 0

    for trip_to_tl in trips_to_tl:
        percent_return = trip_to_tl.result / starting_balance
        if trip_to_tl.result > max_winnings:
            max_winnings = trip_to_tl.result
        total_omgs += trip_to_tl.omgs
        sum_of_omgs += trip_to_tl.omg_total

        add_total_to_ranges(percent_returns, ranges, trip_to_tl.result / starting_balance)

    chances_of_losing_money = 0
    chances_of_breaking_even = 0
    chances_of_doubling = 0
    chances_of_winning = 0

    for r in ranges:
        percent_of_pot = percent_returns[r.label] / num_trips
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
    print("Average OMG Moments: {:.2}".format(total_omgs / num_trips) + " with an average OMG payout of $" + str(sum_of_omgs / total_omgs))