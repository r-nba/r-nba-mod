import logging
import time
from datetime import datetime, timedelta, time as dttime
from data import data
from markdown import markdown

class nba_bot(object):
    def post_index_thread(self):
        pass

    def update_index_thread(self):
        pass

    def test_framework(self):
        print('Hello World!')

    def create_legacy_standings(self):
        legacy_markdown = markdown.get_legacy_standings(self.data.standings)

    def create_widget_standings(self):
        widget_markdown = markdown.get_widget_standings(self.data.standings)

    def __init__(self):
        self.data = data()

def run_nba():
    bot = nba_bot()
    run_updates = True
    consecutive_error_count = 0
    while run_updates:
        try:
            bot.create_legacy_standings()
            update_freq = 60 * 10
            consecutive_error_count = 0
        except KeyboardInterrupt as e:
            logging.error("keyboard interrupt. Stopping bot")
            logging.exception(e)
            raise
        except BaseException as e:
            consecutive_error_count += 1
            logging.exception(e)
            logging.warning("an error occurred during schedule creation " + str(consecutive_error_count) +
                            " consecutive errors")
            update_freq = 60    # try again in one minutes
            if consecutive_error_count > 10:
                logging.warning("too many consecutive errors. exiting.")
                run_updates = False
                update_freq = 0
                raise
        logging.info("sleeping for " + str(timedelta(seconds=update_freq)) + " ... ... ...")
        time.sleep(update_freq)

if __name__ == "__main__":
    run_nba()
