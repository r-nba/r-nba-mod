import praw
import config
import data
import markdown
import datetime
def main():
    reddit = praw.Reddit(client_id=config.client_id, client_secret=config.client_secret, user_agent=config.user_agent, username=config.username, password=config.password)
    updated_sidebar = create_sidebar(reddit)
    update_sidebar(reddit, updated_sidebar)
    create_game_threads(reddit)

def create_sidebar(reddit):
    curr_sidebar_lines = reddit.subreddit('nbadev').wiki['edit_sidebar'].content_md.split('\n')
    M = markdown.markdown()
    D = data.data()

    updated_sidebar = ""
    for line in curr_sidebar_lines:
        if not line.startswith("//"):
            if line.startswith("$team_subreddits"):
                updated_sidebar += '\n' + M.team_subreddits(D.team_subreddits())
            elif line.startswith("$schedule"):
                updated_sidebar += '\n' + M.schedule(D.schedule())
            elif line.startswith("$game_thread_bar"):
                updated_sidebar += '\n' + M.top_bar(D.top_bar())
            elif line.startswith("$standings"):
                updated_sidebar += '\n' + M.standings(D.standings())
            elif line.startswith("$playoffs"):
                updated_sidebar += '\n' + M.playoffs(D.playoffs())
            else:
                updated_sidebar += line + "\n"

    return updated_sidebar

def update_sidebar(reddit, updated_sidebar):
    sidebar_page = reddit.subreddit('nbadev').wiki['edit_sidebar']
    print(updated_sidebar)
    reddit.subreddit('nbadev').wiki['config/sidebar'].edit(content=updated_sidebar)

def create_game_threads(reddit):
    D = data.data()
    games = D.top_bar()
    team_dict = D.team_abbrev_dict
    for game in games:
        if (datetime.datetime.now() + datetime.timedelta(hours=2)) > game['threadtime']:
            if game['thread_created'] == False:
                thread_name =  "[GAME THREAD] " + team_dict[game['vTeamCode']]['long_name']+ ' at ' + team_dict[game['hTeamCode']]['long_name']
                reddit.subreddit('nbadev').submit(thread_name, selftext='')
                game['thread_created'] = True

if __name__ == "__main__":
    main()