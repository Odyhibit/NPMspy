#  Josh Bloom
import os
import sys

import requests
from bs4 import BeautifulSoup


def get_previous_version(selections: BeautifulSoup.find_all) -> str:
    start = str(selections).find('option value="') + 14
    end = str(selections).find('"', start)
    return str(selections)[start:end]


def get_new_soup(url: str) -> BeautifulSoup:
    r = requests.get(url)
    #  print(r.url)
    return BeautifulSoup(r.text, 'html.parser')


def write_file(name: str, url: str):
    os.makedirs(os.path.dirname(name), exist_ok=True)
    with open(name, "w+") as file_out:
        content = requests.get(url)
        file_out.write(str(content.content))


def get_file_list(overview: str) -> list:
    start = overview.find('"items":[') + 9
    end = overview.find("]", start)
    return overview[start:end].split("}")


def get_filename(description: str) -> str:
    start = description.find('"file","path":"') + 15
    end = description.find('"', start)
    return description[start:end]


def get_content_url(description: str) -> str:
    start = description.find('"hash":"') + 8
    end = description.find('"', start)
    return "https://socketusercontent.com/blob/" + str(description[start:end])


package_name = str(sys.argv[1])
print()
print(f"Looking up {package_name} on socket.dev this may take a minute . . .")
print()
package_url = "https://socket.dev/npm/package/" + package_name + "/files"

soup = get_new_soup(package_url)
list_of_versions = soup.find_all('select', "chakra-select")
if len(list_of_versions):
    if "0.0.1-security" in str(list_of_versions):
        previous_version = get_previous_version(list_of_versions)
        package_url += "/" + str(previous_version)
        soup = get_new_soup(package_url)

packages_overview = soup.find_all("script")[-1].text
# print(get_file_list(packages_overview))
list_of_items = get_file_list(packages_overview)
for item in list_of_items:
    filename = get_filename(item)
    file_path = "package_downloads/" + package_name + "/" + filename
    if len(filename) > 0:
        content_url = get_content_url(item)
        print(f"writing {file_path} {content_url}")
        write_file(file_path, content_url)
