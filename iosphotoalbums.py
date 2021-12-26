#!/usr/bin/env python3.10

import argparse
import sys
import plistlib
import os
import glob
import uuid

from typing import Iterable

def main(dcim_dir: str, photos_sqlite_file: str, albumsmetadata_dir: str, output_dir: str) -> int:
    for uuids in get_uuids_of_photos_in_albums(os.path.expanduser(albumsmetadata_dir)):
        for image_uuid in uuids:
            print(image_uuid)
    return 0

def get_uuids_of_photos_in_albums(albumsmetadata_dir: str) -> Iterable[Iterable[str]]:
    for albummetadata_file in glob.glob(os.path.join(albumsmetadata_dir, '*.albummetadata')):
        with open(albummetadata_file, 'rb') as f:
            plist = plistlib.load(f)
            info = plist['$top']
            objects = plist['$objects']
            try: title = objects[info['title'].data]
            except KeyError: continue
            if (prompt_yn(f'Create album "{title}"?', True)):
                yield (str(ux) for ux in _unwrap_uuids(objects[info['assetUUIDs']]))

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
