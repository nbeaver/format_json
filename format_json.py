#! /usr/bin/env python3

import sys
import json
import argparse
import tempfile
import os
import logging
import platform

def format_json_in_place(pathname, sync=True):
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
        if sync:
            # Before we replace the old file with the new one,
            # force the new file to be fully written to disk.
            # Linux-only.
            # https://blog.gocept.com/2013/07/15/reliable-file-updates-with-python/
            tmp_fp.flush()
            logging.debug('attempting to run fdatasync on {}'.format(tmp_fp.name))
            try :
                os.fdatasync(tmp_fp)
            except AttributeError:
                logging.info("os.fdatasync not available on '{}'".format(platform.system()))
                pass
        else:
            logging.warning("file may not be fully written to disk: '{}'".format(tmp_fp.name))
    # Attempt to replace the file atomically.
    logging.debug("replacing '{}' with '{}'".format(tmp_fp.name, pathname))
    try:
        os.replace(tmp_fp.name, pathname)
    except AttributeError:
        # In Python 2.7, os.replace is not available.
        os.rename(tmp_fp.name, pathname)

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
        '-s',
        '--no-sync',
        help='Do not run fdatasync (file may not be completely written to disk)',
        action="store_false",
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
        format_json_in_place(target_path, args.no_sync)
