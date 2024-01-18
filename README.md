# Twitch Username Checker

A script in Python to check if usernames are available from Twitch. Also comes with an auto-generator to find available short usernames.

Originally written by @sixem on GitHub.
Original source: https://gist.github.com/sixem/b358cd424fc5e7b4b4188371d9d5c276

Ported to Python3 by @f-o on GitHub.
- Added support for automatic generation of usernames
- Added argparse
- General cleanup

## Usage:
    twitch-name-checker.py <-l|--list> <list-of-usernames.txt>
    twitch-name-checker.py <-a|--auto> <length-of-usernames>
    twitch-name-checker.py <-h|--help>
