import logging
logging.basicConfig(level=logging.ERROR)

import configparser
from datetime import datetime
from bee42.bee42 import User
from bee42.bee42 import Datapoint
from stravalib import Client 
from stravalib import unithelper 

BEE42_INI = "bee42.ini"
BEE42_INI_BEEMINDER = "BeeMinder"
BEE42_INI_USERNAME = "Username"
BEE42_INI_TOKEN = "Token"
BEE42_INI_STRAVA_TOKEN = "Strava_Token"

RUN_GOAL_SLUG = "run5"
RIDE_GOAL_SLUG = "cycle50"


def dave():
    config = configparser.ConfigParser()
    config.read(BEE42_INI)

    ini_beeminder = config[BEE42_INI_BEEMINDER]
    username = ini_beeminder[BEE42_INI_USERNAME]
    token = ini_beeminder[BEE42_INI_TOKEN]
    strava_token = ini_beeminder[BEE42_INI_STRAVA_TOKEN]

    user = User(username, token)
    print("Username:", user.username, "tz:", user.timezone, "update:", user.updated_at, "goals", user.goalslugs, "db:", user.deadbeat)

    strava_client = Client(access_token=strava_token)
    strava_athlete = strava_client.get_athlete()
    print(strava_athlete.firstname)

    strava_activities = strava_client.get_activities(limit=15)

    for a in strava_activities:
        if (a.type == "Run"):
            print(add_run(user, a))
        elif (a.type == "Ride"):
            print(add_ride(user, a))

def add_run(user, activity):
    return add_activity(user, RUN_GOAL_SLUG, activity, unithelper.kilometers(activity.distance)):

def add_ride(user, activity):
    return add_activity(user, RIDE_GOAL_SLUG, activity, unithelper.miles(activity.distance)):

def add_activity(user, goal_slug, activity, value):
    dp = Datapoint(user, goal_slug)
    dp.value = value
    dp.comment = activity.name
    dp.requestid = activity.id
    dp.timestamp = activity.start_date.timestamp()
    return dp.post()    
    
if __name__ == "__main__":
    dave()

