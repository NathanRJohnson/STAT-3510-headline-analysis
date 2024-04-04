import pandas as pd

def main():

  dates = []
  with open("rand-dates.txt", "r") as datefile:
    x = datefile.read().splitlines()
    dates.extend(x)
  
  dates.sort()
  print(dates)

  with open("rand-dates.txt", "w") as datefile:
    for date in dates:
      datefile.write(date+"\n")

  
if __name__ == '__main__':
  main()