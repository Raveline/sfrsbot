from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
        result = session.query(Quote).filter_by(used=False).\
            filter_by(func.random() > 0.1).limit(1).first()
    except Exception:
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
