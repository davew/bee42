#Beeminder tools

Goal: Provide clean, simple, pythonic access to the Beeminder API. Specifically
to post Strava activities to Beeminder.

I haven't done much programming in recent years. Please challenge me if you
feel that I am over complicating things or not doing them in the most pythonic
way or can improve the code in anyway.

I am coding this in Python 3, although I'm not deliberately seeking to make it
incompatible with Python 2.7. Hence, I will accept ideas to enable people to use
it with Python 2.7 where possible.

This requires Stravalib. I am using the current released version (hence having
to set logging to error only as it issues lots of warnings). I installed this
in my virtual environment using

pip install Stravalib

It automatically uses the 2to3 code to update it to Python 3 syntax.

I can now use the beestrava.py script to add my last 15 strava activities to
Beeminder without getting duplicates.
