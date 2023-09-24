import tweepy
from keys import consumer_key, consumer_secret, access_token, access_token_secret, bearer_token
import requests
import json
from datetime import date
import pandas as pd
import seaborn as sns
import numpy as np
import os
import matplotlib.pyplot as plt

#GETTING TODAYS DATE

# today = date.today()
# today = today.strftime("%Y-%m-%d")

today = '2018-01-02'

#Using todays date, we will request the schedule data from the NHL undocumented API. 
todaysData = requests.get('https://statsapi.web.nhl.com/api/v1/schedule?startDate=' + today + '&endDate=' + today).text
jsonData = json.loads(todaysData)

#Now we will clean the data a bit. 
jsonData = jsonData['dates'][0]['games']
 
gameInfo = {}
 
#This loops through all the games today, will grab the live game link, the home team and the away team. It is then saved into a dictionary.
for team in jsonData:
    gameLiveFeed = 'https://statsapi.web.nhl.com' + team['link']
    awayTeamName = team['teams']['away']['team']['name']
    homeTeamName = team['teams']['home']['team']['name']
    
    gameInfo[gameLiveFeed] = {"Home": homeTeamName, "Away": awayTeamName}


# Now that we have a dictionary of the live games, lets access each game link and grab the stats from that game. 

for gameLink in gameInfo:
    specGameData = requests.get(gameLink).text
    rawGameData = json.loads(specGameData)
    
    #grabbing all player data from each gamee
    awayplayerData = rawGameData['liveData']['boxscore']['teams']['away']['players']
    homeplayerData = rawGameData['liveData']['boxscore']['teams']['home']['players']
    PlayerData = []

    #looping though each playerId
    for player_id, player_info in awayplayerData.items():
        player_dict = {
            "NHL_id" : player_id,
           "fullName": player_info["person"]["fullName"],
            "positionName": player_info["position"]["name"],
            "team" : rawGameData['liveData']['boxscore']['teams']['away']['team']['name'],
        }
        skater_stats = player_info.get("stats", {}).get("skaterStats", {})
        player_dict.update(skater_stats)
        PlayerData.append(player_dict)
    
    for player_id, player_info in homeplayerData.items():
        player_dict = {
            "NHL_id" : player_id,
           "fullName": player_info["person"]["fullName"],
            "positionName": player_info["position"]["name"],
            "team" : rawGameData['liveData']['boxscore']['teams']['home']['team']['name'],
        }
        skater_stats = player_info.get("stats", {}).get("skaterStats", {})
        player_dict.update(skater_stats)
        PlayerData.append(player_dict)

    # Create a DataFrame from the list of player from the game 
    df = pd.DataFrame(PlayerData)
    # Clean data now
    # Dropping rows(players) if their TOI is NaN, basically meaning they were a healthy scratch and wont have any statistics
    df = df[df['timeOnIce'].notna()]
    df['faceOffPct'].fillna(0, inplace = True)
    # Now we want to start to do some statstical analysis of the game stats.

    df['weightedOffence'] = df.apply(lambda row: ((row.assists)*0.75 + (row.goals)*1 + (row.shots)*0.08 + (row.takeaways)*0.2 + (row.faceOffPct-50)/100), axis = 1)
    df['weightedDefence'] = df.apply(lambda row: ((row.giveaways)*(-0.5) + (row.faceOffPct-50)/100 + (row.takeaways)*0.2 + (row.blocked)*0.2 + (row.plusMinus)*0.5), axis = 1)
    df['Overall'] = df.apply(lambda row: ((row.weightedOffence) + (row.weightedDefence)), axis =1 )
    df = df.sort_values(by='Overall', ascending=False)
    df.plot(y=["Overall" , "weightedOffence" , "weightedDefence"], x="fullName", kind="bar")
    plt.savefig(gameLink[41:51] + '.pdf')

   
    
    
####################### TWITTER STIFF ####################################

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

