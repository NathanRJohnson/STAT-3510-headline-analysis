import requests
import scraper_defaults as sd
from bs4 import BeautifulSoup

def main():
  NewYorkTimes = sd.Newspaper("The New York Times", bias=sd.LEFT, cred=sd.HIGH, scraper=scrape_headlines)
  sd.scrape(NewYorkTimes)

def scrape_headlines(year, month, day):
  URL = f"https://www.nytimes.com/issue/todaysheadlines/{year}/{month}/{day}/todays-headlines"
  headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
  }

  all_headlines = []
  page = requests.get(URL, headers=headers)
  soup = BeautifulSoup(page.content, "html.parser")
  sections = soup.find_all("section", class_="css-12etkvn e4k4cot0")
  for section in sections:
    # if section.find('a')['name'] in ['topnews', 'world', 'u.s.', 'politics']:
    all_headlines.extend([headline.text.strip() for headline in section.findAll('h2', class_="css-ds6ff4 e1b0gigc0")])
  
  return all_headlines

if __name__ == '__main__':
  main()