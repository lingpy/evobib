#!/usr/bin/python2.6
import cgitb
cgitb.enable()
import cgi
import sqlite3
import datetime
from docutils.core import publish_parts

print "Content-type: text/html; charset=utf-8"

# get the args of the url, convert nasty field storage to plain dictionary,
# there is probably a better solution, but this works for the moment
xargs = dict(
        remote_dbase = '',
        key = '',
        date = '',
        new_id = '',
        tables = '',
        summary = '',
        unique = '',
        columns = '',
        concepts = '',
        doculects = '',
        template = '',
        history = '',
        phrase = '',
        )
args = {}
tmp_args = cgi.FieldStorage()
for arg in xargs:
    tmp = tmp_args.getvalue(arg)
    if tmp:
        args[arg] = tmp

dbpath = 'data.sqlite3'

# connect to the sqlite database
db = sqlite3.connect(dbpath)
cursor = db.cursor()


print ''
print '<html><body>'
print '<style>td {border:2px solid gray;}'
print '.comment {color:red;}'
print '.keywords {color:darkgreen;}'
print '</style>'
print '<h3>EvoBib Reference Browser</h3>'
print '<form action="" method="get">'
print 'Enter bibliographic key: <input type="text" style="width:200px;" name="key" />'
print '</form>'
print '<form action="" method="get">'
print 'Enter phrase key: <input type="text" style="width:200px;" name="phrase" />'
print '</form>'


href = '<a href="http://bibliography.lingpy.org?key={0}" target="out">{0}</a>'
if args.get('key', '') and not args.get('phrase', ''):
    print '<table style="border:2px;width:80%">'
    for line in cursor.execute(
            'select * from quotes where key="'+args['key']+'";'):
        print '<tr>'
        print '<td>' + href.format(line[1].encode('utf-8')) + '</td>'
        print '<td>' + line[3].encode('utf-8') + '</td>'
        print '</tr>'
        quote = line[2].encode('utf-8')
        quote = publish_parts(
                ".. role:: translation\n\n..  role::comment\n\n ..role:: sampa\n\n" + \
                        quote + ' XSTOPX',
                        writer_name='html'
                        )['html_body']
        quote = quote[:quote.index('XSTOPX')]
        print '<tr><td colspan="2">'+quote.encode('utf-8')+'</td></tr>'
        print '<tr><td class="comment">' + line[4].encode('utf-8') + '</td>'
        print '<td class="keywords">' + line[5].encode('utf-8') + '</td></tr>'
    print '</table></body></html>'

if args.get('phrase', '') and not args.get('key', ''):
    print '<table style="border:2px;width:80%">'
    for line in cursor.execute(
            'select * from quotes where quote like "%'+args['phrase']+'%" or keywords like "%'+args['phrase']+'%" or note like "%'+args['phrase']+'%";'):
        print '<tr>'
        print '<td>' + href.format(line[1].encode('utf-8')) + '</td>'
        print '<td>' + line[3].encode('utf-8') + '</td>'
        print '</tr>'
        quote = line[2].encode('utf-8')
        quote = publish_parts(
                ".. role:: translation\n\n..  role::comment\n\n ..role:: sampa\n\n" + \
                        quote + ' XSTOPX',
                        writer_name='html'
                        )['html_body']
        quote = quote[:quote.index('XSTOPX')]
        quote = quote.replace(args['phrase'], '<span style="background-color:yellow">'+args['phrase']+'</span>')
        print '<tr><td colspan="2">'+quote.encode('utf-8')+'</td></tr>'
        print '<tr><td class="comment">' + line[4].encode('utf-8') + '</td>'
        print '<td class="keywords">' + line[5].encode('utf-8') + '</td></tr>'
    print '</table></body></html>'



