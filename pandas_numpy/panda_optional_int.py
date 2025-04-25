import pandas as pd

d = [
    [1,1,1],
    [2,None,2],
    [3,3,3]
]

df = pd.DataFrame(d, columns=['A','B','C'])

print(df.head())

print()
#df['B'] = df['B'].astype('Int64')
df['B'].fillna(pd.NA, inplace=True)

print(df.head())
