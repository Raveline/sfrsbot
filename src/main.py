#!/usr/bin/env python
'''Shit French Revolutionaries Say Bot (sfrsbot for short)  main module.'''

import argparse

from scripts import feed
from daemon import run_daemon
from utils import create_db, random_quote, connect_sql


def random_and_print():
    session = connect_sql()
    quote = random_quote(session)
    session.close()
    print(quote.to_tweet_string())


def main():
    parser = argparse.ArgumentParser(prog='sfrsbot')
    sub_parsers = parser.add_subparsers()
    feed_p = sub_parsers.add_parser('feed',
                                    help='Feed a quote CSV to the database')
    feed_p.add_argument('csv',
                        type=argparse.FileType('r'),
                        help='CSV file to read')
    feed_p.set_defaults(func=feed)
    daemon_p = sub_parsers.add_parser('daemon',
                                      help='Run the bot as a daemon')
    daemon_p.set_defaults(func=run_daemon)

    init_p = sub_parsers.add_parser('init',
                                    help='Create the database')
    init_p.set_defaults(func=create_db)
    test_random = sub_parsers.add_parser('test_random',
                                         help='Get a random quote to test.')
    test_random.set_defaults(func=random_and_print)

    # Parse and call function
    args = parser.parse_args()
    params = vars(args)
    function = args.func
    del(params['func'])
    function(**params)


if __name__ == "__main__":
    main()
