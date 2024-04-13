import pandas as pd

LOW = 0
HIGH = 1

def main():
  all_headlines = pd.read_csv('combined_headlines.csv')

  # all_headlines.loc[all_headlines['Source'] == 'The Washington Times', 'Cred'] = LOW
  # print(all_headlines.loc[all_headlines['Source'] == 'The Washington Times'].head())
  # all_headlines.loc[all_headlines['Source'] != 'The Washington Times', 'Cred'] = HIGH
  # print(all_headlines.loc[all_headlines['Source'] == 'The Washington Times'].head())
  # all_headlines.to_csv('combined_headlines.csv', index=False)
  cred_col = all_headlines['Cred']
  print(cred_col.value_counts())

if __name__ == '__main__':
  main()