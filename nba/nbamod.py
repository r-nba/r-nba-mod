import praw
import config

def main():
    reddit = praw.Reddit(client_id=config.client_id, client_secret=config.client_secret, user_agent=config.user_agent, username=config.username, password=config.password)

    updated_sidebar = create_sidebar(reddit)
    update_sidebar(reddit, updated_sidebar)

def create_sidebar(reddit):
    curr_sidebar_lines = reddit.subreddit('nba').wiki['edit_sidebar'].content_md.split('\n')
    updated_sidebar = ""
    for line in curr_sidebar_lines:
        if not line.startswith("//"): 
            if line.startswith("$team_subreddits"):
                updated_sidebar += line + "\n"
            elif line.startswith("$schedule"):
                updated_sidebar += line + "\n"
            elif line.startswith("$game_threads"):
                updated_sidebar += line + "\n"
            elif line.startswith("$game_thread_bar"):
                updated_sidebar += line + "\n"
            elif line.startswith("$standings"):
                updated_sidebar += line + "\n"
            elif line.startswith("$playoffs"):
                updated_sidebar += line + "\n"
            else:
                updated_sidebar += line + "\n"

    return updated_sidebar

def update_sidebar(reddit, updated_sidebar):
    sidebar_page = reddit.subreddit('nbadev').wiki['edit_sidebar']
    print(updated_sidebar)
    sidebar_page.edit(updated_sidebar)

if __name__ == "__main__":
    main()