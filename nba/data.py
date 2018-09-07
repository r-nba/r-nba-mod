from urllib.request import urlopen
import json
import datetime
import calendar
import collections

def main():
    d = data()
    d.top_bar()

class data:
    def team_subreddits(self):
        return [{"team_abbrev":abbrev, "subreddit":self.team_abbrev_dict[abbrev]["sub"]} for abbrev in self.team_abbrev_dict]

    def schedule(self):
        days = {}
        for delta in range(3):
            date = (datetime.datetime.today()+datetime.timedelta(days=delta))
            month = calendar.month_name[date.month]
            calendar_day = calendar.day_name[date.weekday()]
            key = calendar_day + ", " + month + " " + date.strftime('%d')
            parameter = date.strftime('%Y%m%d')
            parameter = str(20180928 + delta) # This line is for testing purposes. Date is set to first day of preseason
            #print(key)
            #print(parameter)
            games = []
            with urlopen('http://data.nba.com/prod/v2/' + parameter + '/scoreboard.json') as url:
                j = json.loads(url.read().decode())
                for game in j["games"]:
                    if game["vTeam"]["teamId"] not in self.team_id_dict or game["hTeam"]["teamId"] not in self.team_id_dict: # Games against non-nba teams are disregarded
                        continue
                    gameDetails = {}
                    gameDetails["time"] = game["startTimeEastern"].replace(" ET", "")
                    gameDetails["home"] = game["hTeam"]["triCode"]
                    gameDetails["home_subreddit"] = self.team_id_dict[game["hTeam"]["teamId"]]["sub"]
                    gameDetails["away"] = game["vTeam"]["triCode"]
                    gameDetails["away_subreddit"] = self.team_id_dict[game["vTeam"]["teamId"]]["sub"]
                    #print(gameDetails)
                    games.append(gameDetails)
            #print(games)
            days[key] = games

        #print(days)

        return days

    def game_threads(self):
        return ""

    def top_bar(self): # Check Bre's work on r/nbadev if you don't know what this is
        games = []
        parameter = datetime.datetime.today().strftime('%Y%m%d')
        #parameter = str(20180314) # This line is for testing purposes. Date is set to March 14th, 2018.
        parameter = str(20180928) # This line is for testing purposes. Date is set to March 14th, 2018.
        
        with urlopen('http://data.nba.com/prod/v2/' + parameter + '/scoreboard.json') as url:
            j = json.loads(url.read().decode())
            for game in j["games"]:
                if game["vTeam"]["teamId"] not in self.team_id_dict or game["hTeam"]["teamId"] not in self.team_id_dict: # Games against non-nba teams are disregarded
                    continue
                gameDetails = {}
                if game["statusNum"] == 1: # Game hasn't started
                    gameDetails["time"] = game["startTimeEastern"].replace(" ET", "")
                elif game["statusNum"] == 2: # Game in progress
                    gameDetails["time"] = game["clock"] + " " + game["period"]["current"] + "Q"
                elif game["statusNum"] == 3: # Game completed
                    gameDetails["time"] = "FINAL"
                gameDetails["home"] = game["hTeam"]["triCode"]
                gameDetails["away"] = game["vTeam"]["triCode"]
                if not game["statusNum"] == 1:
                    gameDetails["home_score"] = game["hTeam"]["score"]
                    gameDetails["away_score"] = game["vTeam"]["score"]
                else:
                    gameDetails["home_score"] = ""
                    gameDetails["away_score"] = ""
                #print(gameDetails)
                games.append(gameDetails)
        print(games)
        return games

    def standings(self):
        standings = {}
        with urlopen('http://data.nba.com/prod/v1/current/standings_conference.json') as url:
            j = json.loads(url.read().decode())

            for i in range(0,15):
                east = j['league']['standard']['conference']['east'][i]
                east_id = east['teamId']
                west = j['league']['standard']['conference']['west'][i]
                west_id = west['teamId']
                tmp_row = {
                    'east_name': self.team_id_dict[east_id]['short_name'],
                    'east_nick': self.team_id_dict[east_id]['med_name'],
                    'east_record': east['win'] + '-' + east['loss'],
                    'east_gb_conf': '%.1f' % int(east['gamesBehind']),
                    'east_div_rank': east['divRank'],
                    'conf_rank': str(i+1),
                    'west_name': self.team_id_dict[west_id]['short_name'],
                    'west_nick': self.team_id_dict[west_id]['med_name'],
                    'west_record': west['win'] + '-' + west['loss'],
                    'west_gb_conf': '%.1f' % int(west['gamesBehind']),
                    'west_div_rank': west['divRank']
                }
                standings[int(i+1)] = tmp_row
        return standings

    def playoffs(self):
        bracket = collections.OrderedDict()
        with urlopen('https://data.nba.com/data/10s/prod/v1/2017/playoffsBracket.json') as url:
            j = json.loads(url.read().decode())

            for i in range(0,15):
                series = j['series'][i]
                series_name = str(i+1)
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
                    'bottom_name': self.team_id_dict[bottom_seed]['short_name'],
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

    def __init__(self):        
        self.json_teams = None
        self.load_teams()

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

if __name__ == "__main__":
    main()