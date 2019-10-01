from slacker import Slacker
from SportsCenter import Config
import time


def sendMessage(channel, message):
    # Everytime a different wants to send a message to slack, this is the method that will be used
    # Message will be sent to the channel specified
    slack = Slacker(Config.slackKey)
    slack.chat.post_message(channel, message, as_user=True)
    time.sleep(.2)