DB="${1:-data.sqlite3}"

sqlite3 $DB <<EOF
.mode csv 
.headers on

SELECT id, key, quote, page, keywords
FROM quotes
WHERE key != '#summary'
;
EOF
