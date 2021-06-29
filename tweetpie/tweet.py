import dataclasses

@dataclasses.dataclass
class Tweet:

    tid: int
    created_at: str
    text: str
    user_id: str
    user_created_at: str
    user_name: str
    user_screen_name: str
    user_description: str
    user_location: str
    user_statuses_count: str
    user_followers_count: str
    user_friends_count: str
    user_listed_count: str
    user_favourites_count: str
    url: str = ''

    def __post_init__(self):
        self.user_url = 'https://twitter.com/' + self.user_screen_name
        self.tweet_url = 'https://twitter.com/'+ self.user_screen_name + '/status/'+str(self.tid)
