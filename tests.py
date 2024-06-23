import configparser
from kr_data import init_kr_db
from test import get_challenger_summoners, get_matchlist_by_summoner, get_match_details

config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')
api_key = config_ini['DEFAULT']['key']

REGION = 'kr'
def main():
    init_kr_db()  # データベースとテーブルを初期化

    challengers = get_challenger_summoners(api_key, REGION)
    if challengers:
        for challenger in challengers[:200]:  # 最新の5人のチャレンジャーを対象
            summoner_id = challenger['summonerId']
            matchlist = get_matchlist_by_summoner(api_key, REGION, summoner_id)
            if matchlist:
                for match in matchlist[:3]:  # 各サモナーの最新の3試合を取得
                    match_id = match['gameId']
                    match_details = get_match_details(api_key, REGION, match_id)
                    if match_details:
                        print(f"Match ID: {match_details['gameId']}, Game Duration: {match_details['gameDuration']}, Participants: {len(match_details['participants'])}")

if __name__ == "__main__":
    main()
