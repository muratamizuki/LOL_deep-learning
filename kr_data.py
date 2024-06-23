import sqlite3

def init_kr_db():
    # 'kr_data.db' という名前のデータベースを作成または接続
    conn = sqlite3.connect('kr_data.db')
    c = conn.cursor()

    # summoners テーブルを作成
    c.execute('''
    CREATE TABLE IF NOT EXISTS summoners (
        id TEXT PRIMARY KEY,
        account_id TEXT,
        puuid TEXT,
        name TEXT,
        profile_icon_id INTEGER,
        revision_date INTEGER,
        summoner_level INTEGER
    )
    ''')

    # matches テーブルを作成
    c.execute('''
    CREATE TABLE IF NOT EXISTS matches (
        match_id TEXT PRIMARY KEY,
        summoner_id TEXT,
        champion_id INTEGER,
        role TEXT,
        lane TEXT,
        FOREIGN KEY(summoner_id) REFERENCES summoners(id)
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_kr_db()