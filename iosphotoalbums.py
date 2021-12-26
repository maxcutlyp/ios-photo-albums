#!/usr/bin/env python3.10

import argparse
import sys
import plistlib
import os
import glob
import uuid
import sqlite3
import shutil

from typing import Iterable

def main(dcim_dir: str, photos_sqlite_file: str, albumsmetadata_dir: str, output_dir: str) -> int:
    dcim_dir = os.path.expanduser(dcim_dir)
    photos_sqlite_file = os.path.expanduser(photos_sqlite_file)
    albumsmetadata_dir = os.path.expanduser(albumsmetadata_dir)
    output_dir = os.path.expanduser(output_dir)
    files_in_albums = set()
    for title, uuids in get_uuids_of_photos_in_albums(albumsmetadata_dir):
        dest_dir = os.path.join(output_dir, title)
        os.makedirs(dest_dir, exist_ok=True)
        print(f'copying files to {dest_dir}...')
        for filename in get_filenames_from_uuids(uuids, photos_sqlite_file):
            shutil.copy2(os.path.join(dcim_dir, filename[5:]), dest_dir)
            files_in_albums.add(filename[5:])
    other_dir = os.path.join(output_dir, 'iOSPhotoAlbums_other')
    print(f'copying rest of the files into {other_dir}...')
    os.makedirs(other_dir, exist_ok=True)
    for filename in glob.glob(os.path.join(dcim_dir, '*APPLE', '*')):
        base, fname = os.path.split(filename)
        if os.path.join(os.path.split(base)[1], fname) not in files_in_albums:
            shutil.copy2(filename, other_dir)
    return 0

def get_filenames_from_uuids(uuids: Iterable[str], photos_sqlite_file: str) -> Iterable[str]:
    connection = sqlite3.connect(photos_sqlite_file)
    cursor = connection.cursor()
    formatted_uuids = ','.join(f'"{image_uuid.upper()}"' for image_uuid in uuids)
    for row in cursor.execute(f'SELECT ZDIRECTORY, ZFILENAME FROM ZASSET WHERE ZUUID IN ({formatted_uuids})'):
        yield os.path.join(row[0], row[1])

def get_uuids_of_photos_in_albums(albumsmetadata_dir: str) -> Iterable[Iterable[str]]:
    for albummetadata_file in glob.glob(os.path.join(albumsmetadata_dir, '*.albummetadata')):
        with open(albummetadata_file, 'rb') as f:
            plist = plistlib.load(f)
            info = plist['$top']
            objects = plist['$objects']
            try: title = objects[info['title'].data]
            except KeyError: continue
            if (prompt_yn(f'Create album "{title}"?', True)):
                yield title, (str(ux) for ux in _unwrap_uuids(objects[info['assetUUIDs']]))

# courtesy of https://github.com/yoshtec/catplist/, ty <3 (slightly modified)
def _unwrap_uuids(b: bytes) -> Iterable[uuid.UUID]:
    i = 0
    while i < len(b):
        yield uuid.UUID(bytes=b[i : i + 16])
        i = i + 16

def prompt_yn(question: str, default: bool):
    ans = input(f'{question} [{"Y/n" if default else "y/N"}] ').lower().strip()
    if default:
        return ans[:1] != 'n'
    else:
        return ans[:1] == 'y'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert iOS albums into folders')
    parser.add_argument('dcim_dir', metavar='DCIM', type=str, help='path/to/DCIM')
    parser.add_argument('photos_sqlite_file', metavar='Photos.sqlite', type=str, help='path/to/Photos.sqlite')
    parser.add_argument('albumsmetadata_dir', metavar='AlbumsMetadata', type=str, help='path/to/AlbumsMetadata')
    parser.add_argument('-o', dest='output_dir', metavar='output', type=str, help='path/to/desired/output', default='.')

    args = parser.parse_args()
    sys.exit(main(args.dcim_dir, args.photos_sqlite_file, args.albumsmetadata_dir, args.output_dir))
