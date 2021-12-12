'''
Twitch Username Checker

A small script to check if Twitch usernames are available.
Originally written by @sixem on GitHub.
Original source: https://gist.github.com/sixem/b358cd424fc5e7b4b4188371d9d5c276

Ported to Python3 by @f-o on GitHub.
- Added support for automatic generation of usernames
- Added argparse
- General cleanup

Usage:
    twitch-name-checker.py <-l|--list> <list-of-usernames.txt>
    twitch-name-checker.py <-a|--auto> <length-of-usernames>
    twitch-name-checker.py <-h|--help>
'''

import requests
import sys
from pathlib import Path
import argparse
import string
import itertools

def main():
    parser = argparse.ArgumentParser(description='Check if Twitch usernames are available.')
    parser.add_argument('-l', '--list', dest='file', nargs='?', const="usernames.txt", help='File with a list of usernames to check.')
    parser.add_argument('-a', '--auto', dest='length', nargs='?', const=4, type=int, help='Automatically generate a list of usernames with given length to check.')
    args = parser.parse_args()

    if args.file:
        checker_batch(args.file)
    elif args.length:
        checker_auto(args.length,args.amount)
    else:
        parser.print_help()
        sys.exit(1)

# Checks if a username is available.
def check_name(username):
    r = requests.head("https://passport.twitch.tv/usernames/" + username, headers={'Connection':'close'})
    
    if r.status_code == 403:
        success = False
        while success == False:
            r = requests.head("https://passport.twitch.tv/usernames/" + username, headers={'Connection':'close'})
            if r.status_code != 403:
                success = True
    
    if r.status_code == 200:
        return {'username': username, 'taken': True, 'status_code': r.status_code}
    else:
        return {'username': username, 'taken': False, 'status_code': r.status_code}

# Batch mode.
def checker_batch(file):
    print(f"{p_colors.OKBLUE}Running in {p_colors.HEADER}batch mode!{p_colors.ENDC}")

    # Reads the list of usernames from the specified file.    
    usernames = []
    with open(Path(__file__).parent / file) as f:
        lines = f.readlines()
        for line in lines:
            usernames.append(line.rstrip())

    available_usernames = []
    try:
        for username in usernames:
            status = check_name(username)
            if status['status_code'] == 204:
                print(f"{p_colors.OKGREEN}{status['username']} is available!{p_colors.ENDC}")
                available_usernames.append(username)
            else:
                print(f"{p_colors.FAIL}{status['username']} is not available.{p_colors.ENDC}")

    except KeyboardInterrupt:
        sys.exit(1)

    print("")
    
    print(f"{p_colors.OKBLUE}Check complete, {len(available_usernames)}/{len(usernames)} names are available.{p_colors.ENDC}")
    for user in available_usernames:
        print(p_colors.OKGREEN,user,p_colors.ENDC)
        

# Auto mode.
def checker_auto(length,threads):
    print(f"{p_colors.OKBLUE}Running in {p_colors.HEADER}auto mode!{p_colors.ENDC}")
    usernames = []
    available_usernames = []
    characters = string.ascii_lowercase+string.digits

    # Generates a list of usernames with the specified length.
    for i in itertools.permutations(characters, length):
        usernames.append("".join(i))

    try:
        for username in usernames:
            status = check_name(username)
            if status['status_code'] == 204:
                print(f"{p_colors.OKGREEN}{status['username']} is available!{p_colors.ENDC}")
                available_usernames.append(username)
            else:
                print(f"{p_colors.FAIL}{status['username']} is not available.{p_colors.ENDC}")

    except KeyboardInterrupt:
        sys.exit(1)

    print("")
    
    print(f"{p_colors.OKBLUE}Check complete, {len(available_usernames)}/{len(usernames)} names are available.{p_colors.ENDC}")
    for user in available_usernames:
        print(p_colors.OKGREEN,user,p_colors.ENDC)

            
class p_colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
if __name__ == '__main__':
    main()