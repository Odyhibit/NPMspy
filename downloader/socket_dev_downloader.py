#  Josh Bloom
import os
import sys

import requests


def get_previous_version(selections: str) -> str:
    start = str(selections).find('option value="') + 14
    end = str(selections).find('"', start)
    return str(selections)[start:end]


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


def write_file(name: str, url: str):
    os.makedirs(os.path.dirname(name), exist_ok=True)
    with open(name, "w+") as file_out:
        content = requests.get(url)
        file_out.write(content.content.decode("utf-8"))


def download_package(name: str):
    package_name = str(name)
    print()
    print(f"Looking up {package_name} on socket.dev this may take a minute . . .")
    print()
    package_url = "https://socket.dev/npm/package/" + package_name + "/files"

    page_source = requests.get(package_url).text

    if "0.0.1-security" in page_source:
        previous_version = get_previous_version(page_source)
        package_url += "/" + str(previous_version)
        page_source = requests.get(package_url).text

    list_of_items = get_file_list(page_source)

    for item in list_of_items:
        filename = get_filename(item)
        file_path = "package_downloads/" + package_name + "/" + filename
        if len(filename) > 0:
            content_url = get_content_url(item)
            print(f"writing {file_path}")
            write_file(file_path, content_url)


if __name__ == "__main__":
    download_package(sys.argv[1])

