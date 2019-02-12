#! /usr/bin/env python3

import sys
import json
import argparse
import tempfile
import os

# https://backreference.org/2011/01/29/in-place-editing-of-files/
def format_json_in_place(pathname):
    dirname = os.path.dirname(pathname)
    with open(pathname, 'r') as fp:
        try:
            data = json.load(fp)
        except ValueError:
            sys.stderr.write("In file: {}\n".format(fp.name))
            raise
    # Create a temporary file in the same directory.
    with tempfile.NamedTemporaryFile(mode='w', dir=dirname, delete=False) as tmp_fp:
        json.dump(
            data,
            tmp_fp,
            ensure_ascii=False,
            indent=4,
            separators=(',', ': '),
            sort_keys=True
        )
        tmp_fp.write('\n') # add a trailing newline.
    # Replace the file atomically.
    os.replace(tmp_fp.name, pathname)

def writeable_file(pathname):
    if not os.path.isfile(pathname):
        raise argparse.ArgumentTypeError(
            'not an existing file: {}'.format(pathname))
    if not os.access(pathname, os.W_OK):
        raise argparse.ArgumentTypeError(
            'not a writable file: {}'.format(pathname))
    return pathname

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Format JSON files in place.'
    )
    parser.add_argument(
        'files',
        type=writeable_file,
        help='JSON filepaths',
        nargs='+'
    )
    args = parser.parse_args()
    for json_file in args.files:
        format_json_in_place(json_file)
