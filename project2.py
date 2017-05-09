import numpy as np
import math
import random
import time
import threading
import sys

values = [8,10,13,6]
prob = [0.31,0.29,0.22,0.18]

periods = 9
start_health = 85
total_amount = 0
life_investment = 0
health_investment = 0
token = values[0]

class TokenGenerator(threading.Thread):
    def __init__(self, event):
        threading.Thread.__init__(self)
        self.stopped = event

    def startGenerator(self):
        while not self.stopped.wait(1):
            token = np.random.choice(values, replace=True, p=prob)
            # print("Current token is %s " % token)

def harvest(health):
    harvest_end_time = time.time() + int((30 * health) / 100)
    harvested_amount = 0
    while time.time() < harvest_end_time:
        clicked_amount = token
        print("I am going to harvest %s " % clicked_amount)
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
    return int(regenerated_health)

def enjoy_life(health, life_investment):
    c = 500
    alpha = 0.028
    beta = 0.5
    mew = 0.5
    left = c * (beta * (health/100+.5) + mew)
    right = 1 - math.exp(-alpha * life_investment)
    life_enjoyed = left * right
    print("Player gained %s enjoyment in this period." % life_enjoyed)

def play(health_investment_percent, life_investment_percent):
    stopFlag = threading.Event()
    myTokenGenerator = TokenGenerator(stopFlag)
    myTokenGenerator.start()
    health = start_health
    my_stash = 0

    for i in range(1, periods+1):
        print("Running through period %s." % i)
        my_stash = my_stash + harvest(health)
        print("Player has $%s." % my_stash)
        life_investment = float(life_investment_percent) * my_stash
        health_investment = float(health_investment_percent) * my_stash

        health = degenerate(health, i)
        health = health + regenerate(health, health_investment)
        health = health if health <= 100 else 100
        if health > 0:
          enjoy_life(health, life_investment)
        print("Player's health is %s." % health)
    # End the token generator
    stopFlag.set()

if __name__ == '__main__':
    play(sys.argv[1], sys.argv[2])
