import requests
import lxml.html
import time
import random

from SportsCenter import FinishedGameInfo
from SportsCenter import CurrentGames
from SportsCenter import SlackBot


if __name__ == '__main__':
    x = 1



def checkAllGames():
    finishedGames = [FinishedGameInfo.FinishedGame(["", ""])]
    currentGames = [CurrentGames.CurrentGame(["", ""], ["", ""])]
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
                currentGames = curGame(game, currentGames, './/li[@class = "outcomes first"]/text()', 'mlb-scores','BaseballCurrent')
                print("CURRENT GAMES AFTER METHOD")
                print(currentGames)
            if game.get('class') in ['game post-event pre ', 'game post-event pre game-even']:
                # see if game is in the finishedgames list
                # use method for this part
                # Process finished games using this method as well as getting the scores from the html
                finishedGames = finalGame(game, finishedGames, './/li[@class = "outcomes first"]/text()', messageBox)
        time.sleep(360)


def curGame(game, gameList, scoreLocation, messageBox, sportType):
    # might need to change these because they might have different values for games that are not finished yet
    scores = game.xpath(scoreLocation)
    teams = game.xpath('.//li[@class = "label header" or @class = "label home header"]/a/text()')
    inList = False

    print(gameList)

    for currentGame in gameList:
        # If the game mathces one of the games in the list, that means a game completion message was already sent
        if currentGame.team1 == teams[0] and currentGame.team2 == teams[1]:
            inList = True
            print("going to break")
            print(gameList)
            print(currentGame.score1, currentGame.score2)
            print(scores)
            break

    print("checking if inlist part")
    if inList:
        if currentGame.score1 != scores[0] or currentGame.score2 != scores[1]:
            tme = game.xpath('.//hgroup/h3/text()')[0].strip()

            message = teams[0].strip() + ' ' + scores[0] + ' - ' + teams[1].strip() + ' ' + scores[1] + "\t" + tme
            SlackBot.sendMessage(messageBox, message)
            currentGame.score1 = scores[0]
            currentGame.score2 = scores[1]
            print(gameList)
            print("inside if")
            return gameList
        return gameList
    else:
        gameList.insert(0, CurrentGames.CurrentGame(teams,scores))
        gameList = gameList[:30]
        tme = game.xpath('.//hgroup/h3/text()')[0].strip()
        CurrentGames.gameStarting(teams, scores, tme, sportType)
        return gameList




def finalGame(game, gameList, scoreLocation, messageBox):
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
        SlackBot.sendMessage(messageBox, message)
        gameList.insert(0, FinishedGameInfo.FinishedGame(teams))
        return gameList[:30]
    else:
        return gameList






