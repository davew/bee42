import requests
import datetime
import configparser

BEE42_INI           = "bee42.ini"
BEE42_INI_BEEMINDER = "BeeMinder"
BEE42_INI_USERNAME  = "Username"
BEE42_INI_TOKEN     = "Token"
BEE42_INI_API_URL   = "Api_Url"

BEE42_WEIGHT_GOAL   = "Weight_Goal"

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
        
        self.weight_goal = self.ini_beeminder[BEE42_WEIGHT_GOAL]

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

    def getGoal(self, goal):
        r = requests.get(self.goal_url(goal), params=self.authparam())
        return r.json()

    def getGoalCurValue(self, goal):
        g = self.getGoal(goal)
        return g["curval"]
      
if __name__ == "__main__":
    b = Beeminder()
    print ("User:", b.user)
    print ("My Goals:", b.goals)
    print ("Weight Goal:")
    print (b.getGoal(b.weight_goal))
    print ("Current Weight:", b.getGoalCurValue(b.weight_goal))
