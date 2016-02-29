import requests
import datetime
import configparser

BEE42_INI           = "bee42.ini"
BEE42_INI_BEEMINDER = "BeeMinder"
BEE42_INI_USERNAME  = "Username"
BEE42_INI_TOKEN     = "Token"
BEE42_INI_API_URL   = "Api_Url"

class Beeminder:
    def __init__(self):
        self.load_config()
        self.user = self.loadUser()
        self.goals = self.user['goals']

    def load_config(self    ):
        config = configparser.ConfigParser()
        config.read(BEE42_INI)
        
        self.ini_beeminder = config[BEE42_INI_BEEMINDER]
        self.username = self.ini_beeminder[BEE42_INI_USERNAME]
        self.token = self.ini_beeminder[BEE42_INI_TOKEN]
        self.api_url = self.ini_beeminder[BEE42_INI_API_URL]

        self.user_url = self.api_url + "users/" + self.username + ".json"

    def goal_url(self, goal):
        return self.api_url + "users/" + self.username + "/goals/" + goal + ".json"
        
    def datapoint_url(self, goal):
        return self.api_url + "users/" + self.username + "/goals/" + goal + "/datapoints.json"

    def authparam(self):
        return {'auth_token': self.token}

    def nowparam(self, comment, value):
        n = {
            'value': value,
            'comment': comment,
            }
        n.update(self.authparam())
        return n

    def yesterdayparam(self, comment, value):
        y = {
            'daystamp': datetime.date.today() - datetime.timedelta(days=1),
            }
        y.update(self.nowparam(comment, value))
        return y

    def loadUser(self):
        r = requests.get(self.user_url, params=self.authparam())
        return r.json()

if __name__ == "__main__":
    b = Beeminder()
    print ("User:", b.user)
    print ("My Goals:", b.goals)
    print ("Yesterday:")
    print (b.yesterdayparam("cccc",111))
