#!/usr/bin/python2.6
import cgi
import os
import sqlite3
import urllib
import json

print "Content-type: text/plain; charset=utf-8"
print


# get the args of the url, convert nasty field storage to plain dictionary,
# there is probably a better solution, but this works for the moment
tmp_args = cgi.FieldStorage()
args = {}
for arg in tmp_args:
    args[arg] = tmp_args[arg].value

db = sqlite3.connect('data.sqlite3')
cursor = db.cursor()

# check for remote user
if 'REMOTE_USER' in os.environ:
    user = os.environ['REMOTE_USER']
else:
    user = 'unknown'

if 'add' in args:
    key = args.get('key')
    phrase = args.get('phrase')
    page = args.get('page')
    if key and phrase and page:
        keyword = args.get('keyword', '-')
        comment = args.get('comment', '-')
        query = 'insert into quotes (id, key, quote, page, note, keywords) values (NULL, ?, ?, ?, ?, ?);'
        try:
            cursor.execute(query, (
                urllib.unquote(key), 
                urllib.unquote(phrase), 
                urllib.unquote(page), 
                urllib.unquote(comment), 
                urllib.unquote(keyword)
                ))
            message = 'success'
        except Exception as e:
            message = e
    db.commit()
    print message
            
elif 'modify' in args:
    key = args.get('key')
    phrase = args.get('quote')
    page = args.get('page')
    idx = args.get('idf')

    if key and phrase and page and idx:
        keyword = args.get('keyword', '-')
        comment = args.get('comment', '-')

        query = 'update quotes set key="'+urllib.unquote(key)+'"' +\
                ', quote="'+urllib.unquote(phrase)+'"' +\
                ', page="'+urllib.unquote(page)+'"'+\
                ', note="'+urllib.unquote(comment)+'"'+\
                ', keywords="'+urllib.unquote(keyword)+'" where '+\
                'id='+idx+';'
        print query
        try:
            cursor.execute(query)
            message = 'success'
        except Exception as e:
            message = 'error'
    db.commit()
    print message
