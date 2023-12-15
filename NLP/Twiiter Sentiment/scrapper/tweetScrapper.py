import tweepy

# Twitter API credentials
consumer_key = 'eAS3iOvUyGWqxBxbIEaOkAEq3'
consumer_secret = 'IhUDpxg30jn0hpy2kbOaDt0yqXkgNCRivtZvqjzwk4fZ6KpgPp'
access_key = '1324938826293239808-KluVDzQbgYOWFsVrSHdX7jQrbDZfTi'
access_secret = 'QsUQJ0cvOI6FX1f46xWT2yp85pNgsvPDJNyxT1d3OrhRc'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

#Stream tweets
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        try:
            print(f"{status.user.screen_name}: {status.text}")
        except Exception as e:
            print(f"Error: {e}")

    def on_error(self, status_code):
        print(f"Error with status code: {status_code}")
        return True  # Don't kill the stream

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

try:
    myStream.filter(languages=['en'])
except KeyboardInterrupt:
    print("Stopped.")
finally:
    myStream.disconnect()