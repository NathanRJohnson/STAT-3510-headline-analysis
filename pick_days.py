## Want to generate n number of days for both precovid and during covid
## Save dates to a csv in current format
#THEN
# Load into other file and scrape
import random
import datetime

def random_date(year):
    start_date = datetime.date(year, 1, 1)
    end_date = datetime.date(year, 11, 30) if year == 2019 else datetime.date(year, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + datetime.timedelta(days=random_days)

def main():
  # years_days = {2018: 15, 2019:35, 2020: 35, 2021:15}
  years_days = {2018: 3, 2019: 5, 2020: 5, 2021: 3}  # mini
  dates = []
  for year, days in years_days.items():
        for _ in range(days):
          random_day = random_date(year)
          dates.append(random_day.strftime("%Y-%m-%d"))
  
  with open("rand-dates-mini.txt", 'w') as file:
    for date in dates:
      file.write(date+"\n")

if __name__ == "__main__":
    main()