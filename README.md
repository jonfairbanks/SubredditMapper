# SubredditMapper
Discover related subreddits

### Setup

- Python 3.x
- [Create a Reddit App](https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c)

### Usage

Pass a client id (-c), client secret (-s), username (-u), password (-p) and subreddit (-S) to get started:

```
python3 main.py  -c <CLIENT_ID> -s <CLIENT_SECRET> -u <USERNAME> -p <PASSWORD> -S cars
```

Results are saved to disk as JSON and displayed on-screen.


### To Do

- Parallelization for Subreddit mapping
- Finalize JSON format
- HTTP API Support
- Visualization Support