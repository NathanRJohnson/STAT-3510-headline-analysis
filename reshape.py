import pandas as pd

unsplit = pd.read_csv("aggregated/aggregated_undersampled.csv")

split = pd.DataFrame(columns=['date_id', 'date', 'pre_covid', 'count', 'is_r'])
for i in range(100):
  row = unsplit.iloc[i]
  row_r = { 
            'date_id': i,
            'date': row['date'],
            'pre_covid': row['pre_covid'],       
            'count': row['negative_r'],
            'is_r': 1
          }
  row_l = { 
            'date_id': i,
            'date': row['date'],
            'pre_covid': row['pre_covid'],       
            'count': row['negative_l'],
            'is_r': 0
          }
  
  split.loc[2*i] = row_l
  split.loc[2*i+1] = row_r

split.reset_index().drop('index', axis=1, inplace=True)
split.to_csv("split_aggregated.csv", index=False)
print(split.head())