#  Josh Bloom
# using Command line version of npm and yara.


import sqlite3
import subprocess

import requests
import yara
import gzip


def get_filename(name: str, version: str) -> str:
    if "/" in name:
        name = name[name.find("/") + 1:]   # remove scope
    return name.strip() + "-" + version.strip() + ".tgz"


def get_download_url(name: str, version: str) -> str:
    return "https://registry.npmjs.org/" + name + "/-/" + get_filename(name, version)


def extract_gzip(zip_file):
    zip_file = gzip.open(zip_file)
    return {name: zip_file.read(name) for name in zip_file.namelist()}

conn_npm = sqlite3.connect("../webscraper/npm_packages.db")  # TABLE packages  ->  date text, name text,  version real
cur_npm = conn_npm.cursor()
ten_most_recent = cur_npm.execute("SELECT * from packages ORDER BY date DESC LIMIT 10").fetchall()
for package in ten_most_recent:  # package date,name,version
    package_url = get_download_url(package[1].replace("%2F", "/"), package[2])
    file_response = requests.get(package_url)
    print(package_url)
    print(file_response.apparent_encoding)
    print("about to nmp pack", package[1])
    test_download = subprocess.run(["npm", "pack", str(package[1])])
