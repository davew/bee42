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

    def api_get_skinny_goal(self, goal_slug):
        """A skinny goal is defined by the Beeminder API as a subset of the
        goal data and is all that is generally needed.
        It contains only the most recent datapoint.
        This collects a goal matching the goal_slug passed for the current user
        from Beeminder and returns a SkinnyGoal object"""
        response = requests.get(self.user_url, params=self.auth_param)
        user_dict = response.json()
        

class SkinnyGoal:
    """The limited version of a Beeminder goal"""
    
    def __init__(self, goal_slug):
        """The goal_slug should be considered static for a goal so is passed
        to the constructor. Goals can be loaded from the API or created locally
        and then used to update Beeminder"""
        self.goal_slug = goal_slug
