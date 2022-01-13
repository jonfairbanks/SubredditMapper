import re
import string
import time

RED = str('\033[1;31;40m')
GREEN = str('\033[1;32;40m')
YELLOW = str('\033[1;33;40m')
BLUE = str('\033[1;34;40m')
GREY = str('\033[1;30;40m')
RESET = str('\033[1;37;40m')

def dedupe_list(x):
  return list(dict.fromkeys(x))

def strip_punctuation(x):
  return x.translate(str.maketrans('', '', string.punctuation))

def sub_exists(reddit, x):
  #existsTime = time.time()

  exists = True
  try:
    reddit.subreddits.search_by_name(x, exact=True)
  except:
    exists = False
  
  #totalExistsTime = (time.time() - existsTime)
  #print('\nTime to check if subreddit exists: ' + str(round(totalExistsTime, 4)) + "s")
  
  return exists
  
def parse_subreddit(reddit, sub, args):
  valid_subs = []
  #print("\n", YELLOW, "[[[ Mapping r/", sub, " ]]]", RESET, "\n", sep="")
  try:
    #infoTime = time.time()

    # Gather subreddit info
    subreddit = reddit.subreddit(sub)
    related_subs = []
    related_subs = re.findall(r"/r/([^\s/]+)", subreddit.description)
    
    #totalInfoTime = (time.time() - infoTime)
    #print('\nTime to get related subs from description: ' + str(round(totalInfoTime, 4)) + "s")

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
        #print(GREY, "Related: r/", related_subs[i], RESET, sep="")
        valid_subs.append(related_subs[i])

  except Exception as e:
    print(RED, "Error finding data for ", sub, ": ", RESET, e, sep="")
    pass

  return valid_subs