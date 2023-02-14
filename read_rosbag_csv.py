import pandas as pd

df = pd.read_csv('data/rosbags/ctd.csv', index_col=0)

df.set_index(pd.to_datetime((df.index * 10**9).astype(int)), inplace=True)

print(df.head())