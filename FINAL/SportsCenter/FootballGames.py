import time
import random

from SportsCenter import Utilities


def checkAllGames():
    finishedGames = [Utilities.FinishedGame(["", ""])]
    currentGames = [Utilities.CurrentGame(["", ""], ["", ""])]
    sportType = 'Football'
    # Specific location for the score of a football game in each football game div element
    scoreLocation = './/li[@class = "outcomes total"]/text()'
    while True:
        currentGames, finishedGames = Utilities.mainLoop(sportType, scoreLocation, currentGames, finishedGames)
        # Update every 5 to 6 minutes because football scores do not change very often
        time.sleep(random.randint(300,360))
