#
# Scraper for Postmedia formatted News Sites
#
class Record:
  headline = ""
  date = ""
  pre_covid = 0
  news_source = ""
  bias = 0
# Record Format:
# Headline
# Date 
# Pre-Covid 0/1
# News Source
# Bias


import requests
from bs4 import BeautifulSoup
import pandas as pd
from os.path import join

def main():
  URLS = ["https://calgaryherald.com/sitemap/", "https://torontosun.com/sitemap/", "https://edmontonjournal.com/sitemap/"]

  headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
  }

  dates = []
  with open("rand-dates-mini.txt", "r") as datefile:
    x = datefile.read().splitlines()
    dates.extend(x)
  
  headlines = []
  for url in URLS:
    for date in dates:
      full_url = join(url, date+'/',)
      print(full_url)
      page = requests.get(full_url, headers=headers)

      soup = BeautifulSoup(page.content, "html.parser")
      headline_list = soup.find("ul", class_="sitemap-results-list")
      for headline in headline_list.find_all("li"):
        headlines.append(headline.get_text())

  print(headlines)
if __name__ == "__main__":
  main()