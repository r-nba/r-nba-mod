
import urllib
import requests
import json
import datetime

class Data(object):
    """Data from source provider"""
    
    def refreshTeams(self):
        url = 'https://data.nba.com/data/10s/prod/v1/2017/teams.json'
        rawTeams = urllib.request.urlopen(url).read()
        self.jsonTeams = json.loads(rawTeams.decode('utf-8'))

    def refreshStandings(self):
        url = 'https://data.nba.com/data/10s/prod/v1/current/standings_conference.json'
        rawStandings = urllib.request.urlopen(url).read()
        self.jsonStandings = json.loads(rawStandings.decode('utf-8'))

    def refreshScoreboard(self, gameDate):
        url = 'https://data.nba.com//data/10s/prod/v1/' + gameDate + '/scoreboard.json'
        rawScoreboard = urllib.request.urlopen(url).read()
        self.jsonScoreboard = json.loads(rawScoreboard.decode('utf-8'))

    def refreshAll(self):
        self.refreshTeams()
        self.refreshStandings()
        self.refreshScoreboard(datetime.datetime.strftime(datetime.datetime.today(), '%Y%m%d'))

    def __init__(self):        
        self.jsonTeams = None
        self.jsonStandings = None
        self.refreshScoreboard(datetime.datetime.strftime(datetime.datetime.today(), '%Y%m%d'))