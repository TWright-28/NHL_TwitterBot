import pandas as pd

# Your JSON data as a dictionary
data = {
    "ID8470616": {
        "person": {
            "id": 8470616,
            "fullName": "Ryan Kesler",
            "link": "/api/v1/people/8470616",
            "shootsCatches": "R",
            "rosterStatus": "Y"
        },
        "jerseyNumber": "17",
        "position": {
            "code": "C",
            "name": "Center",
            "type": "Forward",
            "abbreviation": "C"
        },
        "stats": {
            "skaterStats": {
                "timeOnIce": "19:14",
                "assists": 0,
                "goals": 0,
                "shots": 1,
                "hits": 2,
                "powerPlayGoals": 0,
                "powerPlayAssists": 0,
                "penaltyMinutes": 0,
                "faceOffPct": 60.87,
                "faceOffWins": 14,
                "faceoffTaken": 23,
                "takeaways": 1,
                "giveaways": 0,
                "shortHandedGoals": 0,
                "shortHandedAssists": 0,
                "blocked": 1,
                "plusMinus": 0,
                "evenTimeOnIce": "14:35",
                "powerPlayTimeOnIce": "2:09",
                "shortHandedTimeOnIce": "2:30"
            }
        }
    },
    "ID8468535": {
        "person": {
            "id": 8468535,
            "fullName": "Antoine Vermette",
            "link": "/api/v1/people/8468535",
            "shootsCatches": "L",
            "rosterStatus": "Y"
        },
        "jerseyNumber": "50",
        "position": {
            "code": "C",
            "name": "Center",
            "type": "Forward",
            "abbreviation": "C"
        },
        "stats": {
            "skaterStats": {
                "timeOnIce": "13:08",
                "assists": 0,
                "goals": 1,
                "shots": 3,
                "hits": 0,
                "powerPlayGoals": 0,
                "powerPlayAssists": 0,
                "penaltyMinutes": 0,
                "faceOffPct": 53.33,
                "faceOffWins": 8,
                "faceoffTaken": 15,
                "takeaways": 0,
                "giveaways": 0,
                "shortHandedGoals": 0,
                "shortHandedAssists": 0,
                "blocked": 0,
                "plusMinus": 2,
                "evenTimeOnIce": "10:56",
                "powerPlayTimeOnIce": "1:23",
                "shortHandedTimeOnIce": "0:49"
            }
        }
    },
    "ID8467400": {
        "person": {
            "id": 8467400,
            "fullName": "Francois Beauchemin",
            "link": "/api/v1/people/8467400",
            "shootsCatches": "L",
            "rosterStatus": "Y"
        },
        "jerseyNumber": "23",
        "position": {
            "code": "N/A",
            "name": "Unknown",
            "type": "Unknown",
            "abbreviation": "N/A"
        },
        "stats": {}
    }
}

# Extract relevant data and create a list of dictionaries
player_data = []

for player_id, player_info in data.items():
    player_dict = {
        "fullName": player_info["person"]["fullName"],
        "positionName": player_info["position"]["name"]
    }
    skater_stats = player_info.get("stats", {}).get("skaterStats", {})
    player_dict.update(skater_stats)
    player_data.append(player_dict)

# Create a DataFrame from the list of player dictionaries
df = pd.DataFrame(player_data)

# Now you have your data in a Pandas DataFrame
print(df)