import json
import os
import sys
import time
from flask import Flask
from markupsafe import escape

from args import get_args
from mapper import parse_subreddit
from reddit import login

startTime = time.time()

app = Flask(__name__)

RED = str('\033[1;31;40m')
GREEN = str('\033[1;32;40m')
YELLOW = str('\033[1;33;40m')
BLUE = str('\033[1;34;40m')
GREY = str('\033[1;30;40m')
RESET = str('\033[1;37;40m')

@app.route("/")
def health_check():
    return "OK"

@app.route("/<sub>")
def parse(sub):
  args = get_args(sys.argv[1:])

  #print('--- Subreddit Mapper ---\n')

  if args.client_id and args.client_secret and args.username and args.password:
    reddit = login(args=args)
    data = {}
    for i in range(args.limit + 1):
      #print("\n", YELLOW, "[ Mapping Layer ", i, "... ]", RESET, sep="")
      
      # If this is the first run, gather initial data
      if(i == 0):
        temp_data = {
            "layerId": i,
            "parent": None,
            "subreddit": escape(sub), 
            "related": parse_subreddit(reddit, escape(sub), args)
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

    #print("\n", GREEN, "***** MAPPING COMPLETE *****", RESET, "\n", sep="")
    #print(json.dumps(data, indent=4))

    executionTime = (time.time() - startTime)
    print('\nExecution time: ' + str(round(executionTime, 2)) + "s")
    
    return data
  else:
    print(RED + "You'll need to pass a client-id (-c), client-secret (-s), username (-u) and password (-p) to begin." + RESET)
    sys.exit(0)

if __name__ == "__main__":  # pragma: no cover
  app.run(host="0.0.0.0")