import pandas as pd
import numpy as np

LEFT = 0
RIGHT = 1

def main():
  all_headlines_df = pd.read_csv("combined_headlines.csv")
  aggregated_df = pd.read_csv("aggregated/aggregated_full.csv")

  undersampled_df = pd.DataFrame()

  for i in range(100):
    left_headlines_on_day_i = all_headlines_df.loc[(all_headlines_df['Date_id'] == i) & (all_headlines_df['Bias'] == LEFT)]
    left_headlines_to_remove = max(len(left_headlines_on_day_i) - 15, 0)
    random_indicies = np.random.choice(left_headlines_on_day_i.index, left_headlines_to_remove, replace=False)
    reduced_left_headlines = left_headlines_on_day_i.drop(random_indicies).reset_index(drop=True)

    right_headlines_on_day_i = all_headlines_df.loc[(all_headlines_df['Date_id'] == i) & (all_headlines_df['Bias'] == RIGHT)]
    right_headlines_to_remove = max(len(right_headlines_on_day_i) - 15, 0)
    random_indicies = np.random.choice(right_headlines_on_day_i.index, right_headlines_to_remove, replace=False)
    reduced_right_headlines = right_headlines_on_day_i.drop(random_indicies).reset_index(drop=True)

    undersampled_df = pd.concat([undersampled_df, reduced_left_headlines, reduced_right_headlines], axis=0)
    # undersampled_df.reset_index()

  undersampled_df.drop('index', axis=1, inplace=True)
  pd.DataFrame.to_csv(undersampled_df, "undersampled_data.csv", index=False)


if __name__ == '__main__':
  main()