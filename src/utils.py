from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random

from twitter import Twitter, OAuth
from model import Quote, Base
from config import Config
from sqlalchemy import func


class NoMoreQuotesException(Exception):
    pass


def connect_sql():
    engine = create_engine(Config.PostgreURI)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def random_quote(session):
    try:
        # There are obviously better ways of handling this.
        # But this is supposed to scale well up to the ~500Ks.
        # And let's face it, we'll NEVER get to this point.
        # So... let's use this.
        q = session.query(Quote).filter(Quote.used==False)
        count = int(q.count())
        result = q.offset(int(count*random.random())).first()
    except Exception as exc:
        raise NoMoreQuotesException('Ran out of quotes !')
    return result


def twitter_connect():
    return Twitter(auth=OAuth(Config.token,
                              Config.token_secret,
                              Config.consumer_key,
                              Config.consumer_secret))


def tweet(txt):
    conn = twitter_connect()
    conn.statuses.update(status=txt)


def create_db():
    engine = create_engine(Config.PostgreURI)
    Base.metadata.create_all(engine)
