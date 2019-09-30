from slacker import Slacker
from SportsCenter import Config
import time


def sendMessage(channel, message):
    slack = Slacker(Config.slackKey)
    slack.chat.post_message(channel, message, as_user=True)
    time.sleep(.2)