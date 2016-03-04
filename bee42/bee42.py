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


class Goal:
    """A limited version of a Beeminder goal"""
    
    def __init__(self, slug, goal_dict):
        """Create a goal from the response to an api get goal"""
        self.slug = slug
        self.title = goal_dict["title"]
        self.description = goal_dict["description"]
        self.goalval = goal_dict["goalval"]
        self.initday = datetime.datetime.fromtimestamp(goal_dict["initday"])
