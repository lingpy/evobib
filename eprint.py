from tqdm import tqdm

with open("evobib-seminar.bib", "w") as f:
    pass
with open("evobib.bib") as f, open("evobib-seminar.bib", "a") as f2:
    inbr = False
    eprints = {}
    entry = []
    for row in tqdm(f):
        if row[0] == '@':
            inbr = True
            eprints = {}
            entry = []
            out = ""
        elif row[0] == '}':
            inbr = False
            for row in entry:
                out += row
            if "doi" in eprints:
                out += "  eprint = {" + eprints["doi"]
                out += "  eprinttype = {DOI},\n"
            elif "url" in eprints:
                out += "  eprint = {" + eprints["url"]
                out += "  eprinttype = {URL},\n"
            out += "\n}\n\n"
            f2.write(out)


        if inbr:
            try:
                this_row = row.split()[0].strip()
            except:
                pass
            if this_row == "eprint" or this_row == "eprinttype":
                pass
            elif this_row == "url":
                url = row.split("{")[1]
                eprints["url"] = url
            elif this_row == "doi":
                url = row.split("{")[1]
                if not url.startswith("http"):
                    url = "https://doi.org/" + url
                eprints["doi"] = url
            else:
                if this_row == "date":
                    name, date = row.split("=")
                    date = date[1:-1]
                    if "-" in date:
                        entry += [row.replace("date", "pubdate")]
                    else:
                        entry += [row.replace("date", "year")]
                else:
                    entry += [row]
#with open("evobib-seminar.bib", "w") as f:
#    f.write(out)
