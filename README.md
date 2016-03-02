#Beeminder tools

Goal: Provide clean, simple, pythonic access to the Beeminder API.

I haven't done much programming in recent years. Please challenge me if you feel that I am over complicating things or not doing them in the most pythonic way.

Tasks (leading to updating Beeminder Strava goals for both running and cycling. For each supporting occurances and distances (in miles of km)

1. Get a user from the API, create a user object. Throw exceptions for all possible error conditions.
2. Get a simple goal from the API, create a goal object. Throw exceptions for all possible error conditions.
3. Get the timestamp of the last datapoint (so I know how far back to go in Strava)
4. Get all the activities from the last datapoint timestamp
5. Check which activities fit the goal
6. Post the activities as datapoints (keep track of duplicates).
