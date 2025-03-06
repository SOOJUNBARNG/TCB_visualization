import pandas as pd
import requests

df = pd.read_csv("real_basic_data.csv")
df_unique = df["address"].drop_duplicates().reset_index(drop=True)


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


lat_list = []
long_list = []
for clinic_address in df_unique:
    lat, long = get_lat_long_from_address(clinic_address)
    lat_list.append(lat)
    long_list.append(long)

# Combine the results into a DataFrame
total_list = pd.DataFrame(
    {
        "Name": df["name"],
        "Address": df_unique,
        "Latitude": lat_list,
        "Longitude": long_list,
    }
)

# Save the results to a new CSV file
total_list.to_csv("final.csv", index=False)
