# -*- coding: utf8 -*-
'''A module that exposes the very basic model that we're going to use.
'''

import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column, ForeignKey, Integer, String, Date, Boolean)
from sqlalchemy.orm import relationship, backref

from convertdate import french_republican

Base = declarative_base()

REV_CALENDAR_BEGIN = datetime.date(1792, 9, 22)
REV_CALENDAR_END = datetime.date(1806, 1, 1)
MONTHS = ["janvier", "février", "mars",
          "avril", "mai", "juin",
          "juillet", "août", "septembre",
          "octobre", "novembre", "décembre"]


class Author(Base):
    """A member of one of the French revolutionaries assembly."""
    __tablename__ = "author"
    author_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Quote(Base):
    """A simple quote from a French Revolutionary.
    The author is denormalized for now, since we're not sure there would
    be any particular use for this."""
    __tablename__ = "quote"
    quote_id = Column(Integer, primary_key=True)
    content = Column(String)
    date = Column(Date)
    author_id = Column(ForeignKey("author.author_id", ondelete='CASCADE'),
                       nullable=False, index=True)
    used = Column(Boolean, nullable=False, default=False)
    author = relationship("Author",
                          primaryjoin="Quote.author_id == Author.author_id",
                          backref=backref("quotes"))

    def to_date(self):
        """Given the quote, returns the date in a printable, french format.
        If the date is during the french revolutionary calendar usage time,
        display it thusly. Else, display it in the more classical way."""
        if self.date >= REV_CALENDAR_BEGIN and self.date <= REV_CALENDAR_END:
            # During revolutionary calendar : return the date in this format
            d = french_republican.from_gregorian()
            return french_republican.format(d.year, d.month, d.day)
        else:
            return old_date_to_string(self.date)

    def to_tweet_string(self):
        return ''.join(['« ',
                        self.content,
                        '» ',
                        ' (',
                        self.author.name,
                        ')'])


def old_date_to_string(date):
    """Since we cannot use strftime for date below 1900,
    we'll do this manually."""
    d = date.day
    if d == 1:
        d = "1er"
    m = MONTHS[date.month]
    return "%s %s %s" % (d, m, date.year())
