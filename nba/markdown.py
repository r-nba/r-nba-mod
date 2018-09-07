class markdown:

    # Input: dictionary containing team subreddits
    # [{'team_abbrev':'DAL', 'subreddit':'/r/mavericks'}, {'team_abbrev':'DEN', 'subreddit':'/r/denvernuggets'},...]
    # Output: Markdown for team subreddits
    def team_subreddits(self, dict_team_subs):
        team_subs = ''
        for team in dict_team_subs:
            # Unpacks team['subreddit'] into {subreddit}
            team_subs += """* []({subreddit})\n""".format(**team)
        return team_subs

    # Input dictionary containing upcoming schedule data
    # {"Tuesday": [{gameinfo},{gameinfo}], "Wednesday": [{gameinfo},{gameinfo}], "Thursday": [{gameinfo},{gameinfo}]]
    # Output: Markdown for schedule
    def schedule(self, dict_schedule):
        line = ''
        for k, day in dict_schedule.items():
            line += """[{0}| ET](/date)\n""".format(k)
            line += """|||\n:--|:-:\n"""
            for game in day:
                # Unpacks all keys in game into format tags: eg. game['time'] unpacked to {time}
                line += """[{time}](/tgt)|[{home}](/r/{home_subreddit}) at [{away}](/r/{away_subreddit})\n""" \
                    .format(**game)
        return line

    # Input dictionary containing live game scores
    # Output: Markdown for game score bar
    def top_bar(self, top_bar_elements):
        text = """> \n* [](http://reddit.com)\n* [](http://nba-mod-bot.herokuapp.com/)\n* [](#A) [Free Agency Tracker]\n"""
        for game in top_bar_elements:
            home_score = ""
            away_score = ""
            if game['home_score']:
                home_score = "["+game['home_score']+"](#HS)"
                away_score = "["+game['away']+"](#HS)"
                if int(home_score) > int(away_score):
                    game['home'] = "**" + game['home'] + "**"
                elif int(home_score) < int(away_score):
                    game['away']  = "**" + game['away'] + "**"

            text += """* [{0}](#GT) [{1}](#GH) [{2}](#GV) {3} {4}""" \
                .format(game['time'], game['home'], game['away'], home_score, away_score)
        return text

    def standings(self, dict_standings):
        text = """WEST|W - L|GB||GB|W - L|EAST\n:-:|:-:|:-:|:-:|:-:|:-:|:-:\n"""
        for rank,value in dict_standings.items():
            text += """[{west_name}](/r/)|{west_record}|{west_gb_conf}|{conf_rank}|{east_gb_conf}|{east_record}|[{east_name}](/r/)\n""".format(**value)
        return text



    def playoffs(self, dict_playoffs):
        text = """####[](//)\n\n||||||||\n:-:|:-:|:-:|:-:|:-:|:-:|:-:\n**1***8*||**4***5*||**3***6*||**2***7*"""
        for k,v in dict_playoffs.items():
            text += """[](/r/{top_sub})[](/r/{bottom_sub})||[](/r/thunder)[](/r/utahjazz)||[](/r/ripcity)[](/r/nolapelicans)||[](/r/warriors)[](/r/nbaspurs)
**HOU** 4 - 1 *MIN*||**OKC** 2 - 4 *UTA*||**POR** 0 - 4 *NOP*||**GSW** 4 - 1 *SAS*"""


    # Helper functions
    def get_legacy_standings(self, dict_standings):
        legacy_standings = 'WEST|||EAST|||\n:---:|:---:|:---:|:---:|:---:|:---:\n**TEAM**|*W/L*|*GB*|**TEAM**|*W/L*|*GB*\n'

        for i in range(0, 15):
            standings = dict_standings[i + 1]
            if i < 8:
                legacy_standings = legacy_standings + standings['conf_rank'] + ' [](/' + standings['west_name'] + ')|' + \
                                   standings['west_record'] + '|' + standings['west_gb_conf'] + '|' + standings[
                                       'conf_rank'] + ' [](/' + standings['east_name'] + ')|' + standings[
                                       'east_record'] + '|' + standings['east_gb_conf'] + '\n'
            else:
                legacy_standings = legacy_standings + '[](/' + standings['west_name'] + ')|' + standings[
                    'west_record'] + '|' + standings['west_gb_conf'] + '|[](/' + standings['east_name'] + ')|' + \
                                   standings['east_record'] + '|' + standings['east_gb_conf'] + '\n'

        return legacy_standings

    def get_widget_standings(self, dict_standings):
        widget_standings = '- \n - \n     - west\n     - W - L\n     - GB\n     - GB\n     - W - L\n     - east\n\n'

        for i in range(0, 15):
            standings = dict_standings[i + 1]
            widget_standings = widget_standings + '- \n - \n     - [](/' + standings['west_name'] + ')\n     - ' + \
                               standings['west_gb_conf'] + '\n     - ' + standings['west_record'] + '\n - ' + standings[
                                   'conf_rank'] + '\n - [](/#)\n     - [](/' + standings['east_name'] + ')\n     - ' + \
                               standings['east_gb_conf'] + '\n     - ' + standings['east_record'] + '\n\n'

        return widget_standings

    def get_widget_bracket(self, dict_bracket):
        bracket = dict_bracket

        widget_bracket = (
                    "- \n - \n     - 1\n     - 8\n - \n     - 4\n     - 5\n - \n     - 3\n     - 6\n - \n     - 2\n     - 7\n\n" +
                    "- \n - \n     - [](/" + bracket['1']['top_name'] + ")\n     - [](/" + bracket['1'][
                        'bottom_name'] + ")\n" +
                    " - \n     - [](/" + bracket['2']['top_name'] + ")\n     - [](/" + bracket['2'][
                        'bottom_name'] + ")\n - \n" +
                    "     - [](/" + bracket['3']['top_name'] + ")\n     - [](/" + bracket['3'][
                        'bottom_name'] + ")\n - \n  " +
                    "   - [](/" + bracket['4']['top_name'] + ")\n     - [](/" + bracket['4']['bottom_name'] + ")\n\n" +
                    "- \n - \n     - " + bracket['1']['top_name'] + "\n     - " + bracket['1'][
                        'summary'] + "\n     - " + bracket['1']['bottom_name'] +
                    "\n - \n     - " + bracket['2']['top_name'] + "\n     - " + bracket['2']['summary'] + "\n     - " +
                    bracket['2']['bottom_name'] +
                    "\n - \n     - " + bracket['3']['top_name'] + "\n     - " + bracket['3']['summary'] + "\n     - " +
                    bracket['3']['bottom_name'] +
                    "\n - \n     - " + bracket['4']['top_name'] + "\n     - " + bracket['4']['summary'] + "\n     - " +
                    bracket['4']['bottom_name'] + "\n\n" +
                    "- \n - \n     - [](/" + bracket['9']['top_name'] + ")\n     - [](/" + bracket['9'][
                        'bottom_name'] + ")\n" +
                    " - \n     - [](/" + bracket['10']['top_name'] + ")\n     - [](/" + bracket['10'][
                        'bottom_name'] + ")\n\n" +
                    "- \n - \n     - " + bracket['9']['top_name'] + "\n     - " + bracket['9'][
                        'summary'] + "\n     - " + bracket['9']['bottom_name'] +
                    "\n - \n     - " + bracket['10']['top_name'] + "\n     - " + bracket['10'][
                        'summary'] + "\n     - " + bracket['10']['bottom_name'] + "\n\n" +
                    "- \n - \n     - [](/" + bracket['13']['top_name'] + ")\n - \n     - " + bracket['13'][
                        'top_name'] + "\n     - " + bracket['13']['summary'] +
                    "\n     - " + bracket['13']['bottom_name'] + "\n - \n     - [](/" + bracket['13'][
                        'bottom_name'] + ")\n\n" +
                    "- \n - \n     - [](/" + bracket['15']['top_name'] + ")\n\n" +
                    "- \n - \n     - [](/" + bracket['16']['champ'] + ")\n - \n     - " + bracket['15'][
                        'top_name'] + "\n     - " + bracket['15']['summary'] +
                    "\n     - " + bracket['15']['bottom_name'] + "\n\n- \n - \n     - [](/" + bracket['15'][
                        'bottom_name'] + ")\n\n" +
                    "- \n - \n     - [](/" + bracket['14']['top_name'] + ")\n - \n     - " + bracket['14']['top_name'] +
                    "\n     - " + bracket['14']['summary'] + "\n     - " + bracket['14'][
                        'bottom_name'] + "\n - \n     - [](/" + bracket['14']['bottom_name'] + ")\n\n" +
                    "- \n - \n     - " + bracket['11']['top_name'] + "\n     - " + bracket['11'][
                        'summary'] + "\n     - " + bracket['11']['bottom_name'] +
                    "\n - \n     - " + bracket['12']['top_name'] + "\n     - " + bracket['12'][
                        'summary'] + "\n     - " + bracket['12']['bottom_name'] + "\n\n" +
                    "- \n - \n     - [](/" + bracket['11']['top_name'] + ")\n     - [](/" + bracket['11'][
                        'bottom_name'] + ")\n" +
                    " - \n     - [](/" + bracket['12']['top_name'] + ")\n     - [](/" + bracket['12'][
                        'bottom_name'] + ")\n\n" +
                    "- \n - \n     - " + bracket['5']['top_name'] + "\n     - " + bracket['5'][
                        'summary'] + "\n     - " + bracket['5']['bottom_name'] +
                    "\n - \n     - " + bracket['6']['top_name'] + "\n     - " + bracket['6']['summary'] + "\n     - " +
                    bracket['6']['bottom_name'] +
                    "\n - \n     - " + bracket['7']['top_name'] + "\n     - " + bracket['7']['summary'] + "\n     - " +
                    bracket['7']['bottom_name'] +
                    "\n - \n     - " + bracket['8']['top_name'] + "\n     - " + bracket['8']['summary'] + "\n     - " +
                    bracket['8']['bottom_name'] + "\n\n" +
                    "- \n - \n     - [](/" + bracket['5']['top_name'] + ")\n     - [](/" + bracket['5'][
                        'bottom_name'] + ")\n" +
                    " - \n     - [](/" + bracket['6']['top_name'] + ")\n     - [](/" + bracket['6'][
                        'bottom_name'] + ")\n - \n" +
                    "     - [](/" + bracket['7']['top_name'] + ")\n     - [](/" + bracket['7'][
                        'bottom_name'] + ")\n - \n  " +
                    "   - [](/" + bracket['8']['top_name'] + ")\n     - [](/" + bracket['8']['bottom_name'] + ")\n\n" +
                    "- \n - \n     - 1\n     - 8\n - \n     - 4\n     - 5\n - \n     - 3\n     - 6\n - \n     - 2\n     - 7")

        return widget_bracket



