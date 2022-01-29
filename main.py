import json
import sys
import time
from flask import Flask
from markupsafe import escape

from args import get_args
from mapper import parse_subreddit
from reddit import login

RED = str('\033[1;31;40m')
GREEN = str('\033[1;32;40m')
YELLOW = str('\033[1;33;40m')
BLUE = str('\033[1;34;40m')
GREY = str('\033[1;30;40m')
RESET = str('\033[1;37;40m')

args = get_args(sys.argv[1:])

try:
  reddit = login(args=args)
except Exception as e:
  print("There was an error logging into Reddit:", e)

app = Flask(__name__)

@app.route("/")
def health_check():
    return "OK"

@app.route("/api/parse/<sub>")
def parse(sub):
  print("\nReceived request to map r/", sub, sep="")
  startTime = time.time()
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

  executionTime = (time.time() - startTime)
  print('Execution time: ' + str(round(executionTime, 2)) + "s")
  
  return data
  
if __name__ == "__main__":  # pragma: no cover
  if args.client_id and args.client_secret and args.username and args.password:
    print('--- Subreddit Mapper ---\n')
    app.run(host="0.0.0.0")
  else:
    print(RED + "You'll need to pass a client-id (-c), client-secret (-s), username (-u) and password (-p) to begin." + RESET)
    sys.exit(0)
