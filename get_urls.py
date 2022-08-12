# Requires requests, lxml, beautifulsoup4

from bs4 import BeautifulSoup
from collections import OrderedDict
import json
import re
import requests

PARTS = 7
#PARTS=2 # Uncomment for testing to make the script go faster.
urls = {}
ID_REGEXP = re.compile(r'qaudio-([a-zA-Z0-9]+)\.warc\.gz')

for i in range(1, PARTS+1):
    idx_url = f"https://archive.org/download/archiveteam-qaudio-archive-{i}/archiveteam-qaudio-archive-{i}_files.xml"
    resp = requests.get(idx_url)

    soup = BeautifulSoup(resp.content, features='xml')

    for file in soup.find_all('file'):
        name = file['name']
        match = ID_REGEXP.search(name)
        if match is None:
             # This is a metadata file and has no data we care about.
            continue

        id = match.group(1)
        urls[id] = f"https://archive.org/download/archiveteam-qaudio-archive-{i}/qaudio-{id}.warc.gz"

# IDs are integers stored in base36.
sorted_urls = dict(sorted(urls.items(), key = lambda item: int(item[0], base=36)))
out = open("urls.json", "w")
json.dump(sorted_urls, out, indent=4)