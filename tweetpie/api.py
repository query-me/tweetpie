from tweetpie import credential as cred
import tweepy

class Api:

    def __init__(self, credential:cred.Credential):
        auth = tweepy.OAuthHandler(credential.consumer_key, credential.consumer_secret)
        auth.set_access_token(credential.access_token, credential.access_secret)
        self.api = tweepy.API(auth)

    def like(self, tweet_id):
        try:
            self.api.create_favorite(tweet_id)
        except Exception as e:
            print(e)
    
    def retweet(self, tweet_id):
        try:
            self.api.retweet(tweet_id)
        except Exception as e:
            print(e)

    def follow(self, user_id):
        try:
            self.api.create_friendship(user_id)
        except Exception as e:
            print(e)