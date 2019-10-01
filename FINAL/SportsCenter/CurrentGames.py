import requests
import lxml.html
import time
import random
from SportsCenter import SlackBot
from SportsCenter import FinishedGameInfo


if __name__ == '__main__':
    x = 1


class CurrentGame:
    def __init__(self, teams, scores):
        self.team1 = teams[0]
        self.team2 = teams[1]
        self.score1 = scores[0]
        self.score2 = scores[1]


def getGameText(teams, scores, quarter, left, right):
    finalString = teams[0].strip() + " vs " + teams[1].strip() + "\n"
    finalString += scores[0] + " - " + scores[1] + " --- " + quarter + "\n"
    finalString += teams[0].strip() + ": "
    for item in left[:4]:
        for info in item:
            finalString += info + ", "

    finalString += "\n" + teams[1].strip() + ": "
    for item in right[:4]:
        for info in item:
            finalString += info + ", "
    return finalString + "\n"


def checkCurGames():
    gameObjs = [CurrentGame(["", ""], ["", ""])]
    while True:
        url, messageBox = FinishedGameInfo.getUrl('', 'Football')
        doc = lxml.html.fromstring(requests.get(url).content)
        currentGames = doc.xpath('.//div[@class = "game mid-event pre " or @class = "game mid-event pre game-even"]')

        for game in currentGames:
            scores = game.xpath('.//li[@class = "outcomes total"]/text()')
            teams = game.xpath('.//li[@class = "label header" or @class = "label home header"]/a/text()')
            quarter = game.xpath('.//hgroup/h3/text()')[0].strip()

            inList = False
            for fbGame in gameObjs:
                if fbGame.team1 == teams[0] and fbGame.team2 == teams[1]:
                    inList = True
                    break
            if inList:
                if fbGame.score1 != scores[0] or fbGame.score2 != scores[1]:
                    labelsLeft = game.xpath('.//li[@class = "label"]')
                    labelsright = game.xpath('.//li[@class = "label right"]')
                    teamLeft,teamRight = [],[]

                    for labelL, labelR in zip(labelsLeft, labelsright):
                        teamLeft.append(labelL.xpath('.//span/text()'))
                        teamLeft.append(labelL.xpath('.//p/text()'))
                        teamRight.append(labelR.xpath('.//span/text()'))
                        teamRight.append(labelR.xpath('.//p/text()'))

                    fbGame.score1 = scores[0]
                    fbGame.score2 = scores[1]

                    SlackBot.sendMessage(messageBox, getGameText(teams, scores, quarter, teamLeft, teamRight))
            else:
                gameObjs.insert(0, CurrentGame(teams, scores))
                gameObjs = gameObjs[:50]
                gameStarting(teams,scores,quarter)
        time.sleep(random.randint(120,180))


def gameStarting(teams, scores, quarter):
    message = (teams[0].strip() + " vs " + teams[1].strip() + " has started\n")
    message += (scores[0] + " - " + scores[1] + " --- " + quarter + "\n")
    filler1, messageBox = FinishedGameInfo.getUrl('', 'Football')
    SlackBot.sendMessage(messageBox, message)
    return

