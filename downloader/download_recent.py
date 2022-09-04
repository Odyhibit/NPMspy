#  Josh Bloom
# using Command line version of OSS-Gadget and yara.


import sqlite3
import subprocess


def in_green(input: str) -> str:
    return "\033[32;1m" + str(input) + "\033[0m"


def in_red(input: str) -> str:
    return "\033[31m" + str(input) + "\033[0m"


def remove_scope(name: str) -> str:
    if "/" in name:
        name = name[name.find("/") + 1:]
    return name


def get_directory(response: str) -> str:
    directory = "suspicious"
    if 'directory="' in response:
        start = response.find('directory="') + 11
        end = response.find('"', start + 1)
        directory = response[start:end]
    return directory


def download_package(name: str) -> ():
    directory = ""
    package_name = "pkg:npm/" + remove_scope(name)
    package_dir = "package_downloads\\" + name
    # print("oss-download", "-e", "-c", "-x", package_dir, package_name)
    oss_download = subprocess.run(["oss-download", "-e", "-c", "-x", package_dir, package_name], capture_output=True,
                                  encoding="UTF-8")
    index = oss_download.stderr.find(" to ") + 4
    if index > 4:
        directory = oss_download.stderr[index:].strip()

    return directory


def yara_rule(directory: str) -> str:
    #  yara64 -r -m ./yara_rules/rules.yara ./package_downloads/<package_folder>
    # print()
    # print("yara64", "-r", "-m", "yara_rules/rules.yara", directory)
    yara_response = subprocess.run(["yara64", "-r", "-m", "./yara_rules/rules.yara", directory], capture_output=True,
                                   encoding="UTF-8")
    return yara_response.stdout


#  connect to DB
conn_npm = sqlite3.connect("../webscraper/npm_packages.db")
cur_npm = conn_npm.cursor()
#  get most recent packages (date,name,version)
# SELECT packages.name FROM packages LEFT JOIN results ON results.name = packages.name WHERE results.name IS NULL
ten_most_recent = cur_npm.execute("SELECT date,name,version from npm_packages ORDER BY date DESC LIMIT 1000").fetchall()

#  download them with npm
for package in ten_most_recent:  # package date,name,version
    download_dir = download_package(package[1])
    if len(download_dir) > 4:
        yara_matches = yara_rule(download_dir)
        gutter = " " * (75 - len(download_dir))
        if yara_matches == "":
            print(download_dir, gutter, in_green("no matches"))
        else:

            print(download_dir, gutter, in_red(yara_matches))
    else:
        gutter = " " * (75 - len(package[1]))
        print(package[1], gutter, in_red("not downloaded"))