import requests
import lxml.html
import time
import calendar
import datetime as dt
import random
from SportsCenter import Config
from SportsCenter import BaseballGames
from datetime import date


if __name__ == '__main__':
    x = 1

# Clack to be able to keep track of sports games that have finished
class FinishedGame:
    def __init__(self, teams):
        self.team1 = teams[0]
        self.team2 = teams[1]


def checkFinishedGames():
    # Initializes the list with an empty finished game to be able to loop through the list and compare games
    finishedGames = [FinishedGame(["",""])]
    while True:
        time.sleep(random.randint(120,180))
        # Gets the url for the webpage where the scores are located as well as the channel of the room to send
        # the message to in slack
        url, messageBox = getUrl('-final', 'Football')
        html = requests.get(url)
        doc = lxml.html.fromstring(html.content)
        # Gets all completed games from the webpage
        gamesDone = doc.xpath('.//div[@class = "game post-event pre " or @class = "game post-event pre game-even"]')

        for game in gamesDone:
            # Adds finished games to the list using the method from the Baseball file
            finishedGames = BaseballGames.finalGame(game, finishedGames, './/li[@class = "outcomes total"]/text()',
                                                    messageBox)


def getUrl(addition, sportType):
    while True:
        if sportType == 'Football':
            # If statements will only work based on current days of the week and time of day
            if calendar.day_name[date.today().weekday()] in ['Monday','Thursday'] and dt.datetime.now().hour > 17:
                return Config.nflWebsite, 'nfl' + addition + '-scores'
            elif calendar.day_name[date.today().weekday()] in ['Sunday'] and dt.datetime.now().hour > 11:
                return Config.nflWebsite, 'nfl' + addition + '-scores'
            elif calendar.day_name[date.today().weekday()] in ['Friday','Saturday'] and dt.datetime.now().hour > 10:
                html = requests.get(Config.ncaaWeb1)
                doc = lxml.html.fromstring(html.content)
                # NCAA scores is set up a little differently compared to how NFL scores are set up
                section = doc.xpath('.//section[@id = "section_sports"]')
                weekNum = section[0].xpath('.//span[@class = "sp-filter-btn sports-weekly-header-dropdown"]/text()')[2]
                weekNum = weekNum.strip().split(" ")[1]
                # Returns the url of the current week of all ncaa games
                return Config.ncaaWeb2 + weekNum + '/div1.a/', 'ncaa' + addition + '-scores'
            else:
                time.sleep(60)
        elif sportType == "Baseball":
            return Config.mlbWeb, 'mlb-final-scores'
        elif sportType == "BaseballCurrent":
            return '', 'mlb-scores'