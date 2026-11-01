# Release instructions

- Run eprint.py and eprint-case.py
- Open evobib-case.bib and run clean.vim from vim
- Run bib2py.py
- Take most recent data.sqlite and evobib.sqlite and place them into the server
- Run query.sh to get all quotes from data.sqlite
- add files to git repository
- modify release information in `.zenodo.json` and `README.md`
- make new release
- update website (release information in files with dates, add new sqlite files to server, etc.)
