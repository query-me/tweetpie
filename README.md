# tweetpie


tweetpie is a twitter search tool that enables bulk data collection for further analyze, marketing or research purpose. According to the Twitter official [specification](https://developer.twitter.com/en/docs/twitter-api/rate-limits), the standard plan API limits its maximum recent search to 180 searches per user for 15-minute interval. The tool confront this limitation by looking for header information to retrieves the number of search attempts within that interval, and remaining minutes to reset the current restrain, then it automatically restart the recent search until it meets the amount of searches you first provided.

## Installation
- Clone this repo:
```bash
git clone https://github.com/query-me/tweetpie
cd tweetpie
```
- Run this to build an archive file
```bash
python setup.py sdist
pip install dist/tweetpie-1.0.tar.gz
```
make sure to upgrade your pip to the latest release.
- Go to Twitter [developer portal](https://developer.twitter.com/) to retrieve your own consumer keys, consumer secret, access_token and access_secret.
- Make sure to do that before you enable your project app both readable and writable as Twitter sets your first app readable only by default. (__Doing this step before key generation requires regeneration of keys.__)
- change your credentials.json keys accordingly
```
{
    "consumer_key": "<your-consumer-key>",
    "consumer_secret": "<your-consumer-secret>",
    "access_token": "<your-access-token>",
    "access_secret": "<your-access-secret>"
}
```

## How It Works
- Please refer to the [sample.py](https://github.com/query-me/tweetpie/blob/main/sample.py) for how it works but here's some brief usuage.

- define parameters for bulk search
```python
limit_count = 10 # maximum number of tweets to retrieve (per day)
kwd = 'pasta AND perfect' # queries
query = kwd + " -? -filter:retweets -filter:news -filter:replies -source:IFTTT -source:dlvr.it -source:twittbot.net -source:autotweety -source:Google"
start_dt = datetime.datetime.strptime('20210629', '%Y%m%d') # first date to search
period_dt = 7 # first search date -> 'start_dt' look for tweets for the past 'period_at' days
kwd_in_profile = ['age'] # keywords to be included in profile
kwd_notin_profile = ['business', 'stock'] # keywords not to be included in profile
lang = 'en' #lang
```

- perform bulk search (_it might takes a while depending on how much attempts you trying to make_)
```python
# search
collected = collector.search(limit_count=limit_count, query=query,
                            start_dt=start_dt, period_dt=period_dt,
                            kwd_in_profile=kwd_in_profile,
                            kwd_notin_profile=kwd_notin_profile, lang=lang)
```

- Once certain amount of data is collected, you could iterate over the tweet data and like it, retweet it or follow the users.
```python
# search
API = api.Api(cred)
for item in collected:
    print('collected tweet :{}'.format(item.tweet_url))
    API.like(item.tid) # like the tweet
```

## License
MIT