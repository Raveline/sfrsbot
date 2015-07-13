import locale
import datetime

from sqlalchemy.orm.exc import NoResultFound

from utils import connect_sql
from model import Quote, Author


def feed(csv):
    # You'll obviously need fr_FR.utf-8 for this to work.
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
    session = connect_sql()
    for line in csv.readlines():
        add_line(session, line)
    session.close()


def add_line(session, line):
    content = line.split('\t')
    if len(content) != 3:
        print("Could not parse line : %s" % line)
        return
    quote = content[0].strip('"')
    author = content[1]
    quote_date = datetime.datetime.strptime(content[2], '%d %B %Y')
    try:
        author = get_or_create_author(session, author)
        quote = Quote(author=author, content=quote, date=quote_date)
        session.save(quote)
        session.commit()
    except Exception as exc:
        session.rollback()
        print("Could not add the quote : %s" % quote)
        print("Reason : %s" % exc)


def get_or_create_author(session, author):
    try:
        result = session.query(Author).filter_by(name=author).one()
        return result
    except NoResultFound:
        author = Author(name=author)
        session.save(author)
        session.commit()
        return author
