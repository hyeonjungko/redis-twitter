#!/usr/bin/python3
from abc import ABC
from typing import List
from tweet import Tweet


class TwitterAPI(ABC):

    def post_tweet(self, t: Tweet):
        """ Post the given tweet.

        Args:
            t (Tweet): tweet to be posted
        """
        pass

    def add_follower(self, user_id: int, follower_id: int):
        """ Add follower to given user.

        Args:
            user_id (int): id of the user to be followed
            follower_id (int): id of the follower
        """
        pass

    def get_timeline(self, user_id: int) -> List[Tweet]:
        """ Get home timeline for the given user.

        Args:
            user_id (int): user id of the timeline to be retrieved
        Returns:
            list of tweets that make up the user's timeline
        """
        pass

    def get_followers(self, user_id: int) -> List[int]:
        """ Get a list of followers of a given user.

        Args:
            user_id (int): user of the followers to be retrieved
        Returns:
            list of follower ids
        """
        pass

    def get_followees(self, user_id: int) -> List[int]:
        """ Get a list of followers for a given user.ABC

        Args:
            user_id (int): user of the followees to be retrieved
        Returns:
            list of followee ids
        """
        pass

    def get_tweets(self, user_id: int) -> List[Tweet]:
        pass