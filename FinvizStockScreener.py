import csv
import requests
from bs4 import BeautifulSoup
import itertools as it

# url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0&page="
url = "https://finviz.com/screener.ashx?v=111&o=-marketcap"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"}

filename = "FinvizMarketCapital1-200.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="")
writer = csv.writer(f)

title = "No.	Ticker	Company	Sector	Industry	Country	Market Cap	P/E	Price	Change	Volume".split(
    "\t")
# ["No.", "Ticker",	"Company",	"Sector",	"Industry", ...]

writer.writerow(title)  # Need to put the data as a type of the list

for page in range(1, 11):
    if page == 1:
        res = requests.get(url, headers=headers)
    else:
        res = requests.get(url + "&r=" + str(page*20 - 19), headers=headers)

    # res = requests.get(url + "&r=" + str(page*10), headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    # data_rows = soup.find("table", attrs={"class": "type_2"}).find(
    # "tbody").find_all("tr")
    data_rows_dark = soup.find_all("tr", attrs={"class": "table-dark-row-cp"})
    data_rows_light = soup.find_all(
        "tr", attrs={"class": "table-light-row-cp"})

    data_rows = list(it.chain(*zip(data_rows_dark, data_rows_light)))

    for row in data_rows:
        # print(row)
        columns = row.find_all("td")

        if len(columns) <= 1:  # Skip the rows with no meaingful data
            continue

        data = [column.get_text().strip() for column in columns]
        # print(data)
        writer.writerow(data)
