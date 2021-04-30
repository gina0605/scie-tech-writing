import requests
import urllib3
from bs4 import BeautifulSoup
import datetime
import time
import os


urllib3.disable_warnings()


def crawl(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'
    }
    page = requests.get(url, headers=headers, timeout=60, verify=False)
    time.sleep(1)
    content = page.content
    content = content.decode("utf-8")
    return content


def write_to_file(filename, txt, mode='a'):
    with open(filename, mode) as file:
        file.write(txt)


def crawl_solvedac_to_csv(level, csv_filename):
    print(f"crawling level {level}")
    page = 1
    while True:
        content = crawl(f"https://solved.ac/problems/level/{level}?page={page}")
        soup = BeautifulSoup(content, features="html.parser")
        table_selector = "#__next > div.contents > div:nth-child(4) > div > div > div.StickyTable__Wrapper-akg1ak-3.tcQcH.sticky-table > div"
        table = soup.select_one(table_selector)
        if table is None:
            return
        rows = table.find_all('div', recursive=False)
        txt = ""
        for row in rows:
            cells = row.find_all('div', recursive=False)
            id = cells[0].text
            solved_cnt = cells[2].text.replace(",", "")
            avg_tries = cells[3].text
            if id != "#":
                txt += id + "," + solved_cnt + "," + avg_tries + "\n"
        write_to_file(csv_filename, txt)
        page += 1


if __name__ == "__main__":
    now = datetime.datetime.now()
    dirname = "./result/" + now.strftime("%y%m%d-%H%M%S")
    print(f"Write to {dirname}")
    os.mkdir(dirname)
    for level in range(1, 31):
        filename = f"{dirname}/{level}.csv"
        crawl_solvedac_to_csv(level, filename)
