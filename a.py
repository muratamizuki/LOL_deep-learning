import requests
import configparser
import sqlite3

# config.iniファイルの読み込み
config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')
api_key = config_ini['DEFAULT']['key']

REGION = 'kr'

def get_challenger_summoners(api_key, region):
    url = f'https://{region}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()['entries']
        print(f"Fetched {len(data)} challenger summoners")
        return data
    else:
        print(f"Error fetching challenger summoners: {response.status_code} - {response.text}")
        return None

def get_matchlist_by_summoner(api_key, region, summoner_id):
    url = f'https://{region}.api.riotgames.com/lol/match/v4/matchlists/by-account/{summoner_id}?api_key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()['matches']
        print(f"Fetched {len(data)} matches for summoner_id {summoner_id}")
        return data
    else:
        print(f"Error fetching match list: {response.status_code} - {response.text}")
        return None

def get_match_details(api_key, region, match_id):
    url = f'https://{region}.api.riotgames.com/lol/match/v4/matches/{match_id}?api_key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(f"Fetched match details for match_id {match_id}")
        return data
    else:
        print(f"Error fetching match details: {response.status_code} - {response.text}")
        return None

def init_db():
    conn = sqlite3.connect('kr_data.db')
    c = conn.cursor()
    
    c.execute('''
    CREATE TABLE IF NOT EXISTS summoners (
        summoner_id TEXT PRIMARY KEY,
        summoner_name TEXT
    )
    ''')
    
    c.execute('''
    CREATE TABLE IF NOT EXISTS matches (
        match_id TEXT PRIMARY KEY,
        summoner_id TEXT,
        champion_id INTEGER,
        role TEXT,
        lane TEXT,
        FOREIGN KEY(summoner_id) REFERENCES summoners(summoner_id)
    )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized")

def save_summoner_info(summoner_id, summoner_name):
    conn = sqlite3.connect('kr_data.db')
    c = conn.cursor()
    
    c.execute('''
    INSERT OR REPLACE INTO summoners (summoner_id, summoner_name)
    VALUES (?, ?)
    ''', (summoner_id, summoner_name))
    
    conn.commit()
    conn.close()
    print(f"Saved summoner info: {summoner_id} - {summoner_name}")

def save_match_info(match_id, summoner_id, champion_id, role, lane):
    conn = sqlite3.connect('kr_data.db')
    c = conn.cursor()
    
    c.execute('''
    INSERT OR REPLACE INTO matches (match_id, summoner_id, champion_id, role, lane)
    VALUES (?, ?, ?, ?, ?)
    ''', (match_id, summoner_id, champion_id, role, lane))
    
    conn.commit()
    conn.close()
    print(f"Saved match info: {match_id} - {summoner_id} - {champion_id} - {role} - {lane}")

def fetch_summoners():
    conn = sqlite3.connect('kr_data.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM summoners')
    rows = c.fetchall()
    
    for row in rows:
        print(row)
    
    conn.close()

def main():
    init_db()  # データベースとテーブルを初期化

    challengers = get_challenger_summoners(api_key, REGION)
    if challengers:
        for challenger in challengers[:5]:  # 最新の5人のチャレンジャーを対象
            summoner_id = challenger['summonerId']
            summoner_name = challenger['summonerName']
            save_summoner_info(summoner_id, summoner_name)  # サモナー情報を保存
            
            matchlist = get_matchlist_by_summoner(api_key, REGION, summoner_id)
            if matchlist:
                for match in matchlist[:3]:  # 各サモナーの最新の3試合を取得
                    match_id = match['gameId']
                    champion_id = match['champion']
                    role = match['role']
                    lane = match['lane']
                    save_match_info(match_id, summoner_id, champion_id, role, lane)  # マッチ情報を保存
                    
                    match_details = get_match_details(api_key, REGION, match_id)
                    if match_details:
                        print(f"Match ID: {match_details['gameId']}, Game Duration: {match_details['gameDuration']}, Participants: {len(match_details['participants'])}")

    fetch_summoners()  # データベースからサモナー情報を取得して表示

if __name__ == "__main__":
    main()

