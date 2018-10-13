from urllib.request import urlopen
import json
import datetime
import calendar
import collections
import praw
import config
from pprint import pprint
from dateutil import parser

def main():
    d = data()
    d.standings()
    d.playoffs()

class data:

    def team_subreddits(self):
        return [{"team_abbrev": abbrev, "subreddit": self.team_abbrev_dict[abbrev]["sub"]} for abbrev in
                self.team_abbrev_dict]

    def get_schedule(self):
        days = {}
        for delta in range(3):
            date = (datetime.datetime.today() + datetime.timedelta(days=delta))
            month = calendar.month_name[date.month]
            calendar_day = calendar.day_name[date.weekday()]
            key = calendar_day + ", " + month + " " + date.strftime('%d')
            parameter = date.strftime('%Y%m%d')
            games = []
            with urlopen('http://data.nba.com/prod/v2/' + parameter + '/scoreboard.json') as url:
                j = json.loads(url.read().decode())
                for game in j["games"]:
                    if game["vTeam"]["teamId"] not in self.team_id_dict or game["hTeam"][
                        "teamId"] not in self.team_id_dict:  # Games against non-nba teams are disregarded
                        continue
                    gameDetails = {}
                    gameDetails["time"] = game["startTimeEastern"].replace(" ET", "")

                    gameDetails["home"] = game["hTeam"]["triCode"]
                    gameDetails["home_subreddit"] = self.team_id_dict[game["hTeam"]["teamId"]]["sub"]
                    gameDetails["away"] = game["vTeam"]["triCode"]
                    gameDetails["away_subreddit"] = self.team_id_dict[game["vTeam"]["teamId"]]["sub"]
                    gameDetails['station'] = game['watch']['broadcast']['broadcasters']['national']
                    if gameDetails['station']:
                        gameDetails['station'] = gameDetails['station'][0]['shortName']
                    
                    games.append(gameDetails)
                    
            days[key] = games
            
        return days

    def get_threads(self, hTeam, vTeam):
        
        away_team_med = team_abbrev_dict[vTeam]['med_name']
        home_team_med = team_abbrev_dict[hTeam]['med_name']
        
        for t in self.bot.subreddit('nba').new(limit=200):
            if (away_team_med in t.title) and (home_team_med in t.title):
                if t.link_flair_css == 'game':
                    return '//redd.it/' + t.id + ' "GT"'
                elif t.link_flair_css == 'post':
                    return '//redd.it/' + t.id + ' "GF"'
            else:
                return None
        
    def get_games(self):
        games = []
        parameter = datetime.datetime.today().strftime('%Y%m%d')
        with urlopen('http://data.nba.com/prod/v2/' + parameter + '/scoreboard.json') as url:
            j = json.loads(url.read().decode())
            for game in j["games"]:

                if game["vTeam"]["teamId"] not in self.team_id_dict or game["hTeam"][
                    "teamId"] not in self.team_id_dict:  # Games against non-nba teams are disregarded
                    continue
                
                for team in self.teams:
                    if team[0] == game['hTeam']['triCode']:
                        hTeam = team[1]
                    if team[0] == game['vTeam']['triCode']:
                        vTeams = team[1]
                        
                gameDetails = {}
                if game["statusNum"] == 1:  # Game hasn't started
                    gameDetails["time"] = game["startTimeEastern"].replace(" ET", "")
                elif game["statusNum"] == 2:  # Game in progress
                    gameDetails["time"] = str(game["clock"]) + " " + str(game["period"]["current"]) + "Q"
                elif game["statusNum"] == 3:  # Game completed
                    gameDetails["time"] = "FINAL"

                # Find Home and Away teams
                gameDetails["home"] = game["hTeam"]["triCode"]
                gameDetails["away"] = game["vTeam"]["triCode"]

                # Find Home and Away team subs
                gameDetails["home_subreddit"] = self.team_abbrev_dict[gameDetails["home"]]["sub"]
                gameDetails["away_subreddit"] = self.team_abbrev_dict[gameDetails["away"]]["sub"]

                # Find Home and Away team records
                gameDetails["home_win"] = game["hTeam"]["win"]
                gameDetails["home_loss"] = game["hTeam"]["loss"]
                gameDetails["away_win"] = game["vTeam"]["win"]
                gameDetails["away_loss"] = game["vTeam"]["loss"]

                # Find arena
                gameDetails['arena'] = game["arena"]["name"] + ', ' + game["arena"]["city"] + ', ' + game["arena"]["stateAbbr"]

                # Find broadcast info
                broadcasts = dict(
                    local=[],
                    national=[]
                )
                
                for broadcast in game["watch"]["broadcast"]["broadcasters"]["national"]:
                    if len(broadcast) > 0:
                        broadcasts["national"].append(broadcast["shortName"])
                for broadcast in (game["watch"]["broadcast"]["broadcasters"]["vTeam"], game["watch"]["broadcast"]["broadcasters"]["hTeam"]):
                    if len(broadcast) > 0:
                        broadcasts["local"].append(broadcast[0]["shortName"])

                # Find scores if they exist
                if not game["statusNum"] == 1:
                    gameDetails["home_score"] = game["hTeam"]["score"]
                    gameDetails["away_score"] = game["vTeam"]["score"]
                else:
                    gameDetails["home_score"] = ""
                    gameDetails["away_score"] = ""
                
                gameDetails["threadtime"] = parser.parse(game["startTimeEastern"])
                gameDetails['thread_created'] = False

                # Find threads if they exist
                thread_id = self.get_threads(hTeam, vTeam)
                if thread_id is not None:
                    gameDetails['thread_id'] = thread_id
                
                games.append(gameDetails)
                
        return games

    def get_standings(self):
        standings = {}
        with urlopen('http://data.nba.com/prod/v1/current/standings_conference.json') as url:
            j = json.loads(url.read().decode())

            for i in range(0, 15):
                east = j['league']['standard']['conference']['east'][i]
                east_id = east['teamId']
                west = j['league']['standard']['conference']['west'][i]
                west_id = west['teamId']
                tmp_row = {
                    'east_name': self.team_id_dict[east_id]['short_name'],
                    'east_nick': self.team_id_dict[east_id]['med_name'],
                    'east_sub': self.team_id_dict[east_id]["sub"],
                    'east_record': east['win'] + '-' + east['loss'],
                    'east_gb_conf': '%.1f' % int(east['gamesBehind']),
                    'east_div_rank': east['divRank'],
                    'conf_rank': str(i + 1),
                    'west_name': self.team_id_dict[west_id]['short_name'],
                    'west_nick': self.team_id_dict[west_id]['med_name'],
                    'west_sub': self.team_id_dict[west_id]["sub"],
                    'west_record': west['win'] + '-' + west['loss'],
                    'west_gb_conf': '%.1f' % int(west['gamesBehind']),
                    'west_div_rank': west['divRank']
                }
                standings[int(i + 1)] = tmp_row

        return standings

    def get_playoffs(self):
        bracket = collections.OrderedDict()
        with urlopen('https://data.nba.com/data/10s/prod/v1/2017/playoffsBracket.json') as url:
            j = json.loads(url.read().decode())

            for i in range(0, 15):
                series = j['series'][i]
                series_name = str(i + 1)
                series_winner = series['summaryStatusText'][:3]

                top_seed = series['topRow']['teamId']
                bottom_seed = series['bottomRow']['teamId']

                if series_winner == self.team_id_dict[top_seed]['short_name']:
                    series_record = series['summaryStatusText'][-3:].replace("-", " - ")
                else:
                    series_record = series['summaryStatusText'][-3:].replace("-", " - ")[::-1]

                tmp_brkt = {
                    'series': series['confName'] + " R" + series['roundNum'],
                    'top_name': self.team_id_dict[top_seed]['short_name'],
                    'top_seed': series['topRow']['seedNum'],
                    'top_sub': self.team_id_dict[top_seed]["sub"],
                    'bottom_name': self.team_id_dict[bottom_seed]['short_name'],
                    'bottom_seed': series['bottomRow']['seedNum'],
                    'bottom_sub': self.team_id_dict[bottom_seed]["sub"],
                    'summary': series_record
                }

                bracket[series_name] = tmp_brkt

                if j['series'][14]:
                    if series["topRow"]["isSeriesWinner"] or series["bottomRow"]["isSeriesWinner"]:
                        bracket['16'] = {
                            'champ_name': series_winner,
                            'champ_sub': self.team_abbrev_dict[series_winner]["sub"],
                        }
                    else:
                        bracket['16'] = {
                            'champ': "NA"
                        }

        return bracket

    def __init__(self):
        self.json_teams = None
        self.load_teams()
        self.bot = praw.Reddit(client_id=config.client_id, client_secret=config.client_secret,
                               user_agent=config.user_agent, username=config.username, password=config.password)

    # Helper functions
    def load_teams(self):
        self.team_id_dict = {}
        self.team_name_dict = {}
        self.team_abbrev_dict = {}
        with open('data/teams.csv', 'r') as teamInfoFile:
            for teamInfoRow in teamInfoFile.read().split('\n'):
                teamInfo = teamInfoRow.split(',')
                tmp_team_id_dict = {
                    'long_name': teamInfo[0] + ' ' + teamInfo[1],
                    'med_name': teamInfo[1],
                    'short_name': teamInfo[2].upper(),
                    'sub': teamInfo[3],
                    'timezone': teamInfo[4],
                    'division': teamInfo[5],
                    'conference': teamInfo[6],
                    'id': teamInfo[7]
                }
                self.team_id_dict[teamInfo[7]] = tmp_team_id_dict
                self.team_name_dict[teamInfo[1]] = tmp_team_id_dict
                self.team_abbrev_dict[teamInfo[2].upper()] = tmp_team_id_dict
        self.teams = []
        for team, team_data in self.team_abbrev_dict.items():
            self.teams.append((team, team_data['med_name']))


if __name__ == "__main__":
    main()
