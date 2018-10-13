from data import data
from markdown import markdown
from pprint import pprint
import datetime
import requests
import praw
from pprint import pprint
import config
# def getThread(hTeamName, vTeamName):
#     for thread in bot.subreddit('nba' ).new(limit=200):
#         threadType = str(thread.link_flair_css_class)
#         threadDate =  datetime.datetime.now().replace(hour = 0, minute = 0, second = 0, microsecond = 0)
#
#         if thread.threadType == threadType and thread.threadDate == threadDate and all(x in thread.threadTitle for x in [hTeamName, vTeamName]):
#             return thread.threadID
# data = requests.get('https://data.nba.com/data/10s/prod/v1/2017/teams.json').json()
# nicknames = []
#
# for teams in data['league']['standard']:
#     nicknames.append(teams['nickname'])
#
# print(nicknames)
from markdown import markdown
from data import data
mdown = markdown()
data = data()
teams = []
bot = praw.Reddit(client_id=config.client_id, client_secret=config.client_secret, user_agent=config.user_agent, username=config.username, password=config.password)
def getThread(hTeamName, vTeamName):
    for thread in bot.subreddit('nba').new(limit=200):
        threadType = str(thread.link_flair_css_class)
        threadDate =  datetime.datetime.now().replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        pprint(vars(thread))
        if thread.period['current'] == 4 and thread.clock == '':
            if 'postgamethread' == threadType and datetime.datetime.fromtimestamp(thread.created).replace(hour = 0, minute = 0, second = 0, microsecond = 0) == threadDate+datetime.timedelta(days=1) and all(x in thread.title for x in [hTeamName, vTeamName]):
                return thread.url
        else:
            if 'gamethread' == threadType and datetime.datetime.fromtimestamp(thread.created).replace(hour = 0, minute = 0, second = 0, microsecond = 0) == threadDate+datetime.timedelta(days=1) and all(x in thread.title for x in [hTeamName, vTeamName]):
                return thread.url
print((mdown.schedule(data.schedule())))
# print(data.standings())