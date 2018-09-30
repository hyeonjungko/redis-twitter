#!/usr/bin/python3
from datetime import datetime


class Tweet:

    def __init__(self, user_id, timestamp: float, tweet: str):
        self.user_id = user_id
        self.timestamp = timestamp
        self.tweet = tweet

    def __repr__(self):
        return str(self.timestamp) + ' : USER ' + str(self.user_id) + ' : ' + self.tweet
        # .strftime('%y-%m-%d %H:%M:%S')

    def get_user_id(self):
        return self.user_id
