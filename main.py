import tweepy
from keys import consumer_key, consumer_secret, access_token, access_token_secret, bearer_token
import requests
import json
from datetime import date
import pandas as pd
#today = date.today()
#today = today.strftime("%Y-%m-%d")

today = '2018-01-02'


print(today)
todaysData = requests.get('https://statsapi.web.nhl.com/api/v1/schedule?startDate=' + today + '&endDate=' + today).text
jsonData = json.loads(todaysData)

jsonData = jsonData['dates'][0]['games']
 
gameInfo = {}
 
for team in jsonData:
    gameLiveFeed = 'https://statsapi.web.nhl.com' + team['link']
    awayTeamName = team['teams']['away']['team']['name']
    homeTeamName = team['teams']['home']['team']['name']
    
    gameInfo[gameLiveFeed] = {"Home": homeTeamName, "Away": awayTeamName}

print(gameInfo)
    

# print(todaysnumGames)

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



def add_keys_nested_dict(d, keys):
    for key in keys:
        if key not in d:
            d[key] = {}
        d = d[key]
    d.setdefault(keys[-1], 1)