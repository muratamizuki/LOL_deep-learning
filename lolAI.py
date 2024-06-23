import requests
import configparser

# config.iniファイルの読み込み
config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')
API_KEY = config_ini['DEFAULT']['key']

REGION = 'kr'  # 韓国サーバー

# チャレンジャーリーグのサモナーを取得
def get_challenger_summoners(api_key, region):
    league_url = f'https://{region}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key={api_key}'
    response = requests.get(league_url)
    if response.status_code == 200:
        league_data = response.json()
        summoner_ids = [entry['summonerId'] for entry in league_data['entries']]
        return summoner_ids
    else:
        print(f"Error fetching challenger league data: {response.status_code}, {response.text}")
        return []

# サモナーごとのマッチリストを取得
def get_matchlist(api_key, region, summoner_id):
    matchlist_url = f'https://{region}.api.riotgames.com/lol/match/v4/matchlists/by-account/{summoner_id}?api_key={api_key}'
    response = requests.get(matchlist_url)
    if response.status_code == 200:
        matchlist_data = response.json()
        return matchlist_data['matches']
    else:
        print(f"Error fetching match list: {response.status_code}, {response.text}")
        return []

# 試合の詳細データを取得
def get_match_details(api_key, region, match_id):
    match_url = f'https://{region}.api.riotgames.com/lol/match/v4/matches/{match_id}?api_key={api_key}'
    response = requests.get(match_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching match details: {response.status_code}, {response.text}")
        return {}

# メインの処理
def main():
    summoner_ids = get_challenger_summoners(API_KEY, REGION)
    all_matches = []

    for summoner_id in summoner_ids:
        matches = get_matchlist(API_KEY, REGION, summoner_id)
        for match in matches:
            match_id = match['gameId']
            match_details = get_match_details(API_KEY, REGION, match_id)
            all_matches.append(match_details)

    # 収集した試合の詳細データの表示（または保存）
    for match in all_matches:
        print(f"Match ID: {match['gameId']}, Game Duration: {match['gameDuration']}, Participants: {len(match['participants'])}")

if __name__ == "__main__":
    main()
