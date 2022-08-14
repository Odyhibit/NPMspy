#  Josh Bloom
# note: libraries.io api has rate limit of 60 requests / minute, so add a pause if more than 60 pages.

import requests
from bs4 import BeautifulSoup
import sqlite3

apikey = open("apikey", 'r').read().strip()
most_recent = "2022-08-13T15:51:12+00:00"
done = False
con = sqlite3.connect('npm_packages.db')  # TABLE packages  ->  date text, name text,  version real


def retrieve_page(page):
    request_parameters = {
        'page': page,
        'per_page': "100",
        'order': 'desc',
        'platforms': 'NPM',
        'sort': 'created_at',
        'api_key': apikey}
    resp = requests.get("https://libraries.io/search", params=request_parameters)
    if not done:
        print("URL is ", resp.url)
        insert_new(resp.text)


def in_db(package: [], cursor: con.cursor()) -> bool:
    global done
    cursor.execute('SELECT count(date) FROM packages WHERE date = ? AND name = ? AND version = ?', package)
    found = cursor.fetchone()
    if found[0] > 0:
        done = True
        # print("found ", package, "so we are done.")
        return True
    return False


def insert_new(response):
    soup = BeautifulSoup(response, 'html.parser')
    cur = con.cursor()
    for package in soup.find_all('div', 'project'):
        name = package.find('a').get('href')
        date = package.find('time').get('datetime')
        version_text = package.find('small').getText()
        version_start = 21  # manually counted
        version_end = version_text.find('-')
        version = version_text[version_start:version_end]
        if not in_db([date, name, version], cur):
            #  print("Inserting ", name)
            cur.execute('INSERT INTO packages VALUES(?,?,?)', (date, name, version))
    con.commit()


for i in range(1, 10):
    if not done:
        retrieve_page(i)
con.close()
