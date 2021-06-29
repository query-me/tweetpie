from tweetpie import tweetpie, api, credential
import datetime
import pprint
import json

with open("credentials.json", "r") as file:
    creds = json.load(file)

# get credential values
cred = credential.Credential(
    creds['consumer_key'],
    creds['consumer_secret'],
    creds['access_token'],
    creds['access_secret'],
)
collector = tweetpie.Tweetpie(cred)

# search condtion
limit_count = 10 # maximum number of tweets to retrieve (per day)
kwd = 'pasta AND perfect' # queries
query = kwd + " -? -filter:retweets -filter:news -filter:replies -source:IFTTT -source:dlvr.it -source:twittbot.net -source:autotweety -source:Google"
start_dt = datetime.datetime.strptime('20210629', '%Y%m%d') # first date to search
period_dt = 7 # first search date -> 'start_dt' look for tweets for the past 'period_at' days
kwd_in_profile = ['age'] # keywords to be included in profile
kwd_notin_profile = ['business', 'stock'] # keywords not to be included in profile
lang = 'en' #lang

# search
collected = collector.search(limit_count=limit_count, query=query,
                            start_dt=start_dt, period_dt=period_dt,
                            kwd_in_profile=kwd_in_profile,
                            kwd_notin_profile=kwd_notin_profile, lang=lang)

API = api.Api(cred)
for item in collected:
    print('collected tweet :{}'.format(item.tweet_url))
    # API.like(item.tid) # like the tweet
