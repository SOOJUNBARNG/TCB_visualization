import requests
import pandas as pd
import math
import time
import numpy as np

df = pd.read_csv("staff_address_clinic.csv")
staff_list = df["MFコード"]
staff_address = df["スタッフ住所"]
clinic_address = df["クリニック住所"]


def get_lat_long_from_address(address):
    # 国土地理院のAPIエンドポイント
    endpoint = "https://msearch.gsi.go.jp/address-search/AddressSearch"

    # APIリクエストを送信
    response = requests.get(endpoint, params={"q": address})

    # レスポンスのJSONデータを解析
    data = response.json()

    if len(data) > 0:
        # 最初の候補の緯度経度を取得
        lat = data[0]["geometry"]["coordinates"][1]
        lon = data[0]["geometry"]["coordinates"][0]
        return lat, lon
    else:
        return None, None


staff_list = df["MFコード"]
staff_address = df["スタッフ住所"]
clinic_address = df["クリニック住所"]

# データフレームに変換
df = pd.DataFrame(
    {
        "MFコード": staff_list,
        "スタッフ住所": staff_address,
        "クリニック住所": clinic_address,
        "距離": distance_list,
    }
)

# CSVファイルに保存
csv_file_name = "output.csv"
df.to_csv(csv_file_name, index=False)
