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




# get the args of the url, convert nasty field storage to plain dictionary,
# there is probably a better solution, but this works for the moment
xargs = dict(
        key = '',
        author = '',
        year = '',
        title = '',
        fulltext = '',
        display = '',
        keys = '',
        search = '',
        )
args = {}
tmp_args = cgi.FieldStorage()
for arg in xargs:
    tmp = tmp_args.getvalue(arg)
    if tmp:
        args[arg] = tmp

db = sqlite3.connect('evobib.sqlite3')
cursor = db.cursor()

display = 'bibtex'

if args.get('display', ''):
    display = args.get('display', '')

if display == 'js':
    print "Content-type: application/javascript; charset=utf-8"

else:
    print "Content-type: text/html; charset=utf-8"
    print 
    print '<head>'
    print '<link rel="stylesheet" href="../cgi-bin/table.css">'
    print '<link rel="stylesheet" href="table.css">'
    print '<title>EvoBib BibTex</title>'
    print """<script type="text/javascript">
    function showBibTex(node){
        var falert = document.createElement('div');
        falert.id='fake';
        falert.class='fake_alert';
        var text = '<div class="message"><p>Entry in BibTex</p><p><pre style="overflow-x:scroll;text-align:left;margin:10px;padding:10px;background-color:white;">'+node.dataset['bibtex']+'</pre></p>';
        text += '<div style="background-color:Crimson;color:white;cursor:pointer;border:2px solid white;" onclick="closeBibTex();">CLOSE</div></div>';
        document.body.appendChild(falert);
        falert.innerHTML=text;
    }
    function closeBibTex(){
      var fake = document.getElementById('fake');
      document.body.removeChild(fake);
    }
    </script>
    <style>
    .fake_alert {
    	position: fixed;
    	background-color: rgba(0,0,0,0.5);
    	z-index: 100;
    	top:0;
    	left: 0;
    	right: 0;
    	bottom: 0;
    	width: 100%;
    	height: 100%;
    	float: left;
    	text-align:center;
    }
    .message {
      position: absolute;
      margin-left: auto;
      margin-right: auto;
      top:30%;
      left:0;
      right:0;
      background-color: #2d6ca2;
      border: 2px solid LightYellow;
      text-align:center;
      min-width:200px;
      max-width:50%;
      width: auto;
      float: left;
      border-radius:5px;
    }
    </style>
    """
    print '</head>'

if args.get('search', ''):
    search = args.get('search', '')
    search = search.split(',')
    query = 'select key, author, editor, title, booktitle, year, url, doi, bibtex from bibliography where bibtex like "%'+search[0].strip()+'%"'
    for term in search[1:]:
        query += 'and bibtex like "%'+term.strip()+'%"'
    query += ' order by year;'

elif args.get('fulltext', ''):
    fulltext = args.get('fulltext', '')
    query = 'select key, author, editor, title, booktitle, year, url, doi, bibtex from bibliography where bibtex like "%'+fulltext+'%" order by year;'

elif args.get('key', ''):
    query = 'select key, author, editor, title, booktitle, year, url, doi, bibtex from bibliography where key="'+args.get('key', '')+'" order by year;'

elif args.get('keys', ''):
    query = 'select key, author, editor, title, booktitle, year, url, doi, bibtex from bibliography where key like "'+args.get('keys', '')+'%" order by year;'

else:
    query = ''

if display == 'keys':
    keys = []
    for line in cursor.execute('select key from bibliography;'):
        keys += [line[0]]
    keys = ', '.join(keys)
    print '<span type="hidden" id="keys" data-list="'+keys+'"></span>';
    
elif display == 'table':
    text = '<table class="refs">'
    text += """
<tr>
  <th>Key</th>
  <th>Author</th>
  <th>Title</th>
  <th>Year</th>
  <th>URL</th>
  <th>Reference</th>
</tr>
    """
    hits = 0
    for line in cursor.execute(query):

        bibtex = line[-1].replace('"', "''")
        doi, url = line[7], line[6]
        if not url: url = ''
        if not doi: doi = ''
        if doi:
            doi = '<a target="_blank" href="'+doi+'">DOI</a>'
        elif url.strip():
            doi = '<a target="_blank" href="'+url+'">URL</a>'
        else:
            doi = ''

        author, editor = line[1], line[2]
        if not author:
            author = editor
            editor = True
        else:
            editor = False
        
        author = author.split(' and ')
        
        if len(author) == 1:
            author = author[0]
        elif len(author) == 2:
            author = ' and '.join(author)
        else:
            author = author[0]+' et al.'
        if editor:
            author += ' (ed.)'

        year = line[5]
        if not year: year=''

        title, booktitle = line[3], line[4]
        if not title:
            title = booktitle

        td = """
<tr>
  <td><span class="ebkey" data-eb="{0}">{0}</a></td>
  <td>{1}</td>
  <td>{2}</td>
  <td>{3}</td>
  <td>{4}</td>
  <td ><span class="eb" style="cursor:pointer;" data-eb="{0}" data-bibtex="{5}" onclick="showBibTex(this);">BibTex</span></td>
</tr>
        """.format(
                line[0],
                author.encode('utf-8'),
                title.encode('utf-8'),
                year,
                doi,
                bibtex.encode('utf-8')
                )
        text += td
        hits += 1
    text += '</table>'
    if hits: print(text)
    else:
        print 'No values selected.'

elif display == 'js':
    print
    print 'var EvoBib = {'
    text = ''
    for key, bibtex in cursor.execute('select key, bibtex from bibliography;'):
        
        textp = '"'+key+'": "'+bibtex.replace('"', '')+'",'
        textp = textp.replace('<', '&lt;')
        textp = textp.replace('>', '&lt;')
        textp = textp.replace('\n', r'\n')
        text += textp.encode('utf-8')
    text = text[:-1]
    print text
    print '};'

else:
    text = '<pre>'
    for line in cursor.execute(query):

        bibtex = line[-1].replace('"', "''")
        text += '\n'+bibtex.encode('utf-8')+'\n'
    print(text)
