#  Josh Bloom
import requests
from bs4 import BeautifulSoup


def get_raw_contents(url: str) -> requests.Response.content:
    r = requests.get(url)
    return r.content


def get_previous_version(selections: BeautifulSoup.find_all) -> str:
    start = str(selections).find('option value="') + 14
    end = str(selections).find('"', start)
    return str(selections)[start:end]


def has_file_list(page_soup: BeautifulSoup) -> bool:
    link_list = page_soup.find_all('a', class_="chakra-link css-10qsrqw")
    return len(link_list) > 0


def get_new_soup(url: str) -> BeautifulSoup:
    r = requests.get(url)
    #  print(r.url)
    return BeautifulSoup(r.text, 'html.parser')


def write_file(filename: str, content_url: str):
    with open("package_downloads/" + filename, "wb") as file_out:
        content = requests.get(content_url)
        file_out.write(content.content)
        print("writing file", "package_downloads/" + filename, "wb")


def get_file_list(overview: str) -> str:
    start = overview.find('"items":[') + 9
    end = overview.find("]", start)
    print("get list", overview[start:end])
    return overview[start:end]


def get_next_item(file_list: str) -> str:
    start = file_list.find("{")
    end = file_list.find("}")
    print("get item", file_list[start:end])
    return file_list[start:end]


def get_filename(item: str) -> str:
    start = item.find('"file","path":"') + 15
    end = item.find('"', start)
    print("get name",start,end, item[start:end])
    return item[start:end]

package_name = "oaut"
package_url = "https://socket.dev/npm/package/" + package_name + "/files"

soup = get_new_soup(package_url)
list_of_versions = soup.find_all('select', "chakra-select")
if len(list_of_versions):
    previous_version = get_previous_version(list_of_versions)
    package_url += "/" + str(previous_version)
    soup = get_new_soup(package_url)

packages_overview = soup.find_all("script")[-1].text
# print(get_file_list(packages_overview))
print(get_filename(get_next_item(get_file_list(packages_overview))))
