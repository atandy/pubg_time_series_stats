import requests
import os
import time
import pandas as pd

# Get Pubg Player Data from API
# By default, this script :
    # gets NA data in a Pandas Dataframe
    # gets Duo Data
    # is requesting data from player: tandyman
    # you can update these things. 

# Required API Key 
# https://developer.playbattlegrounds.com/
PUBG_KEY=os.getenv('PUBG_KEY')

header = {
  "Authorization": "Bearer {}".format(PUBG_KEY),
  "Accept": "application/vnd.api+json"
}



def get_player(player_name):
  url = "https://api.pubg.com/shards/pc-na/players?filter[playerNames]={}".format(player_name)  
  r = requests.get(url, headers=header)
  return r

def get_player_id(player_response):    
    return player_response.json()['data'][0]['id']


def get_matches(player_response):
    ''' return list of match id strings'''
    return [match['id'] for match in player_response.json()['data'][0]['relationships']['matches']['data']]

def get_match(match_id):
    url = 'https://api.pubg.com/shards/pc-na/matches/{}'.format(match_id)
    return requests.get(url, headers=header).json()

def get_player_performance(match_info, player_id):
    for player_performance in match_info['included']:
        try:
            if player_performance['attributes']['stats']['playerId'] == player_id:
                return player_performance
        except:
            pass

player = get_player('tandyman')
    
player_id = get_player_id(player)
matches_list = get_matches(player)


# get all performances from each match. 
my_performances = []
for match_id in matches_list:
    match_info = get_match(match_id)
    
    # only get duo games
    if not match_info['data']['attributes']['gameMode'] == 'duo-fpp':
        continue
    
    created_at = match_info['data']['attributes']['createdAt']
    match_performance = get_player_performance(match_info, player_id)
    match_performance['createdAt'] = created_at

    my_performances.append(match_performance)
    print(match_performance)
    time.sleep(7)

    

# get the stats specifically from each match performance
stats_list = []
for perf in my_performances:
    stats = match_performance['attributes']['stats']
    stats['createdAt'] = match_performance['createdAt']
    stats_list.append(stats)

# print the data frame of stats
print(pd.DataFrame.from_records(stats_list))
