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
    cursor.execute('SELECT count(date) FROM npm_packages WHERE  name = ? ', (package[1],))
    found = cursor.fetchone()
    if found[0] > 0:
        return True
    return False


def scrape_version(input_string: str) -> str:
    start = 21  # manually counted
    end = input_string.find(' -')
    return input_string[start:end].strip()


def insert_new(response: str, connection: sqlite3.Connection):
    global done
    soup = BeautifulSoup(response, 'html.parser')
    cur = connection.cursor()
    new, existing = 0, 0
    for package in soup.find_all('div', 'project'):
        name_ref = package.find('a').get('href')[5:]
        name = str(name_ref).replace("%2F", "/")
        date = package.find('time').get('datetime')
        version = scrape_version(package.find('small').getText())
        found = in_db([date, name, version], cur)
        if not found:
            cur.execute('INSERT INTO npm_packages(date,name,version) VALUES(?,?,?)', (date, name, version))
            new += 1
        if found:

            cur.execute('UPDATE npm_packages SET date = ?, version = ? WHERE name = ?', (date, version, name))
            existing += 1
    print("  ", new, "new, ", existing, "existing packages")
    if new == 0:
        done = True
    connection.commit()


apikey = open("apikey", 'r').read().strip()
done = False
con_db = sqlite3.connect('npm_packages.db')  # TABLE packages  ->  date text, name text,  version real

for i in range(1, 101):  # any page past 100 gives a 404
    if not done:
        if i % 10 == 0:  # rate limit seems to kick in after 10 pages
            print("Pausing 30 seconds to prevent rate limit.")
            time.sleep(30)
        retrieve_page(i, con_db)

con_db.close()
