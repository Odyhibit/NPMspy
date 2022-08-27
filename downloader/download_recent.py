#  Josh Bloom
# using Command line version of npm and yara.


import sqlite3
import subprocess


def remove_scope(name: str) -> str:
    if "/" in name:
        name = name[name.find("/") + 1:]
    return name


#  connect to DB
conn_npm = sqlite3.connect("../webscraper/npm_packages.db")
cur_npm = conn_npm.cursor()

#  get ten most recent packages (date,name,version)
ten_most_recent = cur_npm.execute("SELECT * from packages ORDER BY date DESC LIMIT 10").fetchall()

#  download them with npm
for package in ten_most_recent:  # package date,name,version
    package_name = "pkg:npm/" + remove_scope(package[1])
    package_dir = "package_downloads/" + remove_scope(package[1])
    oss_download = subprocess.run(["oss-download", "-e", "-c", "-x", package_dir, package_name], capture_output=True)
    yara_response = subprocess.run(["yara64", "-r", "-m", "./yara_rules/rules.yara", package_dir], capture_output=True, text=True)
    if yara_response.stdout != "":
        # process moving the directory to proper folder.
        print(yara_response.stdout)
    #  print("**** ", package_dir, yara_response.stdout)
