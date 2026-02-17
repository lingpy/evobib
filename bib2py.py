# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2010-09-22
# modified : 2026-02-17 09:19
"""
EvoBib Conversion Script
"""

__author__="Johann-Mattis List"
__date__="2026-02-17"


import sqlite3
from re import sub,findall,DOTALL
from sys import argv
import os
import codecs

# These are the parameters, which are used in the current implementation.
parameters = [
        'Isbn',
        'Author',
        'Series',
        'Abstract',
        'Number',
        'Keywords',
        'Year',
        'Title',
        'Booktitle',
        'Institution',
        'Note',
        'Editor',
        'Howpublished',
        'Journal',
        'Volume',
        'Address',
        'Pages',
        'Publisher',
        'School',
        'Doi',
        'Edition',
        'Url',
        'Crossref',
        'Userb',
        'Usera',
        ]
parameters.sort(key=lambda x: len(x), reverse=True)


# Connect the database, the name of the database is passed as argv[1]
#db_name = argv[1]

os.system('rm evobib.sqlite3')

conn = sqlite3.connect('evobib.sqlite3')
c = conn.cursor()

# Create the string that is used in order to create the table "bibliography" in the db
create_table = 'create table bibliography(key text,type text,bibtex text'
for parameter in parameters:
    create_table = create_table + ',' + parameter.lower() + ' text'
create_table = create_table + ');'

# Create the table in the db
c.execute(create_table)

# Read the data from the bibtex-file, the name of the file is the same as db_name
infile = open('evobib-cleaned.bib','r').read()

# Find all distinc entries in the db
entries = findall('\n@.*?\n}', infile, DOTALL)
print(len(entries))

print("First run, searching for crossrefs...")
globaldict = {}
for entry in entries:
    print(entry[:10])
    for param in parameters:
        entry = entry.replace('  '+param, '  '+param.lower())
    this_type = findall('\n@(.*?){',entry)[0].lower()
    this_key = findall('\n@.*?{(.*?),',entry)[0]
    globaldict[this_key] = {}
    if 'XXX' in this_key or this_type.lower() in ['set',"customa","customb",
            "lecture", "preprint"] or '{Media}' in entry:
        pass
    else:
        this_entry_dict = {}
        for param in parameters:
            param = param.lower()
            try:
                result = findall("  *" + param + '\s*= {(.*?)},*\n',entry, DOTALL)[0]
            except:
                try:
                    result = findall("  *" + param + '\s*= {(.*?)},*\n',
                            entry, DOTALL)[0]
                except:
                    result = ''
            if result != '':
                this_entry_dict[param.lower()] = result.replace('\n',' ').replace('}','').replace('{','').replace('\t',' ').replace('  ',' ')
                globaldict[this_key][param] = this_entry_dict[param]
print("...done.")
print(len(globaldict))

converter = {'mvbook': 'book', 'mvcollection': 'collection', 'phdthesis':
        'thesis', 'bookinbook': 'book', 'inbook': 'incollection'}

count = 0
print("Second run, converting to sqlite...")
# Start the main loop
bibout = codecs.open('evobib-converted.bib', 'w', 'utf-8')
etypes = set()
gdict2 = {}
for entry in entries:
    for param in parameters:
        entry = entry.replace('  '+param, '  '+param.lower())

    for param in parameters:
        param = param.lower()
        entry = entry.replace('  '+param, '  '+param.lower())
    this_type = findall('\n@(.*?){',entry)[0].lower()
    this_key = findall('\n@.*?{(.*?),',entry)[0]
    gdict2[this_key] = entry
    if 'XXX' in this_key or 'xxx' in this_key or 'submitted' in this_key or this_type.lower() in ['language', 'set','customa','customb', 'lecture', "preprint"] or 'sole' in this_key or 'lingpy' in this_key or this_key[-1] not in '0123456789abcdefghijklmn':
        pass
    else:
        this_entry_dict = {}
        for param in parameters:
            param = param.lower()
            try:
                result = findall("  *" + param + '\s*= {(.*?)},*\n',entry, DOTALL)[0]
            except:
                try:
                    result = findall("  *" + param + '\s*= {(.*?)},*\n',
                            entry, DOTALL)[0]
                except:
                    result = ''
            if result != '':
                if param == 'crossref':
                    try:
                        for p, v in globaldict[result].items():
                            if p not in this_entry_dict:
                                this_entry_dict[p] = v
                    except:
                        print(result, 'is missing')
                    #try:
                    #    tmp_title = globaldict[result]['maintitle']
                    #except:
                    #    try:
                    #        tmp_title = globaldict[result]['mainbooktitle']
                    #    except:
                    #        try:
                    #            tmp_title = globaldict[result]['booktitle']
                    #        except:
                    #            tmp_title = "Unknown Booktitle"
                    #try:
                    #    this_entry_dict['year'] = globaldict[result]['year']
                    #except:
                    #    pass
                    #
                    ##this_entry_dict[param] = 'http://lingulist.de/evobib/'.format(result,tmp_title)
                else:
                    this_entry_dict[param] = result.replace('\n',' ').replace('}','').replace('{','').replace('\t',' ').replace('  ',' ')

                    if param == 'doi' and param in this_entry_dict:
                        if not this_entry_dict[param].startswith('http'):
                            this_entry_dict[param] = 'https://doi.org/'+this_entry_dict[param]
        if len(this_entry_dict) > 1:
            if 'userb' in this_entry_dict:
                this_entry_dict['title'] += ' '+this_entry_dict['userb']
                del this_entry_dict['userb']
            if 'usera' in this_entry_dict:
                this_entry_dict['title'] += ' ['+this_entry_dict['usera']+']'
                del this_entry_dict['usera']
            if this_type.strip() and this_type not in ['unpublished', 'preprint']:
                etypes.add(this_type)
            bibtex = '@'+converter.get(this_type, this_type)+'{'+this_key+',\n'
            c.execute('insert into bibliography(key,type) values("'+this_key+'","'+converter.get(this_type, this_type)+'");')
            for key in this_entry_dict.keys():
                if key != "crossref":
                    bibtex = bibtex+'    '+key+' = {'+this_entry_dict[key]+'},\n'
                    c.execute('update bibliography set '+key.lower()+' = ? where key = "'+this_key+'";',(this_entry_dict[key],))
                else:
                    bibtex = bibtex+'    '+key+' = {'+globaldict[this_key]['crossref']+'},\n'
                    c.execute('update bibliography set booktitle = ? where key = "'+this_key+'";',(this_entry_dict[key],))
            bibtex = bibtex[:-2] + '\n}\n'
            c.execute('update bibliography set bibtex = ? where key = "'+this_key+'";',(bibtex,))
            count += 1
            bibout.write(bibtex+'\n')
conn.commit()
print("Done, data stored in evobib.sqlite3.")        
print("Currently, there are {0} entryies.".format(count))
bibout.close()
for etype in etypes:
    print(etype)
