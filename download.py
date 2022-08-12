# Dependencies: warcio, requests

from shutil import copyfileobj
from warcio.archiveiterator import ArchiveIterator

import cgi
import json
import os
import requests
import sys

def get_warc(id, url):
    # qAudio stores IDs as integers encoded in base36, but we want our folder names to start with
    # ints in base 10, so that natural sorting in file managers works correctly.
    # For example, we want ID 1A (36 in base 10) to come after ID 2 (2 in base 10) in our list of folders.
    # If we don't use base 10 integers, file managers will sort lexicographically, putting 1A before 2.

    destination_path = f"qaudio-archive/{int(id, base=36)} ({id})"
    os.makedirs(destination_path)
    resp = requests.get(url, stream=True)

    for record in ArchiveIterator(resp.raw):
        if record.rec_type != 'response':
            continue    

        file_id = record.rec_headers['WARC-Target-URI'].split('/')[-1]
        if 'Content-Disposition' not in record.http_headers:
            # This response has no associated filename, so it's probably an error of some sort.
            print(f'skipping id {file_id}')
            print(record.http_headers)
            continue

        disposition = record.http_headers['Content-Disposition']
        _, params = cgi.parse_header(disposition)
        original_filename = params['filename']

        without_ext, ext = os.path.splitext(original_filename)
        # We also want decimal IDS at the beginning here for sorting purposes.
        our_filename = f"{int(file_id, base=36)} - {without_ext} ({file_id}).{ext}"
        file_path = f"{destination_path}/{our_filename}"

        with open(file_path, "wb") as f:
            copyfileobj(record.raw_stream, f)


with open('urls.json') as f:
    urls = json.load(f)

_, first, last = sys.argv

# It's not terribly easy to converts ints back to base 36.
# This is sort of a hack relying on the fact that ids in urls.json are sorted in the right order.

id_list = list(urls.keys())
to_fetch = id_list[id_list.index(first):id_list.index(last)+1]

for id in to_fetch:
    print(f"Fetching {id}")
    get_warc(id, urls[id])
