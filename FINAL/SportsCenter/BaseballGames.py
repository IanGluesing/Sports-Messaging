import requests
import lxml.html
import time
import random

from SportsCenter import FinishedGameInfo
from SportsCenter import CurrentGames
from SportsCenter import SlackBot


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
                finalGame(game)
                x = 1
        time.sleep(360)

def currentGame(game):
    global currentGames
    # might need to change these because they might have different values for games that are not finished yet
    # scores = game.xpath('.//li[@class = "outcomes first"]/text()')
    # teams = game.xpath('.//li[@class = "label header" or @class = "label home header"]/a/text()')
    # print(scores)
    # print(teams)

def finalGame(game):
    # need to take in type of time keeping to be able to use this emthod for football and baseball
    # would need to take in the list class value for where the scores are located
    global finishedGames
    teams = game.xpath('.//li[@class = "label header" or @class = "label home header"]/a/text()')
    inList = False
    for finGame in finishedGames:
        if finGame.team1 == teams[0] and finGame.team2 == teams[1]:
            inList = True
            break
    if not inList:
        inning = game.xpath('.//hgroup/h3/text()')[0].strip()
        scores = game.xpath('.//li[@class = "outcomes first"]/text()')

        message = inning + ":  " + teams[0].strip() + "-" + scores[0] + " vs "
        message += teams[1].strip() + "-" + scores[1] + "\n"
        SlackBot.sendMessage('mlb-final-scores', message)
        finishedGames.insert(0, FinishedGameInfo.FinishedGame(teams))
        finishedGames = finishedGames[:20]


checkAllGames()




