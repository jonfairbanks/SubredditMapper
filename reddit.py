import praw
import random
import string

RED = str('\033[1;31;40m')
GREEN = str('\033[1;32;40m')
YELLOW = str('\033[1;33;40m')
BLUE = str('\033[1;34;40m')
GREY = str('\033[1;30;40m')
RESET = str('\033[1;37;40m')

def generate_user_agent(size = 16, chars = string.ascii_uppercase + string.digits):
    return 'Subreddit-Mapper-'.join(random.choice(chars) for _ in range(size))

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