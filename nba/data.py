import urllib
import requests
import json
import datetime

class data(object):
    """Data from source provider"""

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
    
    def refresh_teams(self):
        url = 'https://data.nba.com/data/10s/prod/v1/2017/teams.json'
        raw_teams = urllib.request.urlopen(url).read()
        self.json_teams = json.loads(raw_teams.decode('utf-8'))

    def refresh_standings(self):
        url = 'https://data.nba.com/data/10s/prod/v1/current/standings_conference.json'
        raw_standings = urllib.request.urlopen(url).read()
        self.json_standings = json.loads(raw_standings.decode('utf-8'))

    def refresh_scoreboard(self, game_date):
        url = 'https://data.nba.com//data/10s/prod/v1/' + game_date + '/scoreboard.json'
        raw_scoreboard = urllib.request.urlopen(url).read()
        self.json_scoreboard = json.loads(raw_scoreboard.decode('utf-8'))

    def refresh_all(self):
        self.refresh_teams()
        self.refresh_standings()
        self.refresh_scoreboard(datetime.datetime.strftime(datetime.datetime.today(), '%Y%m%d'))

    def get_standings(self):
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

    def __init__(self):        
        self.json_teams = None
        self.json_standings = None
        self.refresh_scoreboard(datetime.datetime.strftime(datetime.datetime.today(), '%Y%m%d'))

        self.load_teams()
        self.standings = self.get_standings()
