
# Cosoensis
## Command-line Mastodon client

### Installation

`pip install cosoensis`

### Usage

`cosoensis [-h] [-v] [-t TOOT_LIMIT] [-n] [-H] [-l] [-p] [-# HASHTAG] [-s SEARCH] [-f] [-F] [-cw] [-* FAVOURITE] [-b BOOST] [-c CONVO] [-q QUICK] [-sp SPOILERTEXT]`

positional arguments:
  FILE

options:
  -h, --help            show this help message and exit

  -v, --version         show program's version number and exit

  -t TOOT_LIMIT, --tootlimit TOOT_LIMIT Maximum number of items to display

  -n, --notifications   Scope: notifications

  -H, --home            Scope: home

  -l, --local           Scope: local

  -p, --public          Scope: public

  -# HASHTAG, --hashtag HASHTAG Search by hashtag

  -s SEARCH, --search SEARCH Search hashtags and accounts

  -f, --follows         Show who you follow

  -F, --followers       Show who follows you

  -cw, --content-warnings Display text behind Content Warnings

  -* FAVOURITE, --favourite FAVOURITE Favourite or unfavourite a status

  -b BOOST, --boost BOOST Boost or unboost a status

  -c CONVO, --convo CONVO Show the entire conversation for a status

  -q QUICK, --quick QUICK Send a quick direct toot. (enclose toot in quotes)

  -sp SPOILERTEXT, --spoilertext SPOILERTEXT Pre-fill Spoiler Text field.
