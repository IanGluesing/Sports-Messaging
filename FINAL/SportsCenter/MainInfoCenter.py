from SportsCenter import FinishedGameInfo
from SportsCenter import CurrentGames
from SportsCenter import RedditMessenger
from SportsCenter import BaseballGames
from SportsCenter import NBAgames
import threading


t1 = threading.Thread(target = CurrentGames.checkCurGames, args='',)
t2 = threading.Thread(target = FinishedGameInfo.checkFinishedGames, args='',)
t3 = threading.Thread(target = RedditMessenger.redditBot2, args='',)
t4 = threading.Thread(target = BaseballGames.checkAllGames, args='',)
t5 = threading.Thread(target = NBAgames.chackAllGames, args ='',)


t1.start()
t2.start()
t3.start()
t4.start()
t5.start()

t1.join()
t2.join()
t3.join()
t4.join()
t5.join()