# SubredditMapper
API to discover related subreddits

### Setup

- Python 3.x
- [Create a Reddit App](https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c)

### Usage

Pass a client id (-c), client secret (-s), username (-u) and password (-p) to get started:

```
python3 main.py  -c <CLIENT_ID> -s <CLIENT_SECRET> -u <USERNAME> -p <PASSWORD>
```

Once the app has started navigate to Port 5000 in your browser to continue.

### Endpoints

- `/`: Health endpoint (returns "OK")
- `/api/parse/<subreddit>`: Parse a subreddit for related content 

### To Do

- [ ] Parallelization for Subreddit mapping
- [x] Refactor Code
- [ ] Finalize JSON format
- [x] HTTP API Support
- [ ] [Visualization Support](https://fperucic.github.io/treant-js/examples/collapsable/)
- [ ] Docker Image