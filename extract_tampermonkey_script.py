#!/usr/bin/env python3

# Linux usage: ./extract_tampermonkey_script.py "/home/<USER>/.config/<BROWSER>/Default/Local Extension Settings/<EXTENSION_ID>"
#        i.e.: ./extract_tampermonkey_script.py "/home/foo/.config/google-chrome-beta/Default/Local Extension Settings/gcalenpjmijncebpfijmoaglllgpjagf"
#   Mac usage: ./extract_tampermonkey_script.py "/Users/<USER>/Library/Application Support/Google/Chrome/Default/Local Extension Settings/<EXTENSION_ID>/"
#        i.e.: ./extract_tampermonkey_script.py "/Users/foo/Library/Application Support/Google/Chrome/Default/Local Extension Settings/dhdgffkkebhmkfjojejmpbldmpobfkfo/"

import leveldb
import sys
import re
import json
import codecs

pattern = re.compile(b"^@source(.*)$")

db = leveldb.LevelDB(sys.argv[1:][0])

for k,v in db.RangeIter():
    k = k.decode('utf-8')
    m = pattern.match(k)
    if m:
        v = v.decode('utf-8')
        name = re.sub("[\W\b]", "_", m.groups()[0].strip())
        full_name = "%s.user.js" % name

        print("Writing to %s" % full_name)

        content = json.JSONDecoder().decode(v)['value']

        with codecs.open(full_name, 'w', 'utf-8') as text_file:
            text_file.write(content)