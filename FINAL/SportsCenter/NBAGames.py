import requests
import lxml.html
import time

from SportsCenter import FinishedGameInfo
from SportsCenter import CurrentGames
from SportsCenter import BaseballGames
from SportsCenter import SlackBot


if __name__ == '__main__':
    x = 1

def chackAllGames():
    finishedGames = [FinishedGameInfo.FinishedGame(["", ""])]
    currentGames = [CurrentGames.CurrentGame(["", ""], ["", ""])]
    while True:
        url, messageBox = FinishedGameInfo.getUrl('', 'NBAgames')
        doc = lxml.html.fromstring(requests.get(url).content)
        # Gets all baseball game elements with the specified div elements for the day
        todaysGames = doc.xpath('.//div[@class = "game mid-event pre " or @class = "game mid-event pre game-even"]')
        todaysGames += doc.xpath('.//div[@class = "game post-event pre " or @class = "game post-event pre game-even"]')
        for game in todaysGames:
            if game.get('class') in ['game mid-event pre ', 'game mid-event pre game-even']:
                # see if scores have changed and print out info
                # call method to do this
                currentGames = BaseballGames.curGame(game, currentGames, './/li[@class = "outcomes total"]/text()',
                                                    messageBox, 'NBAgames')
            if game.get('class') in ['game post-event pre ', 'game post-event pre game-even']:
                # see if game is in the finishedgames list
                # use method for this part
                # Process finished games using this method as well as getting the scores from the html
                finishedGames = BaseballGames.finalGame(game, finishedGames,
                                                        './/li[@class = "outcomes total"]/text()', messageBox)
        time.sleep(360)

































