import tweepy
import os


consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")


class MyStreamListener(tweepy.Stream):
    def on_status(self, status):
        print(status.id)


printer = MyStreamListener(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret,
)

printer.filter(track=["Twitter"])
