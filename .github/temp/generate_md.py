import json

with open('.github/temp/mass_dois.json', 'r') as f:
    data = json.load(f)

with open('ENSDF_Mass_Chain_Evaluations.md', 'w', encoding='utf-8') as f:
    f.write("# ENSDF Mass Chain Evaluations\n\n")
    f.write("| Mass Number | Citation (Volume, Page, Year) | DOI | Authors |\n")
    f.write("|---|---|---|---|\n")
    
    for a in range(1, 300):
        a_str = str(a)
        if a_str in data:
            # list shape: [vol, page, year, doi, auth_str, journal]
            record = data[a_str]
            vol = record[0]
            if vol == "NOT FOUND" or vol == "ERROR":
                f.write(f"| A={a} | Not Found / Error | | |\n")
            else:
                page = record[1]
                year = record[2]
                doi = record[3]
                auth = record[4]
                journal = record[5] if len(record) > 5 else "NDS"
                
                # Format citation based on journal
                if journal == "NPA":
                    citation = f"Nucl. Phys. A {vol}, {page} ({year})"
                else:
                    citation = f"Nucl. Data Sheets {vol}, {page} ({year})"
                
                doi_link = f"[{doi}](https://doi.org/{doi})" if doi and doi != "?" else "N/A"
                
                f.write(f"| {a} | {citation} | {doi_link} | {auth} |\n")
        else:
            f.write(f"| {a} | Not Found | | |\n")

print("Created ENSDF_Mass_Chain_Evaluations.md")
