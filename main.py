import argparse
import ast
import json
import os
import praw
import random
import re
import string
import sys
import time
from concurrent import futures

startTime = time.time()

__version__ = '0.1.0'

RED = str('\033[1;31;40m')
GREEN = str('\033[1;32;40m')
YELLOW = str('\033[1;33;40m')
BLUE = str('\033[1;34;40m')
GREY = str('\033[1;30;40m')
RESET = str('\033[1;37;40m')

def generate_user_agent(size = 16, chars = string.ascii_uppercase + string.digits):
    return 'Subreddit-Mapper-'.join(random.choice(chars) for _ in range(size))

def get_args(argv):
    """get args.
    Args:
        argv (list): List of arguments.
    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description=("Map a subreddit for other linked subreddits")
    )

    parser.add_argument("-c", "--client-id", help="your Reddit.com app client-id", type=str, required=True)
    parser.add_argument("-s", "--client-secret", help="your Reddit.com app client-secret", type=str, required=True)
    parser.add_argument("-u", "--username", help="your Reddit.com account login", type=str, required=True)
    parser.add_argument("-p", "--password", help="your Reddit.com account password (never stored)", type=str, required=True)

    parser.add_argument("-S", "--subreddit", help="a Reddit.com subreddit to map", type=str, required=True)
    parser.add_argument("-l", "--limit", help="limit the depth of the subreddit searches (default - 3)", type=int, default=3)

    parser.add_argument("-v", "--version", help="current application version.", action="store_true")

    args = parser.parse_args(argv)
    return args

def login(args):
  """login method.

  Args:
    args (argparse.Namespace): Parsed arguments.

  Returns: a logged on praw instance
  """

  try:
    reddit = praw.Reddit(
      user_agent=generate_user_agent(),
      client_id=args.client_id,
      client_secret=args.client_secret,
      username=args.username,
      password=args.password
    )
    return reddit
  except Exception as e:
    print(RED + "Login Failed\n" + RESET)
    sys.exit(0)

def dedupe_list(x):
  return list(dict.fromkeys(x))

def strip_punctuation(x):
  return x.translate(str.maketrans('', '', string.punctuation))

def sub_exists(reddit, x):
  exists = True
  try:
    reddit.subreddits.search_by_name(x, exact=True)
  except:
    exists = False
  return exists

def parse_subreddit(reddit, sub, args):
  valid_subs = []
  print("\n", YELLOW, "[[[ Mapping r/", sub, " ]]]", RESET, "\n", sep="")
  try:
    # Gather subreddit info
    subreddit = reddit.subreddit(sub)
    related_subs = []
    related_subs = re.findall(r"/r/([^\s/]+)", subreddit.description)
    
    # Strip punctuation from collected subreddits
    for i in range(len(related_subs)):
      related_subs[i] = strip_punctuation(related_subs[i])

    # Remove any duplicate subreddits
    related_subs = dedupe_list(related_subs)

    # Remove any mentions of the searched subreddit
    try:
      related_subs.remove(sub)
    except:
      pass # Do nothing

    try:
      related_subs.remove(sub.capitalize())
    except:
      pass # Do nothing

    try:
      related_subs.remove(sub.upper())
    except:
      pass # Do nothing
    
    try:
      related_subs.remove(sub.lower())
    except:
      pass # Do nothing
    
    try:
      related_subs.remove(args.subreddit)
    except:
      pass # Do nothing
    
    try:
      related_subs.remove(args.subreddit.capitalize())
    except:
      pass # Do nothing
    
    try:
      related_subs.remove(args.subreddit.upper())
    except:
      pass # Do nothing
    
    try:
      related_subs.remove(args.subreddit.lower())
    except:
      pass # Do nothing
    
    # Check if the subreddits found actually exist
    for i in range(len(related_subs)):
      if(sub_exists(reddit, related_subs[i])):
        print(GREY, "Related: r/", related_subs[i], RESET, sep="")
        valid_subs.append(related_subs[i])

  except Exception as e:
    print(RED, "Error finding data for ", sub, ": ", RESET, e, sep="")
    pass

  return valid_subs

def main():
  """main func."""
  args = get_args(sys.argv[1:])

  # Print program version.
  if args.version:
    print(__version__)
    sys.exit(0)

  print('--- Subreddit Mapper ---\n')

  if args.client_id and args.client_secret and args.username and args.password and args.subreddit:
    reddit = login(args=args)
    data = {}
    for i in range(args.limit + 1):
      print("\n", YELLOW, "[ Mapping Layer ", i, "... ]", RESET, sep="")
      # If this is the first run, gather initial data
      if(i == 0):
        temp_data = {
            "layerId": i,
            "parent": None,
            "subreddit": args.subreddit, 
            "related": parse_subreddit(reddit, args.subreddit, args)
        }
        data[i] = temp_data

      # Otherwise use subreddits found from the first run for subsequent runs
      else:
        search = data[i-1]["related"]
        for s in range(len(search)):
          temp_data = {
            "layerId": i,
            "parent": data[i-1]["subreddit"],
            "subreddit": search[s], 
            "related": parse_subreddit(reddit, search[s], args)
          }
          data[len(data)] = temp_data

    print("\n", GREEN, "***** MAPPING COMPLETE *****", RESET, "\n", sep="")
    print(json.dumps(data, indent=4))

    executionTime = (time.time() - startTime)
    print('\nExecution time: ' + str(round(executionTime, 2)) + "s")

    filename = data[0]["subreddit"] + ".json"
    with open(filename, 'w') as outfile:
      json.dump(data, outfile, indent=4)
      outfile.close()
    
    print("\nOutput saved to disk as JSON\n")
  else:
    print(RED + "You'll need to pass a client-id (-c), client-secret (-s), username (-u), password (-p) and subreddit (-S) to begin." + RESET)

  sys.exit(0)

if __name__ == "__main__":  # pragma: no cover
  main()