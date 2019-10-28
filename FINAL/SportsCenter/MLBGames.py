import time
import random

from SportsCenter import Utilities


def checkAllGames():
    finishedGames = [Utilities.FinishedGame(["", ""])]
    currentGames = [Utilities.CurrentGame(["", ""], ["", ""])]
    sportType = 'Baseball'
    # Specific location for the score of a baseball game in each baseball game div element
    scoreLocation = './/li[@class = "outcomes first"]/text()'
    while True:
        currentGames, finishedGames = Utilities.mainLoop(sportType, scoreLocation, currentGames, finishedGames)
        # Update every 5 to 6 minutes because baseball game scores do not change very often
        time.sleep(random.randint(300,360))
