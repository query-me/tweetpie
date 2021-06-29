import datetime
import json
import time
import math
from requests_oauthlib import OAuth1Session
from pytz import timezone
from dateutil import parser
from tweetpie import tweet as twt
from tweetpie import credential as cred

class Tweetpie:
    
    SEARCH_TWEETS_URL = 'https://api.twitter.com/1.1/search/tweets.json'
    RATE_LIMIT_STATUS_URL = "https://api.twitter.com/1.1/application/rate_limit_status.json"

    def __init__(self, credential:cred.Credential):
        self.credential = credential

    def _get_twitter_session(self):
        return OAuth1Session(
            self.credential.consumer_key,
            self.credential.consumer_secret,
            self.credential.access_token,
            self.credential.access_secret
            )

    def _search_twitter_timeline(self, limit_count, keyword, lang, include_in_profile,
                                exclude_in_profile, since='', until='', max_id=''):
        timelines = []
        id = ''
        twitter = self._get_twitter_session()

        params = {'q': keyword, 'count': limit_count, 'result_type': 'mixed', 'lang':lang}

        if max_id != '':
            params['max_id'] = max_id
        if since != '':
            params['since'] = since
        if until != '':
            params['until'] = until

        req = twitter.get(self.SEARCH_TWEETS_URL, params=params)

        if req.status_code == 200:
            search_timeline = json.loads(req.text)

            for tweet in search_timeline['statuses']:
                id = str(tweet['id'])

                if max_id == str(tweet['id']):
                    print('continue')
                    continue

                timeline = twt.Tweet(tid=tweet['id']
                    , created_at=str(parser.parse(tweet['created_at']).astimezone(timezone('Asia/Tokyo')))
                    , text=tweet['text']
                    , user_id=tweet['user']['id']
                    , user_created_at=str(parser.parse(tweet['user']['created_at']).astimezone(timezone('Asia/Tokyo')))
                    , user_name=tweet['user']['name']
                    , user_screen_name=tweet['user']['screen_name']
                    , user_description=tweet['user']['description']
                    , user_location=tweet['user']['location']
                    , user_statuses_count=tweet['user']['statuses_count']
                    , user_followers_count=tweet['user']['followers_count']
                    , user_friends_count=tweet['user']['friends_count']
                    , user_listed_count=tweet['user']['listed_count']
                    , user_favourites_count=tweet['user']['favourites_count'])

                if 'media' in tweet['entities']:
                    medias = tweet['entities']['media']
                    for media in medias:
                        timeline.url = media['url']
                        break
                elif 'urls' in tweet['entities']:
                    urls = tweet['entities']['urls']
                    for url in urls:
                        timeline.url = url['url']
                        break
                else:
                    timeline.url = ''

                if include_in_profile:
                    keys_not_found = [True for k in include_in_profile if k not in timeline.user_description]
                    if keys_not_found:
                        continue
                if exclude_in_profile:
                    keys_found = [True for k in exclude_in_profile if k in timeline.user_description]
                    if keys_found:
                        continue

                timelines.append(timeline)
        else:
            print("ERROR: %d" % req.status_code)

        twitter.close()

        return timelines, id

    def _get_rate_limit_status(self):
        twitter = self._get_twitter_session()
        limit = 1
        remaining = 1
        reset_minute = 0

        req = twitter.get(self.RATE_LIMIT_STATUS_URL)
        if req.status_code == 200:
            limit_api = json.loads(req.text)

            limit = limit_api['resources']['search']['/search/tweets']['limit']
            remaining = limit_api['resources']['search']['/search/tweets']['remaining']
            reset = limit_api['resources']['search']['/search/tweets']['reset']
            reset_minute = math.ceil((reset - time.mktime(datetime.datetime.now().timetuple())) / 60)

        twitter.close()

        return limit, remaining, reset_minute


    def _check_api_remain_and_sleep(self):
        limit, remaining, reset_minute = self._get_rate_limit_status()
        print('limit :{}'.format(limit))
        print('remaining :{}'.format(remaining))
        print('reset :{} minutes'.format(reset_minute))

        if remaining == 0:
            time.sleep(60 * (int(reset_minute) + 1))

        return

    def search(self, limit_count=10, query='',
                start_dt=datetime.datetime.today(),
                period_dt=1, kwd_in_profile=[],
                kwd_notin_profile=[], lang='ja'):

        timelines = []
        max_id = ''

        for i in range(int(period_dt)):
            dt = (start_dt - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
            since = str(dt) + '_00:00:00_JST'
            until = str(dt) + '_23:59:59_JST'

            collected = []

            while True:
                self._check_api_remain_and_sleep()

                timelines, max_id = self._search_twitter_timeline(limit_count, query, lang,
                                                                kwd_in_profile, kwd_notin_profile,
                                                                since, until, max_id)

                time.sleep(5)

                if timelines == []:
                    break
                

                if len(timelines) < limit_count:
                    break
        
        return timelines