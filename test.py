import requests
import configparser

# config.iniファイルの読み込み
config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')
api_key = config_ini['DEFAULT']['key']

REGION = 'kr'

def get_challenger_summoners(api_key, region):
    url = f'https://{region}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['entries']
    else:
        print(f"Error: {response.status_code}")
        return None

def get_matchlist_by_summoner(api_key, region, summoner_id):
    url = f'https://{region}.api.riotgames.com/lol/match/v4/matchlists/by-account/{summoner_id}?api_key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['matches']
    else:
        print(f"Error: {response.status_code}")
        return None

def get_match_details(api_key, region, match_id):
    url = f'https://{region}.api.riotgames.com/lol/match/v4/matches/{match_id}?api_key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None
