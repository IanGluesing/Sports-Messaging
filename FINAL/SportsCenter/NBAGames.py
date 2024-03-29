import time
import random

from SportsCenter import Utilities


def chackAllGames():
    finishedGames = [Utilities.FinishedGame(["", ""])]
    currentGames = [Utilities.CurrentGame(["", ""], ["", ""])]
    sportType = 'NBAgames'
    # Specific location for the score of a basketball game in each basketball game div element
    scoreLocation = './/li[@class = "outcomes total"]/text()'
    while True:
        currentGames, finishedGames = Utilities.mainLoop(sportType, scoreLocation, currentGames, finishedGames)
        # Update every 2 to 3 minutes because basketball scores change quite often
        time.sleep(random.randint(120,180))
