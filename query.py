#!/usr/bin/python2.6
import cgitb
cgitb.enable()
import cgi
import sqlite3
import datetime
from docutils.core import publish_parts
import codecs
import re
import os

print "Content-type: text/html; charset=utf-8"
print 
print '<head>'
print '<link rel="stylesheet" href="../cgi-bin/table.css">'
print '<link rel="stylesheet" href="table.css">'
print '<title>EvoBib Reference Browser</title>'
print '</head>'

limit = 4709

# get the args of the url, convert nasty field storage to plain dictionary,
# there is probably a better solution, but this works for the moment
xargs = dict(
        key = '',
        user = '',
        template = '',
        phrase = '',
        keyword = '',
        show = '',
        edit = '',
        quote = '',
        page = '',
        comment = '',
        keywords = '',
        note = '',
        idf = ''
        )
args = {}
tmp_args = cgi.FieldStorage()
for arg in xargs:
    tmp = tmp_args.getvalue(arg)
    if tmp:
        args[arg] = tmp

if args.get('user') not in 'Mattis':
    db = sqlite3.connect('data2.sqlite3')
else:
    db = sqlite3.connect('data.sqlite3')
cursor = db.cursor()

parts = """.. role:: translation

.. role:: comment

.. role:: sampa

"""

def parse_comment(line, parts):

    href = '<a href="?key={0}">{0}</a><sup><span onclick="showBibTex(this);" data-eb={0} class="kw eb" href="http://bibliography.lingpy.org?key={0}" target="out">BibTex</span></sup>'
    if line[4].strip().lower() == '#abstract':
        parts += '**ABSTRACT**\n\n'
        comment = ''
    elif line[4].strip().lower() == '#summary':
        parts += '**SUMMARY**\n\n'
        comment = ''
    else:
        comment = line[4].encode('utf-8')
    page = line[3].encode('utf-8')
    if page == '000':
        page = ''
    else:
        page = '('+page+')'

    keywords = line[5].encode('utf-8').split(',')
    for i, k in enumerate(keywords):
        keywords[i] = '<a class="kw" href="?keyword='+k.strip()+'">'+k.strip()+'</a>'

    keywords = ', '.join(keywords)

    return (comment, parts, page, line[1],
            href.format(line[1].encode('utf-8')),
            keywords)

def dequote(quote):

    if '#' in quote:
        for ht in re.findall('#[a-zA-Z_]+', quote):
            quote = quote.replace(ht, '`'+ht[1:]+' <'+'?keyword='+ht[1:]+'>`_')
    if '@' in quote:
        for ht in re.findall('@<*[A-Z][a-zA-Z]*>*<*[0-9]*[a-z]*>*', quote):
            key = ht.replace('<', '').replace('>', '')
            visual = re.sub('<.*?>', '', ht)
            quote = quote.replace(ht, '`'+visual[1:]+' <?key='+key[1:]+'>`_')

    return quote

text = ''
if args.get('show', ''):
    query = 'select * from quotes where '
    items = []
    text = '<table class="refs">'
    previous = ''
    if args.get('idf'):
        query = 'select * from quotes where id="'+args['idf']+'";'
    else:
        if args.get('key'):
            items += ['key="'+args['key']+'"']
        if args.get('phrase'):
            if args['phrase'] in ['*'] or len(args['phrase']) < 4:
                pass
            else:
                items += ['quote like "%'+args['phrase']+'%"']
        if args.get('keyword'):
            for k in args['keyword'].split(','):
                if k.strip() and k.strip() not in ['*']:
                    items += ['keywords like "%'+k.strip()+'%"']
        if items:
            query += ' and '.join(items)+' order by page, note;'
        else:
            query = 'select * from quotes limit 0;'

    for line in cursor.execute(
            query):
        comment, current_parts, page, key, keyfmt, kw = parse_comment(line, parts)
        if previous != key:
            previous = key
            text += '<tr><th colspan="3">'+keyfmt+'</th></tr>'

        text += '<tr>'
        quote = line[2].encode('utf-8')
        quote = dequote(quote)
        quote = publish_parts( 
                        current_parts + quote + ' XSTOPX',
                        writer_name='html'
                        )['html_body']
        quote = quote[:quote.index('XSTOPX')].encode('utf-8') + '<span class="page">'+page+'</span> <sup><a title="permalink" style="color:Crimson;font-weight:bold" href="?idf='+str(line[0])+'">['+str(line[0])+']</a></sup>'
        if 'img' in quote:
            quote = quote.replace('src="static', 'src="http://lingulist.de/documents/talks')
        if args.get('phrase'):
            quote = quote.replace(
                    args.get('phrase', 'abcdefghijklmnopqrstuvw'), 
                    '<span style="background-color:yellow">'+args['phrase']+'</span>'
                    )
        if 'SUMMARY' in quote:
            quote = quote.replace('class="document"', 'class="document comment"')

        if args.get('user') not in ['Mattis']:
            comment = '---'
        if line[4] in ['#summary', '#abstract', '#toc']:
            comment = line[4].encode('utf-8')[1:].upper()
        idf = str(line[0])
        text += '<tr><td id="'+idf+'_quote" colspan="3">'+quote+'</td></tr>'
        text += '<tr><td id="'+idf+'_comment" class="comment">' + comment + '</td>'
        if args.get('user') in ['Mattis']:
            text += '<td id="'+idf+'_keywords" class="keywords">' + kw + '</td>'
            text += '<td><input type="submit" value="Modify" onclick="prepareModification(this)" '
            text += ' data-note="'+line[4].encode('utf-8')+'" '
            text += ' data-keywords="'+line[5].encode('utf-8')+'" '
            text += ' data-key="'+key.encode('utf-8')+'" '
            text += ' data-idf="'+str(line[0])+'" '
            text += ' data-page="'+line[3].encode('utf-8')+'" '
            text += ' data-quote="'+line[2].encode('utf-8')+'"</input></td>'
        else:
            text += '<td colspan="2" id="'+idf+'_keywords" class="keywords">' + kw + '</td>'
        text += '</tr>'
    text += '</table>'

print text

