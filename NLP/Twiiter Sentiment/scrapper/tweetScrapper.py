import tweepy

# Twitter API credentials
consumer_key = ''
consumer_secret = ''
access_key = ''
access_secret = ''
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text) #store to database if possible

    def on_error(self, status_code):
        if status_code == 420:
            return False

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)