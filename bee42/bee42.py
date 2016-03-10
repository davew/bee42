"""Access to the beeminder.com api"""

import datetime
import requests

BEE42_INI_API_URL = "https://www.beeminder.com/api/v1/"


class User:
    """A readonly Beeminder user that is loaded using the API.
    It provides access to the read/write goals and thus datapoints"""

    def __init__(self, username, token):
        """ Construct a read-only Beeminder user object and fill it using
        the api."""
        self.username = username
        self.token = token

        self.user_url = BEE42_INI_API_URL + "users/" + self.username + ".json"
        self.auth_param = {'auth_token': self.token}

        self.api_get_user()

    def api_get_user(self):
        """ Use the Beeminder api to fill this user object"""
        response = requests.get(self.user_url, params=self.auth_param)
        user_dict = response.json()
        self.timezone = user_dict["timezone"]
        self.updated_at = datetime.datetime.fromtimestamp(user_dict["updated_at"])
        self.goalslugs = user_dict["goals"]
        self.deadbeat = user_dict["deadbeat"]

    def load_goal(self, slug):
        """retrieve a single goal from the Beeminder API"""
        goal_url = BEE42_INI_API_URL + "users/" + self.username + "/goals/" + slug + ".json"
        response = requests.get(goal_url, params=self.auth_param)
        goal_dict = response.json()
        goal = Goal(slug, goal_dict)
        return goal

    def getDatapoints(self, slug):
        """retrieve all the datapoints for a goal for this user"""
        datapoint_url = BEE42_INI_API_URL + "users/" + self.username + "/goals/" + slug + "/datapoints.json"
        param={}
        param["auth_token"] = self.token
        response = requests.get(datapoint_url, params=param)
        return response.json()


class Goal:
    """A limited version of a Beeminder goal"""

    def __init__(self, slug, goal_dict):
        """Create a goal from the response to an api get goal"""
        self.slug = slug
        self.title = goal_dict["title"]
        self.description = goal_dict["description"]
        self.goalval = goal_dict["goalval"]
        self.initday = datetime.datetime.fromtimestamp(goal_dict["initday"])


class Datapoint:
    """An actual activity, or weight or value associated with a goal"""

    def __init__(self, user, slug):
        """Create a datapoint object"""
        self.user = user
        self.slug = slug
        self.id = None
        self.timestamp = None
        self.daystamp = None
        self.value = None
        self.comment = None
        self.updated_at = None
        self.requestid = None

    def post(self):
        """save a datapoint object to beeminder using API"""
        datapoint_url = BEE42_INI_API_URL + "users/" + self.user.username + "/goals/" + self.slug + "/datapoints.json"
        param={}
        param["auth_token"] = self.user.token
        param["id"] = self.id
        param["timestamp"] = self.timestamp
        param["daystamp"] = self.daystamp
        param["value"] = self.value
        param["comment"] = self.comment
        param["updated_at"] = self.updated_at
        param["requestid"] = self.requestid
        response = requests.post(datapoint_url, params=param)
        return response.status_code
