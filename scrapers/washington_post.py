import requests
from bs4 import BeautifulSoup
import scraper_defaults as sd
  
def main():
  WashingtonPost = sd.Newspaper("The Washington Post", bias=sd.LEFT, cred=sd.MOSTLY, scraper=scrape_headlines)
  sd.scrape(WashingtonPost)

def scrape_headlines(year, month, day):
  MAX_TRIES = 15
  # https://www.washingtonpost.com/pb/api/v2/render/feature/section/story-list?addtl_config=blog-front-archive&content_origin=content-api-query&size=10&from=10&archive_year=2019&archive_month=11&archive_stop=30&primary_node=/opinions/posteverything
  # URL = "https://www.washingtonpost.com/news/posteverything/archive/2019/09/"
  # URL = "https://www.washingtonpost.com/news/posteverything/wp/2019/09/"
  URL = "https://www.washingtonpost.com/pb/api/v2/render/feature/section/story-list"
  headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
  }
  params = {
    "addtl_config": "blog-front-archive",
    "content_origin": "content-api-query",
    "size": 10,
    "from": 0,
    "archive_year": year,
    "archive_month": str(month),
    "archive_stop": 30,
    "primary_node": "/opinions/posteverything"
}

  session = requests.Session()
  all_headlines = []
  tries = 0
  while True:
    page = session.get(URL, headers=headers, params=params)
    if page.status_code != 200:
      print(f"ERROR {page.status_code}")
      break
    
    soup = BeautifulSoup(page.json()["rendering"], "html.parser")
    blocks = soup.find_all("h2")
    headlines = []
    for block in blocks:
      date = block.find('a')['href']
      if f"{year}/{month}/{day}" in date:
        headlines.append(block.text.strip())
    
    params["from"] += 10
    
    if headlines:
      all_headlines.extend(headlines)
    else:
      tries += 1
      if tries > MAX_TRIES: break 
  
  print(all_headlines)
  return all_headlines

if __name__ == '__main__':
  main()
  # scrape_headlines(2019, 10, 11)