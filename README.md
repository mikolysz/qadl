# qadl – Tools for downloading content from the qAudio archive.

## What is qAudio?

qAudio was a service for uploading audio clips. It was integrated with specialized Twitter clients for the blind and mostly popular in the blind community. These clients could often play qAudio links without oepning a web browser, as well as upload and record new clips when composing tweets. Therefore, the service was primarily used to compose audio tweets, something that the blind community loved to do.

Some people also used the service to exchange private voice messages, not realizing that all the content they posted was public and couldn't be deleted later. QAudio links followed a predictable pattern, so links to such content could be guessed easily, in fact, this is precisely how the qAudio archive was made.

## What is the qAudio archive?

Many people have successfully scraped all the contents of qAudio, a fact which the owner of the service wasn't terribly happy about. At some point, when the qAudio maintainer announced that he was considering shutting the service down, an effort was organized to create a public archive of all the files that have ever been uploaded to it. This archive was ultimately created by ArchiveTeam and published on archive.org. However, as it stands, the format of that archive isn't particularly friendly to casual browsing, and specialized tools are required to access its contents. Even with such specialized tools, this process can be described as clunky at best.

## What do the scripts in this repository do?

These scripts allow you to download any part of the qAudio archive you wish, and extract it in a way which enables fast, efficient browsing. They have the following properties:

- The way the filenames are generated ensures that, when browsing, files are sorted chronologically, as they've been added to the archive. This requires your file manager of choice to support natural sorting, I.e. 2.mp3 must come before 10.mp3, not after.
- It's possible to download any chronological slice of the archive without too much effort.
- Original file extensions are preserved and original filenames are visible, allowing for easy access to the downloaded files with ordinary media players.

To my knowledge, no existing tools have these properties, that's why these scripts were written.

For now, using these scripts requires some commandline expertise. Hopefully I'll find a person willing to host this version of the archive at some point, which would make it accessible to users who aren't as tech savvy. If that doesn't happen, I'll consider writing a nicer user-interface myself.

## Dependencies

For these scripts to work, you will need a relatively recent version of Python 3 to be installed. I used version 3.10.1 in development. For most users, requests and warcio need to be installed from pip, if you want to regenerate the urls.json file, you will also need to get the lxml and beautifulsoup4 packages.

## How to use

After installing Python3 and all the required dependencies, change to the directory containing the contents of this repository and execute:

```
python3 download.py <first_pack_id> <last_pack_id>
```

All "packs", from the first up to and including the last, will be downloaded.

### A note about pac ids:

The archive, being the size that it is, is split into multiple .warc.gz files, called packs in this document. Each pack contains roughly 36 files from qAudio itself. Pack ids follow a certain scheme, they start at 1, 2, 3, go to 9, then to A, B, C, and so on up to Z. Then, they go throuhg 10, 11, 12, ..., 19, 1A, 1B, ..., 1Z, 20, 21, ... 29, 2A, ... 2Z, up to 90, 91, 92, ..., 9Z, A0, A1, A2, ... AZ, B1. B2, ..., bZ, up to ZZ. Then, they go from 100, 101, ..., 10Z, 110, 111, 11Z, etc. up to 1ON, which seems to be the last pack.

## Regenerating URLs

The archive is randomly split into 7 parts, each containing a certain number of packs. The packs are distributed randomly, that is, ID 1 is in part 1, ID 2 in part 3, ID 3 in part 2 and so on. This repository contains a file called urls.json, mapping pack IDS to their download URLs (which are based on the part they're in). If you, for whatever reason, want to regenerate this file, running the `get_urls.py` script will do just that. This script fetches the XML file lists for all the 7 parts, and figures out which part contains which packs.

## Contributing

If you have any suggestions or want to improve any of these scripts, feel free to raise an issue or file a pull request. Any help is appreciated. For now, the scripts assume that the user knows what they're doing and throw cryptic errors when inappropriate inputs are given. This is only a temporary state of affairs and will be fixed in a next version.

# License

This scripts are licensed under the BSD 2-clause license.
