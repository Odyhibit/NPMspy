import os
import subprocess


def in_red(red_text: str) -> str:
    return "\033[31m" + str(red_text) + "\033[0m"


def in_green(green_text: str) -> str:
    return "\033[32;1m" + str(green_text) + "\033[0m"


def yara_rule(start_from: str) -> str:
    # linux: yara -r ../downloader/yara_rules/rules.yara  ./set1_malware_packages
    # windows: yara64 -r ../downloader/yara_rules/rules.yara  ./set1_malware_packages
    yara_response = subprocess.run([yara, "-r", "../downloader/yara_rules/rules.yara", start_from], capture_output=True, encoding="UTF-8")
    return yara_response.stdout


#  In linux the command is yara, in windows it is yara64
yara = "yara"
if os.name == "nt":
    yara = "yara64"

print("***   Testing Yara Rules   ***")
list_directories = [f.name for f in os.scandir(path="./set1_malware_packages") if f.is_dir()]

for directory in list_directories:
    print(directory)
    results = yara_rule("./set1_malware_packages/" + directory).split()
    if len(results) > 1:
        for i, result in enumerate(results):
            if i % 2 == 0:
                print("\t", in_green(result), end="")
            else:
                print(" in file", result)
    else:
        print("\t", in_red("No matches"))

