import json
import re

with open('.github/temp/nndc_citations.json') as f:
    data = json.load(f)

unmatched = []
def parse_cit(cit):
    if cit.strip() == "ENSDF":
       return "ENSDF", None, None, None
    
    # NDS
    m_nds = re.match(r'NDS\s+(\d+)\s*[,]*\s*(\d+)\s*\((\d+)\)', cit)
    if m_nds:
       return "Nuclear Data Sheets", m_nds.group(1), m_nds.group(2), m_nds.group(3)
       
    # NP
    m_np = re.match(r'NP\s+A\s*(\d+)\s*[,]*\s*(\d+)\s*\((\d+)\)', cit)
    if m_np:
       return "Nuclear Physics A", m_np.group(1), m_np.group(2), m_np.group(3)

    return None, None, None, None

for a, cit in data.items():
    res = parse_cit(cit)
    if res[0] is None:
        unmatched.append((a, cit))

for u in unmatched:
    print(u)
print(f"Matched {len(data)-len(unmatched)} / {len(data)}")
