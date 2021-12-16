import os
import configparser
import tweepy as tw
import pandas as pd

consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")


def getClient():
    client = tw.Client(
        bearer_token=bearer_token,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )
    return client


def get_tweet(client, id):
    tweet = client.get_tweet(
        id,
        expansions=["author_id"],
        user_fields=["username", "description", "location"],
        tweet_fields=["created_at"],
    )
    return tweet


def searchTweets(query, max_results):
    client = getClient()
    tweets = client.search_recent_tweets(
        query=query,
        max_results=max_results,
        expansions="author_id",
        user_fields=["username", "description", "location"],
        tweet_fields=["created_at"],
    )
    tweet_data = tweets.data
    results = []
    # consider adding a dict comprehension with user data pulled from search_recent_tweets to reduce query
    if tweet_data:
        for tweet in tweet_data:
            twt = get_tweet(client, tweet["id"])
            obj = {}
            obj["id"] = tweet.id
            obj["text"] = tweet.text
            obj["created at"] = tweet.created_at
            obj["user handle"] = twt.includes["users"][0].username
            obj["user bio"] = twt.includes["users"][0].description
            obj["user location"] = twt.includes["users"][0].location
            results.append(obj)
    else:
        return []

    return results


tweets = searchTweets("Doja+Cat -is:retweet", 10)
df = pd.DataFrame.from_dict(tweets)
