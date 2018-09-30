#!/usr/bin/python3

import redis
from twitter_api import TwitterAPI
from typing import List
from tweet import Tweet

TWEETS_PER_TIMELINE = 30


class RedisTwitter(TwitterAPI):
    """ Implementation of Twitter API. """

    def __init__(self):
        """ Initialize Redis server. """
        self.r = redis.StrictRedis(
            host='localhost', port='6379', decode_responses=True)
        self.r.flushall()

    def post_tweet(self, t: Tweet):
        tweet_id = str(self.r.incr('tweet:'))
        key_user = 'user:' + str(t.user_id)
        key_followers = 'followers:' + str(t.user_id)
        key_tweet = 'tweet:' + tweet_id

        # add tweet_id to user key-value store
        self.r.sadd(key_user, tweet_id)

        # for each follower of the user
        for follower in self.r.smembers(key_followers):
            # add tweet to follower's sorted timeline
            key_timeline = 'timeline:' + follower
            self.r.zadd(key_timeline, t.timestamp, tweet_id)

        # add tweet in tweets key-value store
        self.r.hmset(key_tweet, {
            'user_id': t.user_id,
            'tweet_txt': t.tweet,
            'timestamp': t.timestamp
        })

    def add_follower(self, user_id: int, follower_id: int):
        key_followers = 'followers:' + str(user_id)
        key_followees = 'following:' + str(follower_id)

        # add follower to followers key-value store
        self.r.sadd(key_followers, follower_id)
        # add following to followees key-value store
        self.r.sadd(key_followees, user_id)

    def get_timeline(self, user_id: int) -> List[Tweet]:
        key_timeline = 'timeline:' + str(user_id)
        tweets = []

        # fetch tweets from user timeline key-value store
        # in by most recent time order
        for tweet_id in self.r.zrevrange(key_timeline, 0, -1):
            tweets.append(self.fetch_tweet(tweet_id))

        return tweets

    def get_followers(self, user_id: int) -> List[int]:
        key_followers = 'followers:' + str(user_id)
        followers = []

        for follower in self.r.smembers(key_followers):
            followers.append(follower)

        return followers

    def get_followees(self, user_id: int) -> List[int]:
        key_following = 'following:' + str(user_id)
        followees = []

        for followee in self.r.smembers(key_following):
            followees.append(followee)

        return followees

    def get_tweets(self, user_id: int) -> List[Tweet]:
        # access the tweet:user_id
        key_user = 'user:' + str(user_id)
        tweets = []

        for tweet_id in self.r.smembers(key_user):
            tweets.append(self.fetch_tweet(tweet_id))

        return tweets

    def fetch_tweet(self, tweet_id: int):
        tweet_set = self.r.hgetall('tweet:' + str(tweet_id))
        user_id = tweet_set.get('user_id')
        timestamp = tweet_set.get('timestamp')
        tweet_txt = tweet_set.get('tweet_txt')

        return Tweet(user_id, timestamp, tweet_txt)
