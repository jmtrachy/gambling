import cgi
import time
import roulette
import webapp2

from google.appengine.ext import ndb


_MAIN_PAGE_HTML = """\
<!DOCTYPE html>
  <body>
    <form action="/gambling/roulette/driveToTL" method="post">
      <div><label for="numTripsToTL">Number of trips to TL</label><input type="number" name="numTripsToTL" id="numTripsToTL" value="1" max="1000000"/></div>
      <div><label for="numSpins">Number of spins</label><input type="number" name="numSpins" id="numSpins" step="10" value="60" max="150"/></div>
      <div><label for="dollarsPerChip">Dollars per chip</label><input type="number" name="dollarsPerChip" id="dollarsPerChip" value="1" max="25"/></div>
      <div><label for="startingBalance">Starting Balance</label><input type="number" name="startingBalance" id="startingBalance" max="10000" value="300"/></div>
      <div><label for="insideBets">Inside Bets - format is pipe (|) delimited list of comma separated values.  For example: 17|20|17,20 means one chip on 17, one on 20 and one on both</label><input type="text" name="insideBets" id="insideBets" value="17|20|17,20"/></div>
      <div><input type="submit" value="Let's go to Turtle Lake!"></div>
    </form>
  </body>
</html>
"""

saved_betting_numbers = {
    "james_traditional_power":"17|16,17,13,14|14,15,17,18|16,17,19,20|17,18,20,21|26|22,23,25,26|23,24,26,27|25,26,28,29|26,27,29,30"
}

class RouletteController(webapp2.RequestHandler):
    def get(self):

        self.generate_response(_MAIN_PAGE_HTML)

    def post(self):
        # Timing this to find out the slowness
        start_millis = current_time_millis()

        num_trips_to_tl = int(cgi.escape(self.request.get('numTripsToTL')))
        num_spins = int(cgi.escape(self.request.get('numSpins')))
        dollars_per_spin = cgi.escape(self.request.get('dollarsPerChip'))
        starting_balance = int(cgi.escape(self.request.get('startingBalance')))
        inside_bets_raw = cgi.escape(self.request.get('insideBets'))

        saved_bet = saved_betting_numbers.get(inside_bets_raw, None)
        if saved_bet is not None:
            inside_bets_raw = saved_bet

        inside_bets = []
        bets_split = inside_bets_raw.split("|")
        for bet in bets_split:
            numbers = bet.split(",")
            nums = []
            for n in numbers:
                nums.append(int(n))
            inside_bets.append(roulette.InsideBet(nums))

        strat = roulette.RouletteStrategy(inside_bets, [], num_spins, starting_balance)
        strategy_result = roulette.Roulette.play(strat, num_trips_to_tl)

        # Result parsing from here on - split into other location
        ranges = roulette.Roulette.create_ranges()
        percent_returns = roulette.Roulette.initialize_returns_map(ranges)
        html_response = ""

        chances_of_losing_money = 0
        chances_of_breaking_even = 0
        chances_of_doubling = 0
        chances_of_winning = 0

        max_winnings = 0
        total_omgs = 0
        sum_of_omgs = 0

        for trip_to_tl in strategy_result.trips_to_tl:
            percent_return = trip_to_tl.result / float(starting_balance)
            if trip_to_tl.result > max_winnings:
                max_winnings = trip_to_tl.result
            total_omgs += trip_to_tl.omgs
            sum_of_omgs += trip_to_tl.omg_total

            roulette.Roulette.add_total_to_ranges(percent_returns, ranges, percent_return)

        for r in ranges:
            percent_of_pot = percent_returns[r.label] / float(num_trips_to_tl)
            if r.min < .9:
                chances_of_losing_money += percent_of_pot
            if r.min >= 1.1:
                chances_of_winning += percent_of_pot
            if r.min >= 2:
                chances_of_doubling += percent_of_pot
            if r.label == "-10+10%":
                chances_of_breaking_even = percent_of_pot
            html_response += "<p>" + r.label + " = " + str(percent_returns[r.label]) + "; {:.2%}".format(percent_of_pot) + "</p>"

        html_response += "<p>Best trip to Turtle lake results in: " + str(strategy_result.max_winnings) + "</p>"
        html_response += "<p></p>"
        html_response += "<p>Chances of losing money: {:.2%}".format(chances_of_losing_money) + "</p>"
        html_response += "<p>Chances of breaking even: {:.2%}".format(chances_of_breaking_even) + "</p>"
        html_response += "<p>Chances of winning: {:.2%}".format(chances_of_winning) + "</p>"
        html_response += "<p>Chances of doubling: {:.2%}".format(chances_of_doubling) + "</p>"

        end_millis = current_time_millis()
        html_response += "<p>Execution took " + str(end_millis - start_millis) + " milliseconds.</p>"

        self.generate_response(html_response)


    def generate_response(self, response_body):
        self.response.headers["Content-Type"] = "text/html; charset=utf-8"
        self.response.write(response_body)


app = webapp2.WSGIApplication([
    ("/gambling/roulette/", RouletteController),
    ("/gambling/roulette", RouletteController),
    ("/gambling/roulette/driveToTL", RouletteController)
], debug=True)

def current_time_millis():
    return int(round(time.time() * 1000))