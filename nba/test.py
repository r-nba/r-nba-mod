from data import data
from markdown import markdown
from pprint import pprint
from prawmod import bot
import datetime
import requests
import json
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
for team, team_data in data.team_abbrev_dict.items():
    teams.append((team, team_data['med_name']))
print(teams)