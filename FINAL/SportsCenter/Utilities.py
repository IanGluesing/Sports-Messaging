import time
import datetime as dt
from datetime import date
import lxml.html
import requests
import calendar

from SportsCenter import Config
from SportsCenter import SlackBot


class CurrentGame:
    # Class to keep track of all current games and there scores
    def __init__(self, teams, scores):
        self.team1 = teams[0]
        self.team2 = teams[1]
        self.score1 = scores[0]
        self.score2 = scores[1]


# Class to be able to keep track of sports games that have finished
class FinishedGame:
    def __init__(self, teams):
        self.team1 = teams[0]
        self.team2 = teams[1]


def gameStarting(teams, scores, quarter, sport):
    # Formats the message that is sent to the user for a game that has just started
    message = (teams[0].strip() + " vs " + teams[1].strip() + " has started\n")
    message += (scores[0] + " - " + scores[1] + " --- " + quarter + "\n")
    filler1, messageBox = getUrl(sport)
    SlackBot.sendMessage(messageBox, message)


def curGame(game, gameList, scoreLocation, messageBox, sportType):
    # might need to change these because they might have different values for games that are not finished yet
    scores = game.xpath(scoreLocation)
    # Gets team names from the game it is looking at
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
        gameList.insert(0, CurrentGame(teams, scores))
        gameList = gameList[:30]
        tme = game.xpath('.//hgroup/h3/text()')[0].strip()
        # Sends the game to the new game method to send a specific message
        gameStarting(teams, scores, tme, sportType)
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
        # Formats the message that is going to be sent to the user
        message = tme + ":  " + teams[0].strip() + "-" + scores[0] + " vs "
        message += teams[1].strip() + "-" + scores[1] + "\n"
        SlackBot.sendMessage(messageBox, message)
        gameList.insert(0, FinishedGame(teams))
        return gameList[:30]
    else:
        return gameList


def getUrl(sportType):
    while True:
        if sportType == 'Football':
            # If statements will only work based on current days of the week and time of day
            if calendar.day_name[date.today().weekday()] in ['Monday','Thursday'] and dt.datetime.now().hour > 17:
                # Returns the link to the website as well as the chat room any messages should be sent to
                return Config.nflWebsite, 'nfl-scores'
            elif calendar.day_name[date.today().weekday()] in ['Sunday'] and dt.datetime.now().hour > 11:
                # Returns the link to the website as well as the chat room any messages should be sent to
                return Config.nflWebsite, 'nfl-scores'
            elif calendar.day_name[date.today().weekday()] in ['Friday','Saturday'] and dt.datetime.now().hour > 10:
                html = requests.get(Config.ncaaWeb1)
                doc = lxml.html.fromstring(html.content)
                # NCAA scores is set up a little differently compared to how NFL scores are set up
                section = doc.xpath('.//section[@id = "section_sports"]')
                lookingFor = './/span[@class = "sp-filter-btn sports-weekly-header-dropdown"]/text()'
                weekNum = section[0].xpath(lookingFor)[2].strip().split(" ")[1]
                # Returns the url of the current week of all ncaa games
                return Config.ncaaWeb2 + weekNum + '/div1.a/', 'ncaa-football-scores'
            else:
                time.sleep(60)
        elif sportType == "Baseball":
            # Returns the website for baseball games as well as the chat room for where messages need to be sent
            return Config.mlbWeb, 'mlb-scores'
        elif sportType == 'NBAgames':
            # Returns the website for nba games as well as the chat room for where messages need to be sent
            return Config.nbaWeb, 'nba-scores'