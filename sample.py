from tweetpie import tweetpie, api, credential
import datetime
import pprint
import json

with open("credentials.json", "r") as file:
    creds = json.load(file)

# 認証情報取得
cred = credential.Credential(
    creds['consumer_key'],
    creds['consumer_secret'],
    creds['access_token'],
    creds['access_secret'],
)
collector = tweetpie.Tweetpie(cred)

# 検索条件
limit_count = 10 # 最大取得件数/日
kwd = 'ラーメン AND 食べた' # キーワードからクエリ作成
query = kwd + " -? -filter:retweets -filter:news -filter:replies -source:IFTTT -source:dlvr.it -source:twittbot.net -source:autotweety -source:Google"
start_dt = datetime.datetime.strptime('20210629', '%Y%m%d') # 検索開始日
period_dt = 7 # 検索開始日から過去検索する日数
kwd_in_profile = ['歳'] # プロフィールに含める単語
kwd_notin_profile = ['投不労所得資', '稼げる', '毎月', '儲ける'] # プロフィールに含めない単語

# 検索
collected = collector.search(limit_count=limit_count, query=query,
                            start_dt=start_dt, period_dt=period_dt,
                            kwd_in_profile=kwd_in_profile, kwd_notin_profile=kwd_notin_profile)

API = api.Api(cred)
for item in collected:
    print('collected tweet :{}'.format(item.tweet_url))
    # API.like(item.tid) # いいねする
