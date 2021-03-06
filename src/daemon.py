# *-* coding:utf-8 *-*
import datetime
import logging
import time
from utils import (
    random_quote, connect_sql, tweet, get_mention_timeline,
    get_tweet_by_id, tweet_answer)
from model import Quote


class BotDaemon(object):
    MORNING = 9
    NOON = 12
    AFTERNOON = 17
    EVENING = 21
    MAX_TWEETS_PER_HOUR = 20

    def __init__(self, last_poll=None):
        self.flags = {self.MORNING: True,
                      self.NOON: True,
                      self.AFTERNOON: True,
                      self.EVENING: True}
        self.previous_hour_posting = -1
        self.posted_message_last_hour = 0
        self.last_poll = datetime.datetime.utcnow()
        if last_poll is not None:
            timedelta = datetime.timedelta(minutes=last_poll)
            self.last_poll = datetime.datetime.utcnow() - timedelta

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
            self.previous_hour_posting = hour

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
        try:
            tweet(quote.to_tweet_string())
        except:
            logging.error("Could not tweet : %s, too long." % quote.to_tweet_string())
        finally:
            session.close()

    def answer_when(self, tweet_id):
        q_tweet = get_tweet_by_id(tweet_id)
        quote = q_tweet[q_tweet.find(u'«')+1:q_tweet.find(u'»')].strip()
        session = connect_sql()
        try:
            logging.info("Looking for quote %s" % quote)
            quote= session.query(Quote).filter_by(content=quote).one()
            answer = quote.to_date_string()
            logging.info("Found it !  %s" % answer)
        except Exception as exc:
            logging.error("Could not find it. Error : %s" % exc)
            answer = None
        finally:
            session.close()
        return answer

    def check_interaction(self):
        try:
            interactions = get_mention_timeline(self.last_poll)
        except Exception:
            return
        for i in interactions:
            txt = i['text'].lower()
            logging.info('Received tweet ! %s' % txt)
            if txt.find('quand'):
                date_to_answer = self.answer_when(i['in_reply_to_status_id'])
                if date_to_answer:
                    full_tweet = '@%s: %s' % (i['user']['screen_name'],
                                              date_to_answer)
                    tweet_answer(full_tweet, i['id'])
                    self.posted_message_last_hour += 1
        self.last_poll = datetime.datetime.utcnow()


def run_daemon():
    b = BotDaemon()
    b.loop()
