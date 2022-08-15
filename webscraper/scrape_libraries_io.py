#  Josh Bloom
# note: libraries.io api has rate limit time.sleep added to avoid that

import time
import requests
from bs4 import BeautifulSoup
import sqlite3


def retrieve_page(page, connection):
    request_parameters = {
        'api_key': apikey,
        'page': page,
        'per_page': "100",
        'order': 'desc',
        'platforms': 'NPM',
        'sort': 'created_at',
        }
    resp = requests.get("https://libraries.io/search", params=request_parameters)
    if not done:
        if resp.status_code != 200:
            print(f"Status code is {resp.status_code}")
            time.sleep(10)
            retrieve_page(page, connection)
        else:
            print("Page", page, "URL is", resp.url, end="")
            insert_new(resp.text, connection)


def in_db(package: [], cursor: sqlite3.connect) -> bool:
    global done
    cursor.execute('SELECT count(date) FROM packages WHERE date = ? AND name = ? AND version = ?', package)
    found = cursor.fetchone()
    if found[0] > 0:
        return True
    return False


def insert_new(response, connection):
    global done
    soup = BeautifulSoup(response, 'html.parser')
    con = connection
    cur = con.cursor()
    count = 0
    for package in soup.find_all('div', 'project'):
        name = package.find('a').get('href')
        date = package.find('time').get('datetime')
        version_text = package.find('small').getText()
        version_start = 21  # manually counted
        version_end = version_text.find('-')
        version = version_text[version_start:version_end]
        if not in_db([date, name, version], cur):
            cur.execute('INSERT INTO packages VALUES(?,?,?)', (date, name, version))
            count += 1
    print("  * ", count, "new packages")
    if count is 0:
        done = True
    con.commit()


apikey = open("apikey", 'r').read().strip()
most_recent = "2022-08-13T15:51:12+00:00"
done = False
con_db = sqlite3.connect('npm_packages.db')  # TABLE packages  ->  date text, name text,  version real

for i in range(1, 101):  # any page past 100 gives a 404
    if not done:
        if i % 9 == 0:   # rate limit seems to kick in after 10 pages
            time.sleep(20)
        retrieve_page(i, con_db)

con_db.close()
