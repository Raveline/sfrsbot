import datetime
import time
from utils import random_quote, connect_sql, tweet


class BotDaemon(object):
    MORNING = 9
    NOON = 12
    AFTERNOON = 17
    EVENING = 21
    MAX_TWEETS_PER_HOUR = 20

    def __init__(self):
        self.flags = {self.MORNING: True,
                      self.NOON: True,
                      self.AFTERNOON: True,
                      self.EVENING: True}
        self.previous_hour_posting = -1
        self.posted_message_last_hour = 0

    def reset_flags(self):
        for f in self.flags:
            self.flags[f] = True

    def should_i_tweet_now(self, hour):
        return self.flags.get(hour, False)

    def reset_hour(self, new_hour):
        self.previous_hour_posting = new_hour
        self.posted_message_last_hour = 0

    def loop(self):
        while True:
            self.real_loop()

    def real_loop(self):
        hour = datetime.datetime.now().hour

        # Did we pass an hour ?
        if hour != self.previous_hour_posting:
            # Check if this is a new day, a new dawn, etc.
            if hour < self.previous_hour_posting:
                # Yup. We came from 23 to 0.
                self.reset_flags()
            # In any case, reset the tweets / hour limit
            self.previous_hour_posting()

        if self.should_i_tweet_now(hour):
            self.post_random_tweet()
            # Now that it's done, let's put it as false !
            self.flags[hour] = False
        elif self.posted_message_last_hour < self.MAX_TWEETS_PER_HOUR:
            self.check_interaction()

        # Sleep for 10 minutes
        time.sleep(600)

    def post_random_tweet(self):
        session = connect_sql()
        quote = random_quote(session)
        quote.used = True
        session.commit()
        session.close()
        tweet(quote.to_tweet_string())

    def check_interaction(self):
        pass


def run_daemon():
    b = BotDaemon()
    b.loop()
