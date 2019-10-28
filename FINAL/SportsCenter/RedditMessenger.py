import praw
import time
from SportsCenter import SlackBot
from SportsCenter import Config
from datetime import date

if __name__ == '__main__':
    x = 1

# Team name dictionary for team names and stadiums
teamStadiums = {"Kansas City Chiefs": "Arrowhead Stadium", "Dallas Cowboys": "AT&T Stadium",
                "Carolina Panthers": "Bank of America Stadium", "Seattle Seahawks": "CenturyLink Field",
                "Los Angeles Chargers": "Dignity Health Sports Park",
                "Denver Broncos": "Empower Field at Mile High",
                "Washington Redskins": "FedExField", "Cleveland Browns": "FirstEnergy Stadium",
                "Detroit Lions": "Ford Field", "New England Patriots": "Gillette Stadium",
                "Miami Dolphins": "Hard Rock Stadium", "Pittsburgh Steelers": "Heinz Field",
                "Green Bay Packers": "Lambeau Field",
                "San Francisco 49ers": "Levi's Stadium", "Philadelphia Eagles": "Lincoln Financial Field",
                "Los Angeles Rams": "Los Angeles Memorial Coliseum", "Indianapolis Colts": "Lucas Oil Stadium",
                "Baltimore Ravens": "M&T Bank Stadium", "New Orleans Saints": "Mercedes-Benz Superdome",
                "Atlanta Falcons": "Mercedes-Benz Stadium", "New York Giants": "MetLife Stadium",
                "New York Jets": "MetLife Stadium", "Buffalo Bills": "New Era Field",
                "Tennessee Titans": "Nissan Stadium",
                "Houston Texans": "NRG Stadium", "Cincinnati Bengals": "Paul Brown Stadium",
                "Tampa Bay Buccaneers": "Raymond James Stadium", "Oakland Raiders": "RingCentral Coliseum",
                "Chicago Bears": "Soldier Field", "Arizona Cardinals": "State Farm Stadium",
                "Jacksonville Jaguars": "TIAA Bank Field", "Minnesota Vikings": "U.S. Bank Stadium"}

# This is how you are able to communicate with the reddit website and your reddit account
reddit = praw.Reddit(client_id=Config.reddit_id,
                     client_secret=Config.reddit_secret,
                     username=Config.reddit_username,
                     password=Config.reddit_password,
                     user_agent=Config.reddit_agent)

# Method to format messages for upcoming NFL games that will be sent to the user through slack
def getFormattedGameString(submission):
    global teamStadiums
    parts = submission.title.split("@")
    finalStatement = "The " + parts[0].replace("Game Thread: ", "").strip()
    newParts = parts[1].split(" (")
    finalStatement += " @ The " + newParts[0].strip() + "\nGame Time: " + newParts[1].replace(")", "")

    # Loops through dictionary of teams and stadiums to be able to tell the user what stadium the game will be played at
    for key, val in teamStadiums.items():
        if key.lower() == newParts[0].strip().lower():
            finalStatement += "\nLocation: " + val
    return finalStatement


def redditBot2():
    # Gets the reddit information for the subreddit we are using to get posts from
    subreddit = reddit.subreddit(Config.reddit_subreddit_name)
    printedTitles = []
    while True:
        # Will only run on Thursday, Sunday, or Monday because NFL games are not played on other days
        if date.today().weekday() in [3,6,0]:
            # Gets 15 most recent posts from the subreddit
            new_stream = subreddit.new(limit=15)
            for submission in new_stream:
                # This will only be true if the title has a certain modifier and we have already sent a message
                # that uses the title from the post
                if submission.link_flair_text == Config.reddit_thread and submission.title not in printedTitles:
                    SlackBot.sendMessage('nfl-scores', getFormattedGameString(submission) + "\n")
                    printedTitles.insert(0, submission.title)
            # Only keeps the 15 most recent titles so that the list will not continue to fill up while running forever
            printedTitles = printedTitles[:15]
            time.sleep(600)
        else:
            # Checks every 8 hours to see if the current day is in the list of game days
            print(date.today().weekday())
            time.sleep(28800)
