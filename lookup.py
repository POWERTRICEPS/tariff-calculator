import pandas as pd


df = pd.read_csv("app/data/hts_data.csv")
print(df.head(20))
print(df.columns)