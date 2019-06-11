Script to format JSON files in place
====================================

Usage
-----

::

     $ format_json.py /path/to/file1.json

also handles multiple files::

     $ format_json.py /path/to/file1.json /path/to/file2.json

Features
--------

- Correctly modifies files in place with temporary files and ``fdatasync()``.

  (This can be turned off with ``-s`` ``--no-sync``.)

- Follows symlinks properly instead of dereferencing and creating a new copy.

  (This can be turned off with ``-n`` ``--no-follow``.)

- Adjustable indentation level (defaults to 4 spaces).

  (Adjustable with ``-i`` ``--indent``.)

Motivation
----------

There are many tools to pretty-print JSON:

https://stackoverflow.com/questions/5243885/json-command-line-formatter-tool-for-linux

https://stackoverflow.com/questions/352098/how-can-i-pretty-print-json-in-a-shell-script

https://www.pixelstech.net/article/1471447824-Format-JSON-data-on-Ubuntu

However, these tools do not format JSON in place
the way that e.g. ``sed`` does with the ``--in-place`` flag.

Doing this in a way that atomically updates the file in place
is surprisingly tricky to get right.

https://stupidpythonideas.blogspot.com/2014/07/getting-atomic-writes-right.html

https://blog.gocept.com/2013/07/15/reliable-file-updates-with-python/

https://backreference.org/2011/01/29/in-place-editing-of-files/
