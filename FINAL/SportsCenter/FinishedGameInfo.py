import requests
import lxml.html
import time
import calendar
import datetime as dt
import random
from SportsCenter import SlackBot
from SportsCenter import Config
from datetime import date


if __name__ == '__main__':
    x = 1


class FinishedGame:
    def __init__(self, teams):
        self.team1 = teams[0]
        self.team2 = teams[1]


def checkFinishedGames():
    finishedGames = [FinishedGame(["",""])]
    while True:
        time.sleep(random.randint(120,180))
        url, messageBox = getUrl('-final', 'Football')
        html = requests.get(url)
        doc = lxml.html.fromstring(html.content)
        gamesDone = doc.xpath('.//div[@class = "game post-event pre " or @class = "game post-event pre game-even"]')

        for game in gamesDone:
            teams = game.xpath('.//li[@class = "label header" or @class = "label home header"]/a/text()')
            inList = False
            for finGame in finishedGames:
                if finGame.team1 == teams[0] and finGame.team2 == teams[1]:
                    inList = True
                    break
            if not inList:
                quarter = game.xpath('.//hgroup/h3/text()')[0].strip()
                scores = game.xpath('.//li[@class = "outcomes total"]/text()')

                message = quarter + ":  " + teams[0].strip() + "-" + scores[0] + " vs "
                message += teams[1].strip() + "-" + scores[1] + "\n"
                SlackBot.sendMessage(messageBox, message)
                finishedGames.insert(0, FinishedGame(teams))
                finishedGames = finishedGames[:50]


def getUrl(addition, sportType):
    while True:
        if sportType == 'Football':
            if calendar.day_name[date.today().weekday()] in ['Monday','Thursday'] and dt.datetime.now().hour > 17:
                return Config.nflWebsite, 'nfl' + addition + '-scores'
            elif calendar.day_name[date.today().weekday()] in ['Sunday'] and dt.datetime.now().hour > 11:
                return Config.nflWebsite, 'nfl' + addition + '-scores'
            elif calendar.day_name[date.today().weekday()] in ['Friday','Saturday'] and dt.datetime.now().hour > 10:
                html = requests.get(Config.ncaaWeb1)
                doc = lxml.html.fromstring(html.content)
                section = doc.xpath('.//section[@id = "section_sports"]')
                weekNum = section[0].xpath('.//span[@class = "sp-filter-btn sports-weekly-header-dropdown"]/text()')[2]
                weekNum = weekNum.strip().split(" ")[1]
                return Config.ncaaWeb2 + weekNum + '/div1.a/', 'ncaa' + addition + '-scores'
            else:
                time.sleep(60)
        elif sportType == "Baseball":
            return Config.mlbWeb, ''