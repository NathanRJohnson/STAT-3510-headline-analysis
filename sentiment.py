# import tweetnlp
from flair.data import Sentence
from flair.nn import Classifier
import pandas as pd

from os.path import join
from os import listdir

POSITIVE = 1
NEUTRAL = 0
NEGATIVE = -1

def main():
  # model = tweetnlp.load_model('sentiment')
  tagger = Classifier.load('sentiment')
  
  RESULT_DIR = 'sentimental_flair/'
  DATA_DIR = 'scraped/'
  CSVS = listdir(DATA_DIR)

  for csv in CSVS:
    print(csv)
    dataframe = pd.read_csv(join(DATA_DIR, csv))
    headlines = dataframe.loc[:, "Headline"]

    scores = []
    for headline in headlines:
      # sentiment = model.sentiment(headline)
      # scores.append(sentimentToInt(sentiment)
      sentence = Sentence(headline)
      tagger.predict(sentence)
      scores.append(sentence_to_sentiment(sentence))
    dataframe["Sentiment"] = scores

    # print(dataframe.loc[:, dataframe.columns.isin(["Headline", "Sentiment"])])
    dataframe.to_csv(join(RESULT_DIR, csv), index=False)

def old_sentimentToInt(sentiment):
  if sentiment['label'] == 'positive':
    return POSITIVE
  elif sentiment['label'] == 'negative':
    return NEGATIVE
  else:
    return NEUTRAL
  
def sentence_to_sentiment(sentence):
  # print(sentence.get_labels())
  for label in sentence.get_labels():
    score = label.score
    # print(score)
    if score < 0.75:
      return NEUTRAL
    elif "POSITIVE" in label.value:
      return POSITIVE
  return NEGATIVE

def getFloat(s):
  l = []
  for t in s.split():
    try:
      l.append(float(t))
    except ValueError:
      pass
  return l
  
  

if __name__ == '__main__':
  main()

