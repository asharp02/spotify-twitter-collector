import tweepy
import os
import pandas as pd
import csv


consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")


def handle_tweet(tweet_data):
    with open("TweetStream.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow(tweet_data)


class MyStreamListener(tweepy.Stream):
    def on_status(self, status):
        if not hasattr(status, "retweeted_status"):
            if status.truncated == True:
                tweet = status.extended_tweet["full_text"]
            else:
                tweet = status.text
            # obj = {}
            # obj["Tweet ID"] = status.id
            # obj["User ID"] = status.user.id
            # obj["Username"] = status.user.name
            # obj["User Handle"] = status.user.screen_name
            # obj["User Location"] = status.user.location
            # obj["User Bio"] = status.user.description
            data = [
                status.id,
                status.user.id,
                tweet,
                status.user.name,
                status.user.screen_name,
                status.user.location,
                status.user.description,
            ]
            handle_tweet(data)

    def on_error(self, status_code):
        if status_code == 420:
            # Returning False in on_data disconnects the stream
            return False


printer = MyStreamListener(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret,
)

results = []
with open("TweetStream.csv", "a") as f:
    writer = csv.writer(f)
    writer.writerow(
        [
            "Tweet ID",
            "User ID",
            "Tweet Text",
            "Username",
            "User Handle",
            "User Location",
            "User Bio",
        ]
    )

printer.filter(
    locations=[
        -124.7771694,
        24.520833,
        -66.947028,
        49.384472,
    ],
    languages=["en"],
)
