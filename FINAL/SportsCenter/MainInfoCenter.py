from SportsCenter import FootballGames
from SportsCenter import RedditMessenger
from SportsCenter import MLBGames
from SportsCenter import NBAGames
import threading

#t1 = threading.Thread(target = RedditMessenger.redditBot2, args='',)
t1 = threading.Thread(target = FootballGames.checkAllGames, args='', )
t2 = threading.Thread(target = MLBGames.checkAllGames, args='', )
t3 = threading.Thread(target = NBAGames.chackAllGames, args ='', )


t1.start()
t2.start()
t3.start()
#t4.start()

t1.join()
t2.join()
t3.join()
#t4.join()
