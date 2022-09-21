#  Josh Bloom
import requests
from bs4 import BeautifulSoup


def get_filename(url: str, version: str) -> str:
    return url[url.find(version) + len(version):]


def get_raw_contents(url: str) -> requests.Response.content:
    r = requests.get(url)
    return r.content


def get_previous_version(selections: BeautifulSoup.find_all) -> str:
    start = str(selections).find('option value="') + 14
    end = str(selections).find('"', start)
    return str(selections)[start:end]


def has_raw_button(page_soup: BeautifulSoup) -> bool:
    raw_button = page_soup.find_all('a', class_="chakra-button css-zi9wpa")
    # print("looking for raw button", raw_button, len(raw_button))
    return len(raw_button) > 0


def has_file_list(page_soup: BeautifulSoup) -> bool:
    link_list = page_soup.find_all('a', class_="chakra-link css-10qsrqw")
    return len(link_list) > 0


def get_filename_from_url(url: str) -> str:
    start = url.find("files/") + 6
    start = url.find("/", start)
    return url[start:]


def process_folders_files(page_soup: BeautifulSoup, url: str):
    if has_raw_button(page_soup):
        print(url, "has a raw button")
        filename = get_filename_from_url(url)
        raw_content_url = soup.find('a', class_="chakra-button css-zi9wpa")
        write_file(filename, raw_content_url)
        return
    elif has_file_list(page_soup):
        for link in soup.find_all('a', class_="chakra-link css-10qsrqw"):
            print(url + get_filename_from_url(link['href']))
            this_url = url + get_filename_from_url(link['href'])
            new_soup = get_new_soup(this_url)
            print("content", new_soup.find('a', class_="chakra-button css-zi9wpa"))
            process_folders_files(new_soup, this_url)


def get_new_soup(url: str) -> BeautifulSoup:

    r = requests.get(url)
    #  print(r.url)
    return BeautifulSoup(r.text, 'html.parser')


def write_file(filename: str, content_url: str):
    with open("package_downloads/" + filename, "wb") as file_out:
        content = requests.get(content_url)
        file_out.write(content.content)



package_name = "oaut"
package_url = "https://socket.dev/npm/package/" + package_name + "/files"

soup = get_new_soup(package_url)
list_of_versions = soup.find_all('select', "chakra-select")
if len(list_of_versions):
    previous_version = get_previous_version(list_of_versions)
    package_url += "/" + str(previous_version)
    soup = get_new_soup(package_url)

process_folders_files(soup, package_url)
