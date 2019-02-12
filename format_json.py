#! /usr/bin/env python3

import sys
import json
import argparse
import tempfile
import os
import logging

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
            sort_keys=True,
        )
        tmp_fp.write('\n') # add a trailing newline.
    # Replace the file atomically.
    logging.debug("replacing '{}' with '{}'".format(tmp_fp.name, pathname))
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
        '-v',
        '--verbose',
        help='More verbose logging',
        dest="loglevel",
        default=logging.WARNING,
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        '-d',
        '--debug',
        help='Enable debugging logs',
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
    )
    parser.add_argument(
        '-n',
        '--no-follow',
        help='Do not follow symbolic links, dereference and create a new copy instead',
        action="store_true",
    )
    parser.add_argument(
        'files',
        type=writeable_file,
        help='JSON filepaths',
        nargs='+'
    )
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)
    for json_file in args.files:
        if args.no_follow:
            target_path = json_file
        else:
            target_path = os.path.realpath(json_file)
        format_json_in_place(target_path)
