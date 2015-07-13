# Shit French Revolutionaries Say Bot

(Or sfrstbot for short)

## Presentation 

sfrsbot is a small side project. Its purpose is to provide twitter
with witty, pathetic, amusing, grandiose, self-dignified or simply interesting
quotes taken from the archives of the often heated discussions that took place
in the various incarnation of the parliament during the French revolution.

### Bot behaviour

The bot will tweet four times a day, at:
- 9AM
- Noon
- 6PM
- 9PM

It will take a random quote from its database and put the quote and his author.
(In a perfect world, here, I would have written "his or her", but there was no
woman in those assemblies. Which is rather unfair, considering some were the
ghostwriter of the politicans.)

### Bot interactions

If someone interacts with the bot, the following things will happen:
- If the word "quand" is used, namely "when" in french, in the answer to
this bot's tweet, the bot will give the exact date of the citation one
has answered to.
- If not, and if the bot has not tweeted too much the last hour, it will
answer with a random quote - that he might have already used.

In the future, I'd like the bot to be able to answer requests such as "Quote
X", where x are revolutionaries, and "Quote about Y", where Y is a word.

## How to use ?

    ./main.py

Without any options will simply start the bot as a daemon on your machine.

    ./main.py feed <csv_file_path>

Will feed his database. (The CSV format should be as follow : quote, author, date)
