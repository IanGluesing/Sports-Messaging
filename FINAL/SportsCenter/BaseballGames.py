import requests
import lxml.html
import time
import random

from SportsCenter import FinishedGameInfo
from SportsCenter import CurrentGames


if __name__ == '__main__':
    x = 1

currentGames = [CurrentGames.CurrentGame(["", ""], ["", ""])]
finishedGames = [FinishedGameInfo.FinishedGame(["", ""])]

def checkAllGames():
    while True:
        # time.sleep(random.randint(60,90))
        url, messageBox = FinishedGameInfo.getUrl('', 'Baseball')
        doc = lxml.html.fromstring(requests.get(url).content)
        todaysGames = doc.xpath('.//div[@class = "game mid-event pre " or @class = "game mid-event pre game-even"]')
        todaysGames += doc.xpath('.//div[@class = "game post-event pre " or @class = "game post-event pre game-even"]')
        for game in todaysGames:
            if game.get('class') in ['game mid-event pre ','game mid-event pre game-even']:
                # see if scores have changed and print out info
                # call method to do this
                currentGame(game)
            if game.get('class') in ['game post-event pre ', 'game post-event pre game-even']:
                # see if game is in the finishedgames list
                # use method for this part
                print("about to send game")
                currentGame(game)
                x = 1
        time.sleep(100)

def currentGame(game):
    scores = game.xpath('.//li[@class = "outcomes first"]/text()')
    teams = game.xpath('.//li[@class = "label header" or @class = "label home header"]/a/text()')
    print(scores)
    print(teams)

checkAllGames()




