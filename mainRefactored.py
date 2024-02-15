import tweepy
from keys import consumer_key, consumer_secret, access_token, access_token_secret, bearer_token
import requests
import json
from datetime import date
import pandas as pd
import os.path
import matplotlib.pyplot as plt
import numpy as np


####################### TWITTER STIFF ####################################

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

    #V2 Endpoint

client = tweepy.Client(
    bearer_token,
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret,
    wait_on_rate_limit=True
    )
    #GETTING TODAYS DATE


def get_winning_goalie(gameId):
    # Loop through gameWeeks
    for week in jsonDataRaw['gameWeek']:
        # Loop through games in each week
        for game in week['games']:
            # Check if gameId matches
            if game['id'] == gameId:
                # Return winning goalie
                return game['winningGoalie']['lastName']['default']



# today = date.today()
# today = today.strftime("%Y-%m-%d")
today = '2023-09-25'

    #Using todays date, we will request the schedule data from the NHL undocumented API. 
# todaysData = requests.get('https://statsapi.web.nhl.com/api/v1/schedule?startDate=' + today + '&endDate=' + today).text
todaysData = requests.get('https://api-web.nhle.com/v1/schedule/' + today).text

jsonDataRaw = json.loads(todaysData)

    #Now we will clean the data a bit. 
jsonData = jsonDataRaw['gameWeek'][0]['games']

gameInfo = {}
    
# #     #This loops through all the games today, will grab the live game link, the home team and the away team. It is then saved into a dictionary.
for games in jsonData:
    gameId = games['id']
    gameLiveFeed = 'https://api-web.nhle.com/v1/gamecenter/' + str(gameId) + '/boxscore'
    homeTeamName = games['homeTeam']['placeName']['default']
    awayTeamName = games['awayTeam']['placeName']['default']
    
    gameInfo[gameLiveFeed] = {"Home": homeTeamName, "Away": awayTeamName}

# Now that we have a dictionary of the live games, lets access each game link and grab the stats from that game. 

for gameLink in gameInfo:
        specGameData = requests.get(gameLink).text
        rawGameData = json.loads(specGameData)

        try:         
            gameStatus = rawGameData['gameState']
            if(gameStatus == "FINAL"):
                
                winning_goalie = get_winning_goalie(gameLink[39:49])
                
                # Pulling skater data from the GameLink Boxscore
                awayForwardData = rawGameData['boxscore']['playerByGameStats']['awayTeam']['forwards']
                awayDefenseData = rawGameData['boxscore']['playerByGameStats']['awayTeam']['defense']
                awayTeamName = rawGameData['awayTeam']['name']['default']
                awayTeamAbv = rawGameData['awayTeam']['abbrev']
                awayGoalieData = rawGameData['boxscore']['playerByGameStats']['awayTeam']['goalies']
                awayPlayerList = awayForwardData + awayDefenseData
                
                homeForwardData = rawGameData['boxscore']['playerByGameStats']['homeTeam']['forwards']
                homeDefenseData = rawGameData['boxscore']['playerByGameStats']['homeTeam']['defense']
                homeTeamName = rawGameData['homeTeam']['name']['default']
                homeTeamAbv = rawGameData['homeTeam']['abbrev']
                homeGoalieData = rawGameData['boxscore']['playerByGameStats']['homeTeam']['goalies']
                homePlayerList = homeForwardData + homeDefenseData
                
                PlayerData = []
                GoalieData = []
                
                #Creatomg the name for game JPG
                awayFile = gameLink[39:49] + "_" + awayTeamAbv + ".jpg"
                homeFile = gameLink[39:49] + "_" + homeTeamAbv + ".jpg"
                
                #Checking if the file already exists
                homeFile_exists = os.path.exists(homeFile)
                awayFile_exists = os.path.exists(awayFile)
                
                # print(homeList)
                #cont if neither of the files exist
                if homeFile_exists == False & awayFile_exists == False:
                    for player in awayPlayerList:
                        player_dict = {
                            "NHL_id" : player['playerId'],
                            "name" : player['name']['default'],
                            "team" : awayTeamName,
                            "position": player['position'],
                            "toi": player['toi'],
                            "goals": player['goals'],
                            "assists": player['assists'],
                            "points": player['points'],
                            "powerPlayPoints": player['powerPlayPoints'],
                            "shots": player['shots'],
                            "plusMinus": player['plusMinus'],
                            "pim": player['pim'],
                            "hits": player['hits'],
                            "blocks": player['blockedShots'],
                        }
                        PlayerData.append(player_dict)
                    
                    for player in homePlayerList:
                        player_dict = {
                            "NHL_id" : player['playerId'],
                            "name" : player['name']['default'],
                            "team" : homeTeamName,
                            "position": player['position'],
                            "toi": player['toi'],
                            "goals": player['goals'],
                            "assists": player['assists'],
                            "points": player['points'],
                            "powerPlayPoints": player['powerPlayPoints'],
                            "shots": player['shots'],
                            "plusMinus": player['plusMinus'],
                            "pim": player['pim'],
                            "hits": player['hits'],
                            "blocks": player['blockedShots'],
                        }
                        PlayerData.append(player_dict)

                    for goalie in awayGoalieData:
                        goalie_dict = {
                            "NHL_id" : goalie['playerId'],
                            "team": awayTeamName,
                            "goalsAgaints" : goalie['goalsAgainst'],
                            "toi": goalie['toi'],
                            "goalsAgainst": goalie['goalsAgainst'],
                            "saveShotsAgainst": goalie['saveShotsAgainst'],
                        }
                        GoalieData.append(goalie_dict)
                        
                    for goalie in homeGoalieData:
                        goalie_dict = {
                            "NHL_id" : goalie['playerId'],
                            "team": homeTeamName,
                            "goalsAgaints" : goalie['goalsAgainst'],
                            "toi": goalie['toi'],
                            "goalsAgainst": goalie['goalsAgainst'],
                            "saveShotsAgainst": goalie['saveShotsAgainst'],
                        }
                        GoalieData.append(goalie_dict)
                        
                 # Create a DataFrame from the list of player from the game 
                    df_player = pd.DataFrame(PlayerData)
                    df_goalie = pd.DataFrame(GoalieData)
#                     # Clean data now
#                     # Dropping rows(players) if their TOI is NaN, basically meaning they were a healthy scratch and wont have any statistics
                    df_player = df_player[df_player['toi'].notna()]
                    df_goalie = df_goalie[df_goalie['toi'].notna()]
                    
                    df_player['Offence'] = df_player.apply(lambda row: ((row.assists)*4 + (row.goals)*6), axis = 1)
                    df_player['MicroStats'] = df_player.apply(lambda row: ((row.hits)*1 + (row.blocks)*1 + (row.plusMinus)*0.5 + (row.shots)*0.9 + (row.pim)*0.5) + (row.powerPlayPoints)*2, axis = 1)
                    df_player['Overall'] = df_player.apply(lambda row: ((row.Offence) + (row.MicroStats)), axis =1 )
                    # df_goalie = df_goalie.apply(lambda row: ((row.goalsAgainst)*(-3) + (row.saveShotsAgainst.split('/')[0])*0.6 ))
                    # df = df.sort_values(by='Overall', ascending=False)
                      
    

        except:
            print("not enough data")

            

#         try:
#             #grabbing all player data from each gamee         
#             gameStatus = rawGameData['gameData']['status']['abstractGameState']
#             if(gameStatus == "Final"):
            
#                 awayplayerData = rawGameData['liveData']['boxscore']['teams']['away']['players']
#                 awayTeam = rawGameData['gameData']['teams']['away']['name']
#                 awayTeamABV = rawGameData['gameData']['teams']['away']['abbreviation']
#                 homeplayerData = rawGameData['liveData']['boxscore']['teams']['home']['players']
#                 homeTeam = rawGameData['gameData']['teams']['home']['name']
#                 homeTeamABV = rawGameData['gameData']['teams']['home']['abbreviation']
                
#                 PlayerData = []
                
#                 awayFile = gameLink[41:51] + "_" + awayTeamABV + ".jpg"
#                 homeFile = gameLink[41:51] + "_" + homeTeamABV + ".jpg"
                
#                 homeFile_exists = os.path.exists(homeFile)
#                 awayFile_exists = os.path.exists(awayFile)
                
#                 if homeFile_exists == False & awayFile_exists == False:

#                     #looping though each playerId
#                     for player_id, player_info in awayplayerData.items():
#                         player_dict = {
#                             "NHL_id" : player_id,
#                             "fullName": player_info["person"]["fullName"],
#                             "positionName": player_info["position"]["name"],
#                             "team" : rawGameData['liveData']['boxscore']['teams']['away']['team']['name'],
#                         }
#                         skater_stats = player_info.get("stats", {}).get("skaterStats", {})
#                         player_dict.update(skater_stats)
#                         PlayerData.append(player_dict)
                    
#                     for player_id, player_info in homeplayerData.items():
#                         player_dict = {
#                             "NHL_id" : player_id,
#                             "fullName": player_info["person"]["fullName"],
#                             "positionName": player_info["position"]["name"],
#                             "team" : rawGameData['liveData']['boxscore']['teams']['home']['team']['name'],
#                         }
#                         skater_stats = player_info.get("stats", {}).get("skaterStats", {})
#                         player_dict.update(skater_stats)
#                         PlayerData.append(player_dict)

#                     # Create a DataFrame from the list of player from the game 
#                     df = pd.DataFrame(PlayerData)
#                     # Clean data now
#                     # Dropping rows(players) if their TOI is NaN, basically meaning they were a healthy scratch and wont have any statistics
#                     df = df[df['timeOnIce'].notna()]
#                     df['faceOffPct'].fillna(0, inplace = True)
#                     # Now we want to start to do some statstical analysis of the game stats.

#                     df['Offence'] = df.apply(lambda row: ((row.assists)*0.75 + (row.goals)*1 + (row.shots)*0.08 + (row.takeaways)*0.2 ), axis = 1)
#                     df['Defence'] = df.apply(lambda row: ((row.giveaways)*(-0.5) + (row.faceOffPct-50)/100 + (row.takeaways)*0.2 + (row.blocked)*0.2 + (row.plusMinus)*0.5), axis = 1)
#                     df['Overall'] = df.apply(lambda row: ((row.Offence) + (row.Defence)), axis =1 )
#                     df = df.sort_values(by='Overall', ascending=False)
                    
#                     #Creating dataframes for each team and their players
#                     dfteam1 = df.loc[df['team'] == awayTeam]
#                     dfteam2 = df.loc[df['team'] == homeTeam]
                    
#                     #Now plotting each df

#                     dfteam1.plot(y=["Overall" , "Offence" , "Defence"], x="fullName", kind="bar", title=awayTeam)
#                     plt.tight_layout()
#                     plt.savefig(gameLink[41:51] + '_' + awayTeamABV + '.jpg')
#                     plt.cla()
                    
#                     dfteam2.plot(y=["Overall" , "Offence" , "Defence"], x="fullName", kind="bar", title = homeTeam)
#                     plt.tight_layout()
#                     plt.savefig(gameLink[41:51] + '_' + homeTeamABV + '.jpg')
#                     plt.cla()
#                     awayFile = gameLink[41:51] + "_" + awayTeamABV + ".jpg"
#                     homeFile = gameLink[41:51] + "_" + homeTeamABV + ".jpg"
#                     media_Id_Away = api.media_upload(filename=awayFile).media_id_string
#                     media_Id_Home = api.media_upload(filename= homeFile).media_id_string
#                     #description to be tweeted
#                     msg = today + ': ' + awayTeam + ' vs ' + homeTeam + ' Game Statistics:'
#                     print(msg)
#                     client.create_tweet(text=msg, media_ids=[media_Id_Away, media_Id_Home])
#                 else: 
#                     print("Alredy have the game scores for " + homeTeamABV + ' ' + awayTeamABV)
#         except:
#             print('Not enough Game Stats')
            
#     #upload media to twtiite
