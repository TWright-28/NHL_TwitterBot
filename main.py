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

for team in jsonData:
    teamList = team['teams']['away']['team']['name']
    print(json.dumps(teamList, indent=4))

    # for awayList in teamList:
    #     awayLists = awayList['team']
    #     for awayTeam in awayLists:
    #         awayTeamDetail = awayTeam['team']
    #         for awayTeamName in awayTeamDetail:
    #             print(awayTeamName['name'])
    

#   for awayTeam in teamList:
#     awayTeamName = awayTeam['away']
#     for awayTeamFinalname in awayTeamName:
                





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