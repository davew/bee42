import configparser

from bee42.bee42 import User
from bee42.bee42 import Datapoint

BEE42_INI = "bee42.ini"
BEE42_INI_BEEMINDER = "BeeMinder"
BEE42_INI_USERNAME = "Username"
BEE42_INI_TOKEN = "Token"

def dave():
    config = configparser.ConfigParser()
    config.read(BEE42_INI)

    ini_beeminder = config[BEE42_INI_BEEMINDER]
    username = ini_beeminder[BEE42_INI_USERNAME]
    token = ini_beeminder[BEE42_INI_TOKEN]

    user = User(username, token)
    print("Username:", user.username, "tz:", user.timezone, "update:", user.updated_at, "goals", user.goalslugs, "db:", user.deadbeat)

    goal = user.load_goal("cyclemore")
    print("Slug:", goal.slug, "Title:", goal.title, "Desc:", goal.description, "Val:", goal.goalval, "init:", goal.initday)

    dp = Datapoint(user, "testmore")
    dp.value = 2
    dp.comment = "an autotest"
    dp.post()

    dps = user.getDatapoints("testmore")
    print("DPS:", dps)
    
if __name__ == "__main__":
    dave()

