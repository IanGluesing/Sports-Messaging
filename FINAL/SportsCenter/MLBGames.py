import requests
import lxml.html
import time

from SportsCenter import FinishedGameInfo
from SportsCenter import CurrentGames
from SportsCenter import SlackBot


if __name__ == '__main__':
    x = 1



def checkAllGames():
    finishedGames = [FinishedGameInfo.FinishedGame(["", ""])]
    currentGames = [CurrentGames.CurrentGame(["", ""], ["", ""])]
    while True:
        # Gets the url for the baseball scores website as well as for the message box for baseball games
        url, messageBox = FinishedGameInfo.getUrl('', 'Baseball')
        doc = lxml.html.fromstring(requests.get(url).content)
        # Gets all baseball game elements with the specified div elements for the day
        todaysGames = doc.xpath('.//div[@class = "game mid-event pre " or @class = "game mid-event pre game-even"]')
        todaysGames += doc.xpath('.//div[@class = "game post-event pre " or @class = "game post-event pre game-even"]')
        for game in todaysGames:
            if game.get('class') in ['game mid-event pre ','game mid-event pre game-even']:
                # see if scores have changed and print out info
                # call method to do this
                currentGames = curGame(game, currentGames, './/li[@class = "outcomes first"]/text()', 'mlb-scores',
                                       'BaseballCurrent')
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

    for currentGame in gameList:
        # If the game matches one of the games in the list, that means a game completion message was already sent
        if currentGame.team1 == teams[0] and currentGame.team2 == teams[1]:
            inList = True
            break
    if inList:
        # If the game we are checking is in the list and the score has changed from the last time, we run this if
        # statement
        if currentGame.score1 != scores[0] or currentGame.score2 != scores[1]:
            # Gets the current time left for whatever game and sport we are checking
            tme = game.xpath('.//hgroup/h3/text()')[0].strip() + "\n"

            # Formats the message that is going to be sent to a chat room
            message = teams[0].strip() + ' ' + scores[0] + ' - ' + teams[1].strip() + ' ' + scores[1] + " --- " + tme
            # Sends message to the correct chat room
            SlackBot.sendMessage(messageBox, message)
            # Then updates new scores for each team
            currentGame.score1 = scores[0]
            currentGame.score2 = scores[1]
            return gameList
        # If the game scores have not changed, then the list is just returned with no updates
        return gameList
    else:
        # If the game we are looking at is not currently in the gamelist, then it will be added to the beginning of the
        # list
        gameList.insert(0, CurrentGames.CurrentGame(teams,scores))
        gameList = gameList[:30]
        tme = game.xpath('.//hgroup/h3/text()')[0].strip()
        # Sends the game to the new game method to send a specific message
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






