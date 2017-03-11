from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import API
import json
from pygeocoder import Geocoder
import requests
import os


def main():

    exCoords = [59.925639, 10.722448]

    url = "http://animalia-life.com/data_images/bird/bird1.jpg"
    geoData = Geocoder.reverse_geocode(exCoords[0], exCoords[1])
    message = "TEST: Pothole encountered at (" + str(exCoords[0]) + "," + str(exCoords[1]) + ") in " + str(geoData.street_name) + ", " + str(geoData.city)
    print(message)
    tweet_image(url, message)


def get_twitter_auth_api():
    consumer_key = 'uwCTYRKSGNpvm88llOymBsZA2'
    consumer_secret = 'wdLTbXwwqaVBaeh6BI8dmbJMoJE1pO8kQZ1lss8sXvzbpJ9yjE'
    access_token = '840258538672934912-ExVJ3XSfqbQrIDIlwz6yJs5S0XsePNb'
    access_token_secret = 'YH5TSRXWOZ1RvqhjY4SZUcHptnvNsTiffc1qBBDbAGyQ2'

    #This handles Twitter authetification and the connection to Twitter Streaming API
    listener = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = API(auth)
    print api.me().name

    return [auth, api]

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):

        out = json.loads(data)

        if 'limit' not in out.keys():
            print(out['created_at'][0:16] + ' by ' + out['user']['name'] + ': ' + out['text'].rjust(10))

        return True

    def on_error(self, status):
        print(status)


def tweet_image(url, message):
    [auth, api] = get_twitter_auth_api()
    filename = 'temp.jpg'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)

        api.update_with_media(filename, status=message)
        os.remove(filename)
    else:
        print("Unable to download image")





    #stream = Stream(auth, listener)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    #stream.filter(track=keyFilter)
    #stream.filter(locations=[-6.38,49.87,1.77,55.81]) #geobox with allocated corners

main()