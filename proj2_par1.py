import numpy as np
import math
import random
import time
import threading
import sys

values = [8, 10, 13, 6]
prob = [0.31, 0.29, 0.22, 0.18]

periods = 14
start_health = 85
total_amount = 0
life_investment = 0
health_investment = 0


class TokenGenerator(object):
    def __init__(self, interval):
        self._timer = None
        self.interval = interval
        self.is_running = False
        self.token = np.random.choice(values, replace=False, p=prob)
        self.startGenerator()

    def startGenerator(self):
        if not self.is_running:
            self._timer = threading.Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def _run(self):
        self.is_running = False
        self.startGenerator()
        self.token = np.random.choice(values, replace=False, p=prob)
        print("Current token is %s " % self.token)

    def get_token(self):
        return self.token

    def stop(self):
        self._timer.cancel()
        self.is_running = False


def harvest(health, tokengenerator):
    harvest_end_time = time.time() + int((30 * health) / 100)
    harvested_amount = 0
    while time.time() < harvest_end_time:
        clicked_amount = tokengenerator.get_token()
        print("Going to harvest %s " % clicked_amount)
        time.sleep(3)
        harvested_amount = harvested_amount + clicked_amount
    return harvested_amount


def degenerate(health, period):

    degenerated_health = health - (15 + period)
    if degenerated_health < 0:
        print "Player is Dead"
        return 0
    return degenerated_health


def regenerate(health, health_investment):
    delta = 0.025
    gamma = 30
    numerator = 1 - math.exp(-1 * delta * health_investment)
    denominator = 1 + math.exp(-1 * delta * health_investment)
    regenerated_health = gamma * numerator/denominator
    health += int(regenerated_health)
    return health if health <= 100 else 100


def enjoy_life(health, life_investment):
    c = 500
    alpha = 0.028
    beta = 0
    mew = 1
    left = c * (beta * (health/100+.5) + mew)
    right = 1 - math.exp(-alpha * life_investment)
    life_enjoyed = left * right
    print("Player gained %s enjoyment in this period." % life_enjoyed)
    return life_enjoyed


def play(health_investment_percent, life_investment_percent):
    myTokenGenerator = TokenGenerator(1)
    health = start_health
    my_stash = 0
    total_life_enjoyed = 0

    for i in range(1, periods+1):
        print("Running through period %s." % i)
        harvested = harvest(health, myTokenGenerator)
        print("Harvest for this period is %s" % harvested)
        my_stash += harvested
        print("Player has $%s." % my_stash)
        life_investment = float(life_investment_percent) * my_stash
        health_investment = float(health_investment_percent) * my_stash
        reduction = life_investment + health_investment

        print("Player had %(stash)s and is spending $%(life)s on enjoying "
              "life and $%(med)s on his medical bills and is left with %("
              "left)s" % {'stash': my_stash, 'life': life_investment,
                          'med': health_investment,
                          'left': my_stash - reduction,
                          })
        my_stash -= reduction

        health = degenerate(health, i)
        health = regenerate(health, health_investment)
        print("Player's health is %s." % health)

        if health > 0:
            total_life_enjoyed += enjoy_life(health, life_investment)

    # End the token generator
    myTokenGenerator.stop()
    print("Enjoyed %s" % total_life_enjoyed)
    print("Left with %s" % my_stash)

if __name__ == '__main__':
    play(sys.argv[1], sys.argv[2])
