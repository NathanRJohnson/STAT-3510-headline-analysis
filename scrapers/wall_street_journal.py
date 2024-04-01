import requests
import scraper_defaults as sd
import pandas
from bs4 import BeautifulSoup

def main():
  WallStreetJournal = sd.Newspaper("The Wall Street Journal", bias=sd.RIGHT, cred=sd.MOSTLY, scraper=scrape_headlines)
  sd.scrape(WallStreetJournal)

def scrape_headlines(year, month, day):
  URL = "https://www.wsj.com/news/archive/{}/{}/{}".format(year, month, day)

  headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
  }

  all_headlines = set()
  page = requests.get(URL, headers=headers)
  if page.status_code != 200:
      print(f"ERROR {page.status_code}")

  else:
     soup = BeautifulSoup(page.content, "html.parser")
     headlines = soup.find_all("article")
     for headline in headlines:
      # if headline.find('span').text.strip() in ['U.S.', 'Asia', 'China', 'Africa', 'Europe', 'East Is East', 'Middle East', 'Latin America', 'World', 'Politics']: 
      all_headlines.add(headline.find("h2").text.strip())
  
  return all_headlines 


if __name__ == '__main__':
  main()