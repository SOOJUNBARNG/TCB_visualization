import pandas as pd

# CSVを読み込む
df = pd.read_csv("")  # CSVファイルを読み込み、DataFrameとして保存

# データフレームの構造を確認する
df.info()  # データの概要（データ型、行数、列数、nullの有無）を表示する
df.describe()  # 数値データの基本統計量（平均、標準偏差、最小値、四分位数など）を表示

# 欠損値の確認
df.isnull().sum()  # 各列に含まれるnull（欠損値）の数を合計で表示する

# 特定の列に含まれるユニークな値の数を確認
df["column_name"].nunique()  # 指定した列のユニークな値の個数を取得
df["column_name"].unique()  # 指定した列のユニークな値を配列として取得

# データフレーム内の重複行を確認
df.duplicated().sum()  # 重複している行の数を取得
df[df.duplicated()]  # 重複している行自体を抽出して表示

# 数値データの相関関係を確認
df.corr()  # 数値列同士の相関係数を計算し、相関行列として表示

# 数値データの分布をヒストグラムで可視化
df.hist(
    figsize=(10, 8)
)  # 各数値列に対してヒストグラムをプロットする（図のサイズを指定）

# メモリ使用量を確認
df.memory_usage(
    deep=True
)  # 各列のメモリ使用量を表示し、deep=Trueでより正確な使用量を計算
