import praw
import config
import data
import markdown
import datetime
import calendar
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
from pprint import pprint


class NBA_MOD:

    bot_name = 's4njee'

    def __init__(self):
        reddit = praw.Reddit(client_id=config.client_id, client_secret=config.client_secret, user_agent=config.user_agent,
                             username=config.username, password=config.password)
        # updated_sidebar = create_sidebar(reddit)
        # update_sidebar(reddit, updated_sidebar)

        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)
        self.D = data.data()
        self.M = markdown.markdown()
        self.update_games_daily()
        self.day = datetime.datetime.today().strftime('%Y%m%d')
        self.update_games_minutely()
        self.sched = BlockingScheduler()
        for game in self.games:
            if game['thread_id']:
                submission = reddit.submission(id=game['thread_id'])
                if submission.author.name == self.bot_name:
                    self.sched.add_job(self.update_game_thread, "interval", [submission, game['home'], game['away']], id=game['thread_id'], minutes=1, end_date=game['threadtime']+datetime.timedelta(hours=4), max_instances=12)
                    game['thread_created'] = True
        self.sched.add_job(self.create_game_threads, "interval", [reddit], minutes=1, max_instances=8)
        self.sched.add_job(self.create_sidebar, 'interval', [reddit], minutes=1, max_instances=8)
        self.sched.add_job(self.update_games_daily, "cron", hour=12)
        self.sched.add_job(self.update_games_minutely, "interval", minutes=1)
        self.sched.start()
        submissions = []


    def create_sidebar(self, reddit):
        curr_sidebar_lines = reddit.subreddit('nbadev').wiki['edit_sidebar'].content_md.split('\n')
        updated_sidebar = ""
        for line in curr_sidebar_lines:
            if not line.startswith("//"):
                if line.startswith("$team_subreddits"):
                    updated_sidebar += '\n' + self.M.team_subreddits(self.D.team_subreddits())
                elif line.startswith("$schedule"):
                    updated_sidebar += '\n' + self.M.create_schedule(self.D.get_schedule())
                elif line.startswith("$game_thread_bar"):
                    updated_sidebar += '\n' + self.M.create_game_bar(self.current_games)
                elif line.startswith("$standings"):
                    updated_sidebar += '\n' + self.M.create_standings(self.D.get_standings())
                elif line.startswith("$playoffs"):
                    updated_sidebar += '\n' + self.M.create_playoffs(self.D.get_playoffs())
                else:
                    updated_sidebar += line + "\n"
        reddit.subreddit('nbadev').wiki['config/sidebar'].edit(content=updated_sidebar)


    def update_sidebar(self, reddit, updated_sidebar):
        sidebar_page = reddit.subreddit('nbadev').wiki['edit_sidebar']
        print(updated_sidebar)
        reddit.subreddit('nbadev').wiki['config/sidebar'].edit(content=updated_sidebar)

    def create_game_threads(self, reddit):
        team_dict = self.D.team_abbrev_dict
        for game in self.games:
            if (datetime.datetime.now() + datetime.timedelta(hours=2)) > game['threadtime']:
                if game['thread_created'] == False:
                    date = datetime.datetime.today()
                    month = calendar.month_name[date.month]
                    calendar_day = calendar.day_name[date.weekday()]
                    date = calendar_day + ", " + month + " " + date.strftime('%d')
                    visiting_team = team_dict[game['away']]['long_name'] + ' (' + game['away_win'] + '-' + game[
                        'away_loss'] + ')'
                    home_team = team_dict[game['home']]['long_name'] + ' (' + game['home_win'] + '-' + game[
                        'home_loss'] + ')'
                    thread_name = "[GAME THREAD] {0} at {1} - ({2})".format(visiting_team, home_team, date)
                    submission = reddit.subreddit('nbadev').submit(thread_name, selftext='', flair_id='fea08cec-69cf-11e8-9dba-0e75baaabcce')
                    end_time = game['threadtime'] + datetime.timedelta(hours=4)
                    job = self.sched.add_job(self.update_game_thread, "interval", [submission, game['home'], game['away']], id=game['thread_id'], minutes=1, end_date=end_time, max_instances=12)
                    game['thread_created'] = True

    def update_game_thread(self, submission, hteam, vteam):
        submission_text = self.M.generate_thread_markdown(self.current_games, hteam, vteam)
        if submission_text != '':
            submission.edit(submission_text)

    def update_games_daily(self):
        self.games = self.D.get_games()
        self.day = datetime.datetime.today().strftime('%Y%m%d')

    def update_games_minutely(self):
        self.current_games = self.D.get_games(self.day)
NBA = NBA_MOD()
