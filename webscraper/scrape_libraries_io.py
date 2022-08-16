#  Josh Bloom
# note: libraries.io api has rate limit(429) time.sleep added to avoid that

import time
import requests
from bs4 import BeautifulSoup
import sqlite3


def retrieve_page(page, connection):
    global apikey
    request_parameters = {
        'api_key': apikey,
        'page': page,
        'per_page': "100",
        'order': 'desc',
        'platforms': 'NPM',
        'sort': 'created_at'}
    resp = requests.get("https://libraries.io/search", params=request_parameters)

    if resp.status_code == 200:
        print("Page", page, "URL is", resp.url, end="")
        insert_new(resp.text, connection)

    if resp.status_code != 200:
        print(f"Error retrieving page - status code is {resp.status_code}")
        time.sleep(10)
        retrieve_page(page, connection)


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
    cur = connection.cursor()
    new, updated = 0, 0
    for package in soup.find_all('div', 'project'):
        name = package.find('a').get('href')[5:]
        date = package.find('time').get('datetime')
        version_text = package.find('small').getText()
        version_start = 21  # manually counted
        version_end = version_text.find('-')
        version = version_text[version_start:version_end]
        found = in_db([date, name, version], cur)
        if not found:
            cur.execute('INSERT INTO packages VALUES(?,?,?)', (date, name, version))
            new += 1
        if found:
            cur.execute('UPDATE packages SET date = ?, version = ? WHERE name = ?', (date, version, name))
            updated += 1
    print("  * ", new, "new, ", updated, "updated packages")
    if new == 0:
        done = True
    connection.commit()


apikey = open("apikey", 'r').read().strip()
done = False
con_db = sqlite3.connect('npm_packages.db')  # TABLE packages  ->  date text, name text,  version real

for i in range(1, 101):  # any page past 100 gives a 404
    if not done:
        if i % 9 == 0:  # rate limit seems to kick in after 10 pages
            time.sleep(20)
        retrieve_page(i, con_db)

con_db.close()
