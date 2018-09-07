import urllib
import requests
import json
import datetime
from pprint import pprint

class data:
    def team_subreddits(self):
        return ""

    def schedule(self):
        return ""

    def game_threads(self):
        return ""

    def top_bar(self): # Check Bre's work on r/nbadev if you don't know what this is
        def reddit_card():
            return ""
        
        def flair_tool_card():
            return ""
        
        def live_game_updates_cards():
            return ""
        
        top_bar_cards = []
        top_bar_cards.append(reddit_card())
        top_bar_cards.append(flair_tool())
        top_bar_cards.append(live_game_updates())
        return top_bar_cards

    def standings(self):

        standings = {}
        with urllib.request.urlopen('http://data.nba.com/prod/v1/current/standings_conference.json') as url:
            j = json.loads(url.read().decode())

            for i in range(0,15):
                east = j['league']['standard']['conference']['east'][i]
                east_id = east['teamId']
                west = j['league']['standard']['conference']['west'][i]
                west_id = west['teamId']
                tmp_row = {
                    'east_name': self.team_dict[east_id]['short_name'],
                    'east_nick': self.team_dict[east_id]['med_name'],
                    'east_record': east['win'] + '-' + east['loss'],
                    'east_gb_conf': '%.1f' % int(east['gamesBehind']),
                    'east_div_rank': east['divRank'],
                    'conf_rank': str(i+1),
                    'west_name': self.team_dict[west_id]['short_name'],
                    'west_nick': self.team_dict[west_id]['med_name'],
                    'west_record': west['win'] + '-' + west['loss'],
                    'west_gb_conf': '%.1f' % int(west['gamesBehind']),
                    'west_div_rank': west['divRank']
                }
                standings[int(i+1)] = tmp_row
        return standings

    def playoffs(self):
        """
        bracket = {}
        with urllib.request.urlopen('https://data.nba.com/data/10s/prod/v1/2017/playoffsBracket.json') as url:
            j = json.loads(url.read().decode())

            for i in range(0,15):
                series = j['series'][i]
                series_name = str(i+1)
                series_winner = series['summaryStatusText'][:3]
                
                top_seed = series['topRow']['teamId']
                bottom_seed = series['bottomRow']['teamId']
                
                if series_winner == self.team_dict[top_seed]['short_name']:
                    series_record = series['summaryStatusText'][-3:].replace("-", " - ")
                else:
                    series_record = series['summaryStatusText'][-3:].replace("-", " - ")[::-1]

                tmp_brkt = {
                    'series': series['confName'] + " R" + series['roundNum'],
                    'top_name': self.team_dict[top_seed]['short_name'],
                    'top_seed': series['topRow']['seedNum'],
                    'bottom_name': self.team_dict[bottom_seed]['short_name'],
                    'bottom_seed': series['bottomRow']['seedNum'],
                    'summary': series_record
                }

                bracket[series_name] = tmp_brkt

                if j['series'][14]:
                    if [series['topRow']['isSeriesWinner'],series['bottomRow']['isSeriesWinner']] == 'true':
                        bracket['16'] = {
                            'champ': series_winner
                        }
                    else:
                        bracket['16'] = {
                            'champ': "NA"
                        }
        return bracket
        """
        return ""

    def __init__(self):        
        self.json_teams = None
        self.load_teams()

    # Helper functions
    def load_teams(self):
        self.team_dict = {}
        self.team_dict_med_key = {}
        self.team_dict_short_key = {}
        with open('data/teams.csv', 'r') as teamInfoFile:
            for teamInfoRow in teamInfoFile.read().split('\n'):
                teamInfo = teamInfoRow.split(',')
                tmp_team_dict = {
                    'long_name': teamInfo[0] + ' ' + teamInfo[1],
                    'med_name': teamInfo[1],
                    'short_name': teamInfo[2].upper(),
                    'sub': teamInfo[3],
                    'timezone': teamInfo[4],
                    'division': teamInfo[5],
                    'conference': teamInfo[6],
                    'id': teamInfo[7]
                }
                self.team_dict[teamInfo[7]] = tmp_team_dict
                self.team_dict_med_key[teamInfo[1]] = tmp_team_dict
                self.team_dict_short_key[teamInfo[2].upper()] = tmp_team_dict

data = data()
pprint(data.standings())