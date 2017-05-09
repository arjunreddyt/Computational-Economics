import random

POS = ["GO                      "
      ,"Mediterranean Avenue    "
      ,"Community Chest 1       "
      ,"Baltic Avenue           "
      ,"Income Tax              "
      ,"Reading Railroad        "
      ,"Oriental Avenue         "
      ,"Chance 1                "
      ,"Vermont Avenue          "
      ,"Connecticut Avenue      "
      ,"Jail                    "
      ,"St. Charles Place       "
      ,"Electric Company        "
      ,"States Avenue           "
      ,"Virginia Avenue         "
      ,"Pennsylvania Railroad   "
      ,"St. James Place         "
      ,"Community Chest 2       "
      ,"Tennessee Avenue        "
      ,"New York Avenue         "
      ,"Free Parking            "
      ,"Kentucky Avenue         "
      ,"Chance 2                "
      ,"Indiana Avenue          "
      ,"Illinois Avenue         "
      ,"B. & O. Railroad        "
      ,"Atlantic Avenue         "
      ,"Ventnor Avenue          "
      ,"Water Works             "
      ,"Marvin Gardens          "
      ,"Go To Jail              "
      ,"Pacific Avenue          "
      ,"North Carolina Avenue   "
      ,"Community Chest 3       "
      ,"Pennsylvania Avenue     "
      ,"Short Line              "
      ,"Chance 3                "
      ,"Park Place              "
      ,"Luxury Tax              "
      ,"Boardwalk               "
      ]
REPEATS = int(10e5)

class Monopoly:
  position = 0
  doubles = 0
  board = []

  def __init__(self):
    self.position = 0
    self.doubles = 0

    # Initialize the board
    self.board = range(40)
    for i in range(40):
      self.board[i] = 0

  def show(self):
    for i in range(40):
      print(str(POS[i])+" | "+str(self.board[i]/float(REPEATS)))

  def move(self):
    rolled = self.roll()

    if (rolled):
      self.position = (self.position + rolled) % 40
      self.register()


  def roll(self):
    die1 = random.randint(1,6)
    die2 = random.randint(1,6)

    if (die1 == die2):
      self.doubles += 1
    else:
      self.doubles = 0

    if (self.doubles >= 3):
      self.doubles = 0
      self.gotoJail()
      return None
    else:
      return die1 + die2

  def register(self):
    self.board[self.position] += 1

    # Community Chest
    if (self.position == 2  or
        self.position == 17 or
        self.position == 33):
      self.communityChest()

    # Chance
    elif (self.position == 7  or
          self.position == 22 or
          self.position == 36):
      self.chance()

    # Goto Jail
    elif (self.position == 30):
      self.gotoJail()

  def gotoJail(self):
    self.position = 10
    self.register()

  def advanceToGo(self):
    self.position = 0
    self.register()

  def advanceToUtility(self):
    if (self.position <= 12 or self.position > 28):
      self.position = 12
    else:
      self.position = 28

    self.register()

  def advanceToStation(self):
    if (self.position <= 5 or self.position > 35):
      self.position = 5
    elif (self.position <= 15):
      self.position = 15
    elif (self.position <= 25):
      self.position = 25
    elif (self.position <= 35):
      self.position = 35

    self.register()

  def communityChest(self):
    card = random.randint(0,17)

    # Advance to go
    if (card == 0):
      self.advanceToGo()

    elif (card == 4):
      self.gotoJail()

  def chance(self):
    card = random.randint(0,16)

    if (card == 0):
      self.advanceToGo()

    # Go to Illimois Avenue
    elif (card == 1):
      self.position = 24
      self.register()

    elif (card == 2):
      self.advanceToUtility()

    elif (card == 3):
      self.advanceToStation()

    # Go to St Charles Place
    elif (card == 4):
      self.position = 11
      self.register()

    # Go back three spaces
    elif (card == 7):
      self.position = (self.position - 3) % 40
      self.register()

    elif (card == 8):
      self.gotoJail()

    # Go to Reading Railroad
    elif (card == 11):
      self.position = 5
      self.register()

    # Go to Broadwalk
    elif (card == 12):
      self.position = 39
      self.register()


if __name__=='__main__':
  random.seed()
  game = Monopoly()

  for _ in range(REPEATS):
    game.move()

  game.show()



