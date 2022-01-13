import argparse

def get_args(argv):
    parser = argparse.ArgumentParser(
      description=("Map a subreddit for other linked subreddits")
    )

    parser.add_argument("-c", "--client-id", help="your Reddit.com app client-id", type=str, required=True)
    parser.add_argument("-s", "--client-secret", help="your Reddit.com app client-secret", type=str, required=True)
    parser.add_argument("-u", "--username", help="your Reddit.com account login", type=str, required=True)
    parser.add_argument("-p", "--password", help="your Reddit.com account password (never stored)", type=str, required=True)

    parser.add_argument("-l", "--limit", help="limit the depth of the subreddit searches (default - 2)", type=int, default=2)

    parser.add_argument("-v", "--version", help="current application version.", action="store_true")

    args = parser.parse_args(argv)
    return args