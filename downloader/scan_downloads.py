#  Josh Bloom
# using Command line version of OSS-Gadget and yara.


import sqlite3
import subprocess


def in_green(input: str) -> str:
    return "\033[32;1m" + str(input) + "\033[0m"


def in_red(input: str) -> str:
    return "\033[31m" + str(input) + "\033[0m"


def scope_url(name: str) -> str:
    return name.replace("@", "%40").replace("/", "%2f")


def get_directory(response: str) -> str:
    directory = "suspicious"
    if 'start_from="' in response:
        start = response.find('start_from="') + 11
        end = response.find('"', start + 1)
        directory = response[start:end]
    return directory


def rule_id(rule_name: str, connection: sqlite3.connect) -> int:
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM yara_matches WHERE  rule_name = ? ', (rule_name,))
    found = cursor.fetchone()
    print(type(found))
    if found is not None:
        return int(found[0])
    cursor.execute('INSERT INTO yara_matches(rule_name) VALUES(?)', (rule_name,))
    return cursor.lastrowid


def download_package(name: str) -> ():
    directory = ""
    package_name = "pkg:npm/" + scope_url(name)
    package_dir = "package_downloads\\" + name
    # oss-download -e -c -x <package_dir> <package_name>
    oss_download = subprocess.run(["oss-download", "-e", "-c", "-x", package_dir, package_name], capture_output=True,
                                  encoding="UTF-8")
    index = oss_download.stderr.find(" to ") + 4
    if index > 4:
        directory = oss_download.stderr[index:].strip()[18:]

    return directory


def yara_rule(directory: str) -> str:
    #  yara64 -r ./yara_rules/rules.yara ./package_downloads/<package_folder>
    # print("yara64", "-r", "yara_rules/rules.yara", start_from)
    yara_response = subprocess.run(["yara64", "-r", "./yara_rules/rules.yara", directory], capture_output=True,
                                   encoding="UTF-8")
    return yara_response.stdout


def add_result(cursor: sqlite3.Connection.cursor, package_id: int, yara_id: int):
    cursor.execute("INSERT INTO results (package_id,match_id) values (?,?)", (package_id, yara_id))


if __name__ == "__main__":
    #   hard coded yara results
    not_downloaded = 1
    no_matches = 2

    conn_npm = sqlite3.connect("../webscraper/npm_packages.db")
    cur_npm = conn_npm.cursor()
    most_recent = cur_npm.execute("SELECT date,name,version,npm_packages.id from npm_packages "
                                  "LEFT JOIN results ON results.package_id = npm_packages.id "
                                  "WHERE results.id IS NULL ORDER BY date DESC LIMIT 1000").fetchall()

    for package in most_recent:
        name = package[1]
        package_id = package[3]
        download_dir = download_package(name)

        if len(download_dir) > 4:  # download worked
            yara_matches = yara_rule(download_dir)
            gutter = " " * (75 - len(download_dir))
            if yara_matches == "":
                add_result(cur_npm, package_id, no_matches)
                print(download_dir, gutter, in_green("no matches"))
            else:
                yara_match_id = rule_id(yara_matches.split()[0], conn_npm)
                add_result(cur_npm, package_id, yara_match_id)
                print(download_dir, gutter, in_red(yara_matches))
        else:  # download did not work
            add_result(cur_npm, package_id, not_downloaded)
            gutter = " " * (75 - len(name))
            print(package[1], gutter, in_red("not downloaded"))

        conn_npm.commit()
