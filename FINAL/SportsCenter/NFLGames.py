import requests
import lxml.html
import time
import random

from SportsCenter import Utilities


if __name__ == '__main__':
    x = 1

def checkAllGames():
    finishedGames = [Utilities.FinishedGame(["", ""])]
    currentGames = [Utilities.CurrentGame(["", ""], ["", ""])]
    while True:

        # Gets the url and name of the message box for nba games
        url, messageBox = Utilities.getUrl('Football')
        doc = lxml.html.fromstring(requests.get(url).content)
        # Gets all baseball game elements with the specified div elements for the day
        todaysGames = doc.xpath('.//div[@class = "game mid-event pre " or @class = "game mid-event pre game-even"]')
        todaysGames += doc.xpath('.//div[@class = "game post-event pre " or @class = "game post-event pre game-even"]')
        # Loops through all games for the current day
        for game in todaysGames:
            # This if is for all games that are currently in progress and does tests on them
            if game.get('class') in ['game mid-event pre ', 'game mid-event pre game-even']:
                # Update list with all the necessary information for the current game we are looking at
                currentGames = Utilities.curGame(game, currentGames, './/li[@class = "outcomes total"]/text()',
                                                 messageBox, 'Football')
            # This if is for all games that have been finished
            if game.get('class') in ['game post-event pre ', 'game post-event pre game-even']:
                # Update list with all the necessary information for the finished game we are looking at
                finishedGames = Utilities.finalGame(game, finishedGames,
                                                    './/li[@class = "outcomes total"]/text()', messageBox)
        time.sleep(random.randint(120, 180))