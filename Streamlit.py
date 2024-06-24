import streamlit as st

import pandas as pd

from sklearn.model_selection import train_test_split
import joblib

# チャンピオン名とIDの対応リストを辞書に変換
champion_dict = {
    "アニー": 1,
    "オラフ": 2,
    "ガリオ": 3,
    "ツイステッド・フェイト": 4,
    "シン・ジャオ": 5,
    "アーゴット": 6,
    "ルブラン": 7,
    "ブラッドミア": 8,
    "フィドルスティックス": 9,
    "ケイル": 10,
    "マスター・イー": 11,
    "アリスター": 12,
    "ライズ": 13,
    "サイオン": 14,
    "シヴィア": 15,
    "ソラカ": 16,
    "ティーモ": 17,
    "トリスターナ": 18,
    "ワーウィック": 19,
    "ヌヌ＆ウィルンプ": 20,
    "ミス・フォーチュン": 21,
    "アッシュ": 22,
    "トリンダメア": 23,
    "ジャックス": 24,
    "モルガナ": 25,
    "ジリアン": 26,
    "シンジド": 27,
    "イブリン": 28,
    "トゥイッチ": 29,
    "カーサス": 30,
    "チョ＝ガス": 31,
    "アムム": 32,
    "ラムス": 33,
    "アニビア": 34,
    "シャコ": 35,
    "ドクター・ムンド": 36,
    "ソナ": 37,
    "カサディン": 38,
    "イレリア": 39,
    "ジャンナ": 40,
    "ガングプランク": 41,
    "コーキ": 42,
    "カルマ": 43,
    "タリック": 44,
    "ベイガー": 45,
    "トランドル": 48,
    "スウェイン": 50,
    "ケイトリン": 51,
    "ブリッツクランク": 53,
    "マルファイト": 54,
    "カタリナ": 55,
    "ノクターン": 56,
    "マオカイ": 57,
    "レネクトン": 58,
    "ジャーヴァンⅣ": 59,
    "エリス": 60,
    "オリアナ": 61,
    "ウーコン": 62,
    "ブランド": 63,
    "リー・シン": 64,
    "ヴェイン": 67,
    "ランブル": 68,
    "カシオペア": 69,
    "スカーナー": 72,
    "ハイマーディンガー": 74,
    "ナサス": 75,
    "ニダリー": 76,
    "ウディア": 77,
    "ポッピー": 78,
    "グラガス": 79,
    "パンテオン": 80,
    "エズリアル": 81,
    "モルデカイザー": 82,
    "ヨリック": 83,
    "アカリ": 84,
    "ケネン": 85,
    "ガレン": 86,
    "レオナ": 89,
    "マルザハール": 90,
    "タロン": 91,
    "リヴェン": 92,
    "コグ＝マウ": 96,
    "シェン": 98,
    "ラックス": 99,
    "ゼラス": 101,
    "シュヴァーナ": 102,
    "アーリ": 103,
    "グレイブス": 104,
    "フィズ": 105,
    "ボリベア": 106,
    "レンガー": 107,
    "ヴァルス": 110,
    "ノーチラス": 111,
    "ビクター": 112,
    "セジュアニ": 113,
    "フィオラ": 114,
    "ジグス": 115,
    "ルル": 117,
    "ドレイヴン": 119,
    "ヘカリム": 120,
    "カ＝ジックス": 121,
    "ダリウス": 122,
    "ジェイス": 126,
    "リサンドラ": 127,
    "ダイアナ": 131,
    "クイン": 133,
    "シンドラ": 134,
    "オレリオン・ソル": 136,
    "ケイン": 141,
    "ゾーイ": 142,
    "ザイラ": 143,
    "カイ＝サ": 145,
    "ナー": 150,
    "ザック": 154,
    "ヤスオ": 157,
    "ヴェル＝コズ": 161,
    "タリア": 163,
    "カミール": 164,
    "アクシャン": 166,
    "ベル＝ヴェス": 200,
    "ブラウム": 201,
    "ジン": 202,
    "キンドレッド": 203,
    "ゼリ": 221,
    "ジンクス": 222,
    "タム・ケンチ": 223,
    "ヴィエゴ": 234,
    "セナ": 235,
    "ルシアン": 236,
    "ゼド": 238,
    "クレッド": 240,
    "エコー": 245,
    "キヤナ": 246,
    "ヴァイ": 254,
    "エイトロックス": 266,
    "ナミ": 267,
    "アジール": 268,
    "ユーミ": 350,
    "サミーラ": 360,
    "スレッシュ": 412,
    "イラオイ": 420,
    "レク＝サイ": 421,
    "アイバーン": 427,
    "カリスタ": 429,
    "バード": 432,
    "ラカン": 497,
    "ザヤ": 498,
    "オーン": 516,
    "サイラス": 517,
    "ニーコ": 518,
    "アフェリオス": 523,
    "レル": 526,
    "パイク": 555,
    "ヴェックス": 711,
    "ヨネ": 777,
    "セト": 875,
    "リリア": 876,
    "グウェン": 887,
    "レナータ・グラスク": 888,
    "ニーラ": 895,
    "ミリオ": 902,
    "カ＝サンテ": 897,
    "スモルダー": 901,
    "フェイ": 910,
    "ブライアー": 233,
    "ナフィーリ": 950
}


st.header('LOL勝利予想AI')

# チャンピオン名からIDを取得する関数
def get_champion_id(champion_name):
    return champion_dict.get(champion_name, "チャンピオンが見つかりません")

# モデルをロードする関数
def load_model(model_filename='lolperfect_AI.pkl'):
    return joblib.load(model_filename)

# 試合を予測する関数
def predict_match(loaded_model, champion_ids_100, champion_ids_200, X):
    new_match_data = {
        'champion_ids_100': champion_ids_100,
        'champion_ids_200': champion_ids_200
    }

    max_champions = 5
    for team in [100, 200]:
        key = f'champion_ids_{team}'
        for i in range(max_champions):
            new_match_data[f'champion_{team}_{i+1}'] = new_match_data[key][i]

    new_match_data.pop('champion_ids_100')
    new_match_data.pop('champion_ids_200')

    new_match_df = pd.DataFrame([new_match_data])

    # 特徴量名を学習時のものと一致させる
    new_match_df.columns = [
        'champion_100_1', 'champion_100_2', 'champion_100_3', 'champion_100_4', 'champion_100_5',
        'champion_200_1', 'champion_200_2', 'champion_200_3', 'champion_200_4', 'champion_200_5'
    ]

    # 足りない特徴量を補完
    for col in X.columns:
        if col not in new_match_df.columns:
            new_match_df[col] = 0

    new_match_df = new_match_df[X.columns]

    prediction = loaded_model.predict(new_match_df)
    win_probability = loaded_model.predict_proba(new_match_df)

    return prediction, win_probability


champion_ids_100 = []
champion_ids_200 = []

left_col, right_col = st.columns(2)

champion_names = list(champion_dict.keys())

with left_col:
    st.header("BLUEチーム")
    roles = ["TOP", "JG", "MID", "ADC", "SUP"]
    for i, role in enumerate(roles):
        champion_name = st.text_input(f"{role}", key=f"left{i}")
        champion_id = get_champion_id(champion_name)
        if champion_id != "チャンピオンが見つかりません":
            champion_ids_100.append(champion_id)

with right_col:
    st.header("REDチーム")
    roles = ["TOP", "JG", "MID", "ADC", "SUP"]
    for i, role in enumerate(roles):
        champion_name = st.text_input(f"{role}", key=f"right{i}")
        champion_id = get_champion_id(champion_name)
        if champion_id != "チャンピオンが見つかりません":
            champion_ids_200.append(champion_id)

if st.button("予測を実行"):
    model_filename = 'lolperfect_AI.pkl'
    loaded_model = load_model(model_filename)

    X = pd.DataFrame(columns=[
        'team_gold_100', 'team_gold_200', 'team_damage_100', 'team_damage_200',
        'team_vision_100', 'team_vision_200', 'team_kills_100', 'team_kills_200',
        'team_deaths_100', 'team_deaths_200', 'team_assists_100', 'team_assists_200',
                'champion_100_1', 'champion_100_2', 'champion_100_3', 'champion_100_4', 'champion_100_5',
        'champion_200_1', 'champion_200_2', 'champion_200_3', 'champion_200_4', 'champion_200_5'
    ])

    if len(champion_ids_100) == 5 and len(champion_ids_200) == 5:
        prediction, win_probability = predict_match(loaded_model, champion_ids_100, champion_ids_200, X)

        st.write(f'予測結果: {"Team BLUE Wins" if prediction[0] == 1 else "Team RED Wins"}')
        st.write(f'勝利確率: {win_probability}')
    else:
        st.write("各チームに5つのチャンピオンIDを入力してください。")