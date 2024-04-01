import requests
from bs4 import BeautifulSoup
import scraper_defaults as sd

def main():
  WashingtonTimes = sd.Newspaper("The Washington Times", bias=sd.RIGHT, cred=sd.MIXED, scraper=scrape_headlines)
  sd.scrape(WashingtonTimes)

def scrape_headlines(year, month, day):
  
  BASE_URL = f"https://washingtontimes.newsbank.com/search?date_from={month}/{day}/{year}&date_to={month}/{day}/{year}&pub%5B0%5D=WSTB" #&page=4
  url = BASE_URL

  headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
  }
  
  all_headlines = []
  incr = 1
  while True:
    page = requests.get(url, headers=headers)
    if page.status_code != 200:
      break

    soup = BeautifulSoup(page.content, "html.parser")
    sections = soup.find_all("div", class_="views-field views-field-text-1")
    if not sections:
      break

    for section in sections:
      all_headlines.extend([headline.text.strip() for headline in section.find_all('a')])

    url = BASE_URL + f'&page={incr}'
    incr += 1

  return all_headlines

  
if __name__ == '__main__':
  main()