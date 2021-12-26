#!/usr/bin/env python3.10

import argparse
import sys

def main(dcim_dir: str, photos_sqlite_file: str, output_dir: str) -> int:
    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert iOS albums into folders')
    parser.add_argument('dcim_dir', metavar='DCIM', type=str, help='path/to/DCIM')
    parser.add_argument('photos_sqlite_file', metavar='Photos.sqlite', type=str, help='path/to/Photos.sqlite')
    parser.add_argument('albumsmetadata_dir', metavar='AlbumsMetadata', type=str, help='path/to/AlbumsMetadata')
    parser.add_argument('-o', dest='output_dir', metavar='output', type=str, help='path/to/desired/output', default='.')

    args = parser.parse_args()
    sys.exit(main(args.dcim_dir, args.photos_sqlite_file, args.output_dir))
