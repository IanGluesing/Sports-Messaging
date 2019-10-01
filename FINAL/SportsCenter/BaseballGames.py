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

def checkAllGames():
    finishedGames = [FinishedGameInfo.FinishedGame(["", ""])]
    while True:
        url, messageBox = FinishedGameInfo.getUrl('', 'Baseball')
        doc = lxml.html.fromstring(requests.get(url).content)
        # Gets all baseball game elements with the specified div elements for the day
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
                # Process finished games using this method as well as getting the scores from the html
                finishedGames = finalGame(game, finishedGames, './/li[@class = "outcomes first"]/text()')
        time.sleep(360)

def currentGame(game):
    global currentGames
    # might need to change these because they might have different values for games that are not finished yet
    # scores = game.xpath('.//li[@class = "outcomes first"]/text()')
    # teams = game.xpath('.//li[@class = "label header" or @class = "label home header"]/a/text()')
    # print(scores)
    # print(teams)

def finalGame(game, gameList, scoreLocation):
    # need to take in type of time keeping to be able to use this emthod for football and baseball
    # would need to take in the list class value for where the scores are located
    teams = game.xpath('.//li[@class = "label header" or @class = "label home header"]/a/text()')
    inList = False
    # Loops through all finished games in the list of finished games sent to the method
    for finGame in gameList:
        # If the game mathces one of the games in the list, that means a game completion message was already sent
        if finGame.team1 == teams[0] and finGame.team2 == teams[1]:
            inList = True
            break
    if not inList:
        # If a completion message has not already been sent, this message will get the game information
        # and send a message to the proper channel in slack and add the game to the list of finished games
        tme = game.xpath('.//hgroup/h3/text()')[0].strip()
        scores = game.xpath(scoreLocation)

        message = tme + ":  " + teams[0].strip() + "-" + scores[0] + " vs "
        message += teams[1].strip() + "-" + scores[1] + "\n"
        SlackBot.sendMessage('mlb-final-scores', message)
        gameList.insert(0, FinishedGameInfo.FinishedGame(teams))
        return gameList[:30]






