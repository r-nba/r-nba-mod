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

    # Input dictionary containing live game scores
    # Output: Markdown for game score bar
    def create_game_bar(self, game_bar_elements):
        text = """> \n* [Reddit](//www.reddit.com)\n* [Player Flair Tool](//www.nbaflairbot.herokuapp.com/)\n* [](#A) [Free Agency Tracker](https://www.reddit.com/r/nba/6j2ts)\n"""
        for game in game_bar_elements:
            home_score = ""
            away_score = ""
            if game['home_score']:
                home_score = "["+game['home_score']+"](#HS)"
                away_score = "["+game['away_score']+"](#HS)"
                if int(game['home_score']) > int(game['away_score']):
                    game['home'] = "**" + game['home'] + "**"
                elif int(game['home_score']) < int(game['away_score']):
                    game['away']  = "**" + game['away'] + "**"

            text += """* [{0}]({1}) [{2}](#GH) [{3}](#GV) {4} {5}\n""" \
                .format(game['time'],game['thread_link'], game['away'], game['home'], away_score, home_score)
        text += '*  \n'
        return text

    def create_standings(self, dict_standings):
        text = """###[](//)\n\n##[](//)\n\n|WEST|W - L|GB||GB|W - L|EAST\n:-:|:-:|:-:|:-:|:-:|:-:|:-:\n"""
        for rank,value in dict_standings.items():
            text += """[{west_name}](/r/{west_sub})|{west_record}|{west_gb_conf}|{conf_rank}|{east_gb_conf}|{east_record}|[{east_name}](/r/{east_sub})\n""".format(**value)
        return text

    def generate_thread_markdown(self, games, hteam, vteam):
        text = ''
        for game in games:
            if game['home'] == hteam and game['away'] == vteam:
                text += '[{away_long}](/r/{away_subreddit}) Score: {away_score}\n'.format(**game)
                text += '[{home_long}](/r/{home_subreddit}) Score: {home_score}\n'.format(**game)
        return text


    # Input dictionary containing upcoming schedule data
    # {"Tuesday": [{gameinfo},{gameinfo}], "Wednesday": [{gameinfo},{gameinfo}], "Thursday": [{gameinfo},{gameinfo}]]
    # Output: Markdown for schedule
    def create_schedule(self, dict_schedule):
        line = '###[](//)\n######[](//)\n\n'
        for k, day in dict_schedule.items():
            line += """[{0}| ET](/date)\n""".format(k)
            line += """|||\n:--|:-:\n"""
            for game in day:
                # Unpacks all keys in game into format tags: eg. game['time'] unpacked to {time}
                line += """[{time}](/tgt)|[{home}](/r/{home_subreddit}) at [{away}](/r/{away_subreddit})\n""" \
                    .format(**game)
        return line

    def create_playoffs(self, dict_playoffs):
        text = """###[](//)\n\n####[](//)\n\n||||||||\n:-:|:-:|:-:|:-:|:-:|:-:|:-:\n**1***8*||**4***5*||**3***6*||**2***7*\n"""

        # West Round 1
        for i in range(1,5):
            text += """[](/r/{top_sub})[](/r/{bottom_sub})||""".format(**dict_playoffs[str(i)])
        text = text[:-2] + "\n"
        for i in range(1,5):
            text += """**{top_name}** {summary} *{bottom_name}*||""".format(**dict_playoffs[(str(i))])
        text = text[:-2] + "\n\n"

        # West Round 2
        text += """||||\n:-:|:-:|:-:\n"""
        for i in range(9,11):
            text += """[](/r/{top_sub})[](/r/{bottom_sub})||""".format(**dict_playoffs[(str(i))])
        text = text[:-2] + "\n"
        for i in range(9,11):
            text += """**{top_name}** {summary} *{bottom_name}*||""".format(**dict_playoffs[(str(i))])
        text = text[:-2] + "\n\n"

        #WCF
        text += """||||||||||\n:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:\n"""
        text += """|||[](/r/{top_sub})||**{top_name}** {summary} *{bottom_name}*||[](/r/{bottom_sub})||\n|\n""".format(**dict_playoffs['13'])

        #Finals
        text += """|||||[{top_name}](/r/{top_sub})|||\n""".format(**dict_playoffs['15'])
        text += """[{champ_name}](/r/{champ_sub})|[<-- CHAMP](/CHAMP)""".format(**dict_playoffs['16'])
        text += """|||**{top_name}** {summary} *{bottom_name}*||||\n""".format(**dict_playoffs['15'])
        text += """|||||[{bottom_name}](/r/{bottom_sub})||||\n|\n""".format(**dict_playoffs['15'])

        #ECF
        text += """|||[](/r/{top_sub})||**{top_name}** {summary} *{bottom_name}*||[](/r/{bottom_sub})||""".format(**dict_playoffs['14'])

        #East Round 2
        text += """\n\n||||\n:-:|:-:|:-:\n"""
        for i in range(11,13):
            text += """**{top_name}** {summary} *{bottom_name}*||""".format(**dict_playoffs[(str(i))])
        text = text[:-2] + "\n"
        for i in range(11,13):
            text += """[](/r/{top_sub})[](/r/{bottom_sub})||""".format(**dict_playoffs[(str(i))])
        text = text[:-2] + "\n"

        #East Round 1
        text += """\n||||||||\n:-:|:-:|:-:|:-:|:-:|:-:|:-:\n"""
        for i in range(5,9):
            text += """**{top_name}** {summary} *{bottom_name}*||""".format(**dict_playoffs[(str(i))])
        text = text[:-2] + "\n"
        for i in range(5,9):
            text += """[](/r/{top_sub})[](/r/{bottom_sub})||""".format(**dict_playoffs[str(i)])
        text = text[:-2] + "\n"


        text += """**1***8*||**4***5*||**3***6*||**2***7*\n"""
        return text
