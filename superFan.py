import praw
import config
import configTwitter
import tweepy, time, sys, os

#REDDIT
def bot_login():
	print("Logging in...")
	r = praw.Reddit(username = config.username,
			password = config.password,
			client_id = config.client_id,
			client_secret = config.client_secret,
			user_agent = "Raptors bot v1.0")
	print("Logged in!")
	return r

def run_bot(r,submissionTitle,submissionID,submissionURL,counter):
	nba = r.subreddit('nba')
	raptors = r.subreddit('torontoraptors')

	for submission in raptors.hot(limit=5):
		if submission.id not in submissionID:
			submissionTitle.append(submission.title)
			submissionID.append(submission.id)
			submissionURL.append(submission.url)
			counter += 1
			with open("submissionIDs.txt" , "a") as f:
				f.write(submission.id + "\n")
	time.sleep(5)
	return (submissionTitle,submissionURL,counter)

def getPreviousPosts():
	if not os.path.isfile("submissionIDs.txt"):
		submissionID = []
	else:
		with open("submissionIDs.txt", "r") as f:
			submissionID = f.read()
			submissionID = submissionID.split("\n")

	return submissionID

r = bot_login()
submissionTitle = []
submissionID = getPreviousPosts()
submissionURL = []
counter = 0
submissionTitle,submissionURL,counter = run_bot(r,submissionTitle,submissionID,submissionURL,counter)

#Twitter
auth = auth = tweepy.OAuthHandler(configTwitter.consumer_key, configTwitter.consumer_secret)
auth.set_access_token(configTwitter.access_token, configTwitter.access_token_secret)
tweets = []
message = ""
for i in range(0,counter):
	message = submissionTitle[i] + '\n\n' + submissionURL[i]
	tweets.append(message)
api = tweepy.API(auth)
for x in range(1,counter):
	api.update_status(tweets[x])
	time.sleep(5)
