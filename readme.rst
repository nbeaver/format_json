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
