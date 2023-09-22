import tweepy
from keys import consumer_key, consumer_secret, access_token, access_token_secret, bearer_token
import requests
import json
from datetime import date
import pandas as pd

#GETTING TODAYS DATE

#today = date.today()
#today = today.strftime("%Y-%m-%d")

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
    
    playerData = rawGameData['liveData']['boxscore']['teams']['away']['players']
       
    player_data = []

    for player_id, player_info in playerData.items():
        player_dict = {
           "fullName": player_info["person"]["fullName"],
            "positionName": player_info["position"]["name"]
        }
        skater_stats = player_info.get("stats", {}).get("skaterStats", {})
        player_dict.update(skater_stats)
        player_data.append(player_dict)

# Create a DataFrame from the list of player dictionaries
    df = pd.DataFrame(player_data)
    print(df)
    
    #Now  that we have the game data, we want to grab each individual players statistics for the game. 
    
    
    
    
    
    
    
    
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

