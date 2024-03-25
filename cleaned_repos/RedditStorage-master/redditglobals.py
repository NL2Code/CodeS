import praw

global USERAGENT, USERNAME, PASSWORD, SUBREDDIT, r

USERAGENT = "reddit storage bot"
USERNAME = ""
PASSWORD = ""
SUBREDDIT = "redditstoragetest"


r = praw.Reddit(USERAGENT)
