import pandas as pd

unsplit = pd.read_csv("aggregated/aggregated_full.csv")

# split = pd.DataFrame(columns=['date_id', 'date', 'pre_covid', 'n_count', 't_count', 'd_count', 'is_r'])
# for i in range(100):
#   row = unsplit.iloc[i]
#   row_l = { 
#             'date_id': i,
#             'date': row['date'],
#             'pre_covid': row['pre_covid'],       
#             'n_count': row['negative_l'],
#             't_count': row['total_l'],
#             'd_count': row['total'],
#             'is_r': 0
#           }
#   row_r = { 
#             'date_id': i,
#             'date': row['date'],
#             'pre_covid': row['pre_covid'],       
#             'n_count': row['negative_r'],
#             't_count': row['total_r'],
#             'd_count': row['total'],
#             'is_r': 1
#           }
  
#   split.loc[2*i] = row_l
#   split.loc[2*i+1] = row_r

# split.reset_index().drop('index', axis=1, inplace=True)
# split.to_csv("split_bias_full.csv", index=False)
# print(split.head())

split = pd.DataFrame(columns=['date_id', 'date', 'pre_covid', 'n_count', 't_count', 'd_count', 'is_high'])
for i in range(100):
  row = unsplit.iloc[i]
  row_high = { 
            'date_id': i,
            'date': row['date'],
            'pre_covid': row['pre_covid'],       
            'n_count': row['negative_high'],
            't_count': row['total_high'],
            'd_count': row['total'],
            'is_high': 1
          }
  row_low = { 
            'date_id': i,
            'date': row['date'],
            'pre_covid': row['pre_covid'],       
            'n_count': row['negative_low'],
            't_count': row['total_low'],
            'd_count': row['total'],
            'is_high': 0
          }
  
  split.loc[2*i] = row_high
  split.loc[2*i+1] = row_low

split.reset_index().drop('index', axis=1, inplace=True)
split.to_csv("split_cred_full.csv", index=False)
print(split.head())