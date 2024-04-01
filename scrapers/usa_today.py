import requests
from bs4 import BeautifulSoup
import datetime
import scraper_defaults as sd

def main():
  USAToday = sd.Newspaper("USA Today", bias=sd.LEFT, cred=sd.MOSTLY, scraper=scrape_headline)
  sd.scrape(USAToday)

def scrape_headline(year, month, day):
  month_name = datetime.datetime(int(year), int(month), int(day)).strftime("%B").lower()
  URL = f"https://www.usatoday.com/sitemap/{year}/{month_name}/{day}/"
  
  headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
  }

  all_headlines = []
  page = requests.get(URL, headers=headers)
  soup = BeautifulSoup(page.content, "html.parser")
  headline_col = soup.find("div", class_="sitemap-column-wrapper")
  headline_list = headline_col.find("ul", class_="sitemap-list")
  headlines = headline_list.find_all("li", class_="sitemap-list-item")
  all_headlines.extend([headline.text.strip() for headline in headlines])

  return all_headlines

if __name__ == '__main__':
  main()