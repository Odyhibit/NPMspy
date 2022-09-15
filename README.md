# NPMspy
Observe new NPM packages, looking for suspicious code.

## Requirements:
yara, or yara64.exe in your path.
oss-download available in your path.

### Webscraper
webscraper/scrape_libraries_io.py 
  * scrape the most recent package names from Libraries.io 
  * stored in the same directory in a sqlite database

### Downloading/Sanning packages
downloader/download_recent.py 
  * get most recent unscanned packages from database
  * use oss-download to save the package
  * use yara to scan the package
  * save results in database

### Database layout
![DBMS ER diagram (UML notation) (1)](https://user-images.githubusercontent.com/1384102/190476962-4d33e7c2-9358-4af8-ab1b-024f350a96b9.jpeg)
