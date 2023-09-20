import tweepy
from keys import consumer_key, consumer_secret, access_token, access_token_secret, bearer_token
import requests
import json
from datetime import date

#today = date.today()
#today = today.strftime("%Y-%m-%d")

today = '2018-01-02'


print(today)
todaysGames = requests.get('https://statsapi.web.nhl.com/api/v1/schedule?startDate=' + today + '&endDate=' + today).text
jsonData = json.loads(todaysGames)
todaysnumGames = jsonData['totalGames']

print(todaysnumGames)

# #V1 Endpoint 
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
# api = tweepy.API(auth, wait_on_rate_limit=True)

# #V2 Endpoint

# client = tweepy.Client(
#     bearer_token,
#     consumer_key,
#     consumer_secret,
#     access_token,
#     access_token_secret,
#     wait_on_rate_limit=True
# )

# #upload media to twtiiter

# media_Id = api.media_upload(filename="unnamed.jpg").media_id_string
# print(media_Id)

# #description to be tweeted
# msg = "Test run"

# client.create_tweet(text=msg, media_ids=[media_Id])
# print("twweeteted")