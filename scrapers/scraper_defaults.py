import pandas as pd

# Bias
LEFT = 0
RIGHT = 1

# Cred
HIGH = 0
MOSTLY = 1
MIXED = 2

class Newspaper:
  def __init__(self, name, bias, cred, scraper) -> None:
    self.name = name
    self.bias = bias
    self.cred = cred   
    self.scraper = scraper

def scrape(newspaper):
  data = []
  dates = getDates() # update for full later

  for i, date in enumerate(dates):
    y, m, d = format_date(date)
    covid_status = getCovidStatus(y, m)
    headlines = newspaper.scraper(y, m, d)
    for headline in headlines:
      data.append({
        'Headline': headline,
        'Source': newspaper.name,
        'Year': y,
        'Month': m,
        'Day': d, 
        'Date_id': i,
        'Pre-Covid': covid_status,
        'Bias': newspaper.bias,
        'Cred': newspaper.cred
      })

  pd.DataFrame(data).to_csv(f"scraped/{newspaper.name.replace(' ', '_')}.csv", index=False)

def format_date(date):
  tokens = date.split('-')
  return tokens[0], tokens[1], tokens[2]

def getCovidStatus(year, month):
  year = int(year)
  month = int(month)
  return 0 if year < 2019 or year == 2019 and month <= 11 else 1

def getDates():
  dates = []
  with open("rand-dates-mini.txt", "r") as datefile:
    x = datefile.read().splitlines()
    dates.extend(x)
  return dates
  
def getDate():
  return ["2019-11-12"]

