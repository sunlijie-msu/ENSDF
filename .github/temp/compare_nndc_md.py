"""
Parse NNDC EvaluationIndexServlet JSON and compare against ENSDF_Mass_Chain_Evaluations.md.
Output: all mismatches between NNDC ground truth and our markdown.
"""

import json
import re
from pathlib import Path

# ── 1. NNDC raw data (copy-pasted from fetched JSON) ─────────────────────────
NNDC_RAW = """
[{"type":"MASS","a":1,"citation":"NDS 106, 601 (2005)"},
{"type":"MASS","a":2,"citation":"ENSDF"},
{"type":"MASS","a":3,"citation":"NDS 130 1 (2015)"},
{"type":"MASS","a":4,"citation":"NP A541 1 (1992)"},
{"type":"MASS","a":5,"citation":"NP A708,3 (2002)"},
{"type":"MASS","a":6,"citation":"NP A708, 3 (2002)"},
{"type":"MASS","a":7,"citation":"NP A708, 3 (2002)"},
{"type":"MASS","a":8,"citation":"NP A745, 155 (2004)"},
{"type":"MASS","a":9,"citation":"NP A745 155 (2004)"},
{"type":"MASS","a":10,"citation":"NP A745 155 (2004)"},
{"type":"MASS","a":11,"citation":"NP A880, 88 (2012)"},
{"type":"MASS","a":12,"citation":"NP A968, 71 (2017)"},
{"type":"MASS","a":13,"citation":"NDS 198, 1 (2024)"},
{"type":"MASS","a":14,"citation":"NP A523,1 (1991)"},
{"type":"MASS","a":15,"citation":"NP A523,1 (1991)"},
{"type":"MASS","a":16,"citation":"NP 564 1 (1993)"},
{"type":"MASS","a":17,"citation":"NP A564, 1 (1993)"},
{"type":"MASS","a":18,"citation":"NP A595, 1 (1995)"},
{"type":"MASS","a":19,"citation":"NP A595, 1 (1995)"},
{"type":"MASS","a":20,"citation":"NP A636, 249 (1998)"},
{"type":"MASS","a":21,"citation":"NDS 127, 1 (2015)"},
{"type":"MASS","a":22,"citation":"NDS 127, 69(2015)"},
{"type":"MASS","a":23,"citation":"NDS 171, 1 (2021)"},
{"type":"MASS","a":24,"citation":"NDS 186, 2 (2022)"},
{"type":"MASS","a":25,"citation":"NDS 205, 1 (2025)"},
{"type":"MASS","a":26,"citation":"NDS 134, 1 (2016)"},
{"type":"MASS","a":27,"citation":"NDS 112, 1875 (2011)"},
{"type":"MASS","a":28,"citation":"NDS 114, 1189 (2013)"},
{"type":"MASS","a":29,"citation":"NDS 113, 909 (2012)"},
{"type":"MASS","a":30,"citation":"NDS 197, 1 (2024)"},
{"type":"MASS","a":31,"citation":"NDS 184, 29 (2022)"},
{"type":"MASS","a":32,"citation":"NDS 201, 1 (2025)"},
{"type":"MASS","a":33,"citation":"NDS 199, 1 (2025)"},
{"type":"MASS","a":34,"citation":"NDS 113, 1563 (2012)"},
{"type":"MASS","a":35,"citation":"NDS 112,2715 (2011)"},
{"type":"MASS","a":36,"citation":"NDS 113, 1 (2012)"},
{"type":"MASS","a":37,"citation":"NDS 113, 365 (2012)"},
{"type":"MASS","a":38,"citation":"NDS 152, 1 (2018)"},
{"type":"MASS","a":39,"citation":"NDS 149, 1 (2018)"},
{"type":"MASS","a":40,"citation":"NDS 140, 1 (2017)"},
{"type":"MASS","a":41,"citation":"NDS 133, 1 (2016)"},
{"type":"MASS","a":42,"citation":"NDS 135, 1 (2016)"},
{"type":"MASS","a":43,"citation":"NDS 126, 1 (2015)"},
{"type":"MASS","a":44,"citation":"NDS 190, 1 (2023)"},
{"type":"MASS","a":45,"citation":"NDS 109, 171 (2008)"},
{"type":"MASS","a":46,"citation":"NDS 91, 1 (2000)"},
{"type":"MASS","a":47,"citation":"NDS 203, 1 (2025)"},
{"type":"MASS","a":48,"citation":"NDS 179, 1 (2022)"},
{"type":"MASS","a":49,"citation":"NDS 109, 1879 (2008)"},
{"type":"MASS","a":50,"citation":"NDS 157, 1 (2019)"},
{"type":"MASS","a":51,"citation":"NDS 144, 1 (2017)"},
{"type":"MASS","a":52,"citation":"NDS 128, 185 (2015)"},
{"type":"MASS","a":53,"citation":"NDS 110,2689 (2009)"},
{"type":"MASS","a":54,"citation":"NDS 121, 1 (2014)"},
{"type":"MASS","a":55,"citation":"NDS 109, 787 (2008)"},
{"type":"MASS","a":56,"citation":"NDS 112, 1513 (2011)"},
{"type":"MASS","a":57,"citation":"NDS 85, 415 (1998)"},
{"type":"MASS","a":58,"citation":"NDS 111, 897 (2010)"},
{"type":"MASS","a":59,"citation":"NDS 151, 1 (2018)"},
{"type":"MASS","a":60,"citation":"NDS 114, 1849 (2013)"},
{"type":"MASS","a":61,"citation":"NDS 125, 1 (2015)"},
{"type":"MASS","a":62,"citation":"NDS 204, 1 (2025)"},
{"type":"MASS","a":63,"citation":"NDS 196, 17 (2024)"},
{"type":"MASS","a":64,"citation":"NDS 178, 41 (2021)."},
{"type":"MASS","a":65,"citation":"NDS 202, 59 (2025)"},
{"type":"MASS","a":66,"citation":"NDS 111, 1093 (2010)"},
{"type":"MASS","a":67,"citation":"NDS 106, 159 (2005)"},
{"type":"MASS","a":68,"citation":"NDS 113, 1735 (2012)"},
{"type":"MASS","a":69,"citation":"NDS 207, 1 (2026)"},
{"type":"MASS","a":70,"citation":"NDS 136, 1 (2016)"},
{"type":"MASS","a":71,"citation":"NDS 188, 1 (2023)"},
{"type":"MASS","a":72,"citation":"NDS 111,1 (2010)"},
{"type":"MASS","a":73,"citation":"NDS 158, 1 (2019)"},
{"type":"MASS","a":74,"citation":"NDS 107, 1923 (2006)"},
{"type":"MASS","a":75,"citation":"NDS 114, 841 (2013)"},
{"type":"MASS","a":76,"citation":"ENSDF"},
{"type":"MASS","a":77,"citation":"ENSDF"},
{"type":"MASS","a":78,"citation":"NDS 110, 1917 (2009)"},
{"type":"MASS","a":79,"citation":"NDS 135, 193 (2016)"},
{"type":"MASS","a":80,"citation":"NDS 105, 223 (2005)"},
{"type":"MASS","a":81,"citation":"NDS 199, 271 (2025)"},
{"type":"MASS","a":82,"citation":"NDS 157, 260 (2019)"},
{"type":"MASS","a":83,"citation":"NDS 125, 201 (2015)"},
{"type":"MASS","a":84,"citation":"NDS 110,2815 (2009)"},
{"type":"MASS","a":85,"citation":"NDS 116, 1 (2014)"},
{"type":"MASS","a":86,"citation":"NDS 203, 283 (2025)"},
{"type":"MASS","a":87,"citation":"NDS 129, 1 (2015)"},
{"type":"MASS","a":88,"citation":"NDS 115, 135 (2014)"},
{"type":"MASS","a":89,"citation":"NDS 114, 1 (2013)"},
{"type":"MASS","a":90,"citation":"NDS 165, 1 (2020)"},
{"type":"MASS","a":91,"citation":"NDS 114, 1293 (2013)"},
{"type":"MASS","a":92,"citation":"NDS 113, 2187 (2012)"},
{"type":"MASS","a":93,"citation":"NDS 112, 1163 (2011)"},
{"type":"MASS","a":94,"citation":"NDS 107, 2423 (2006)"},
{"type":"MASS","a":95,"citation":"NDS 111, 2555 (2010)"},
{"type":"MASS","a":96,"citation":"NDS 109, 2501 (2008)"},
{"type":"MASS","a":97,"citation":"NDS 111, 525 (2010)"},
{"type":"MASS","a":98,"citation":"NDS 164, 1 (2020)"},
{"type":"MASS","a":99,"citation":"NDS 145, 25 (2017)"},
{"type":"MASS","a":100,"citation":"NDS 172, 1 (2021)"},
{"type":"MASS","a":101,"citation":"ENSDF"},
{"type":"MASS","a":102,"citation":"NDS 110, 1745 (2009)"},
{"type":"MASS","a":103,"citation":"NDS 110, 2081 (2009)"},
{"type":"MASS","a":104,"citation":"NDS 108,2035 (2007)"},
{"type":"MASS","a":105,"citation":"NDS 161, 1 (2019)"},
{"type":"MASS","a":106,"citation":"NDS 109, 943 (2008)"},
{"type":"MASS","a":107,"citation":"NDS 109, 1383 (2008)"},
{"type":"MASS","a":108,"citation":"ENSDF"},
{"type":"MASS","a":109,"citation":"NDS 137, 1 (2016)"},
{"type":"MASS","a":110,"citation":"NDS 113, 1315 (2012)"},
{"type":"MASS","a":111,"citation":"NDS 110, 1239 (2009)"},
{"type":"MASS","a":112,"citation":"NDS 124, 157 (2015)"},
{"type":"MASS","a":113,"citation":"NDS 111, 1471 (2010)"},
{"type":"MASS","a":114,"citation":"NDS 113, 515 (2012)"},
{"type":"MASS","a":115,"citation":"NDS 113, 2391 (2012)"},
{"type":"MASS","a":116,"citation":"NDS 111, 717 (2010)"},
{"type":"MASS","a":117,"citation":"ENSDF"},
{"type":"MASS","a":118,"citation":"NDS 75,99 (1995)"},
{"type":"MASS","a":119,"citation":"NDS 110,2945 (2009)"},
{"type":"MASS","a":120,"citation":"NDS 96, 241 (2002)"},
{"type":"MASS","a":121,"citation":"NDS 111, 1619 (2010)"},
{"type":"MASS","a":122,"citation":"NDS 108, 455 (2007)"},
{"type":"MASS","a":123,"citation":"NDS 174, 1 (2021)"},
{"type":"MASS","a":124,"citation":"NDS 109, 1655 (2008)"},
{"type":"MASS","a":125,"citation":"NDS 112, 495 (2011)"},
{"type":"MASS","a":126,"citation":"NDS 180, 1 (2022)"},
{"type":"MASS","a":127,"citation":"NDS 112, 1647 (2011)"},
{"type":"MASS","a":128,"citation":"NDS 129, 191 (2015)"},
{"type":"MASS","a":129,"citation":"NDS 121, 143 (2014)"},
{"type":"MASS","a":130,"citation":"NDS 93, 33 (2001)"},
{"type":"MASS","a":131,"citation":"NDS 107, 2715 (2006)"},
{"type":"MASS","a":132,"citation":"NDS 104, 497 (2005)"},
{"type":"MASS","a":133,"citation":"NDS 112, 855 (2011)"},
{"type":"MASS","a":134,"citation":"NDS 103, 1 (2004)"},
{"type":"MASS","a":135,"citation":"NDS 109, 517 (2008)"},
{"type":"MASS","a":136,"citation":"NDS 152, 331 (2018)"},
{"type":"MASS","a":137,"citation":"NDS 108,2173 (2007)"},
{"type":"MASS","a":138,"citation":"NDS 146, 1 (2017)"},
{"type":"MASS","a":139,"citation":"NDS 138, 1 (2016)"},
{"type":"MASS","a":140,"citation":"NDS 154, 1 (2018)"},
{"type":"MASS","a":141,"citation":"NDS 122, 1 (2014)"},
{"type":"MASS","a":142,"citation":"NDS 112, 1949 (2011)"},
{"type":"MASS","a":143,"citation":"NDS 113, 715 (2012)"},
{"type":"MASS","a":144,"citation":"NDS 93, 599 (2001)"},
{"type":"MASS","a":145,"citation":"NDS 110, 507 (2009)"},
{"type":"MASS","a":146,"citation":"NDS 136, 163 (2016)"},
{"type":"MASS","a":147,"citation":"NDS 181, 1 (2022)"},
{"type":"MASS","a":148,"citation":"NDS 208, 1 (2026)"},
{"type":"MASS","a":149,"citation":"NDS 185, 2 (2022)"},
{"type":"MASS","a":150,"citation":"NDS 114, 435 (2013)"},
{"type":"MASS","a":151,"citation":"NDS 110, 1 (2009)"},
{"type":"MASS","a":152,"citation":"NDS 114, 1497 (2013)"},
{"type":"MASS","a":153,"citation":"NDS 170, 1 (2020)"},
{"type":"MASS","a":154,"citation":"NDS 200, 2 (2025)"},
{"type":"MASS","a":155,"citation":"NDS 160, 1 (2019)"},
{"type":"MASS","a":156,"citation":"NDS 113, 2537 (2012)"},
{"type":"MASS","a":157,"citation":"NDS 132, 1 (2016)"},
{"type":"MASS","a":158,"citation":"NDS 141, 1 (2017)"},
{"type":"MASS","a":159,"citation":"NDS 113, 157 (2012)"},
{"type":"MASS","a":160,"citation":"NDS 176, 1 (2021)"},
{"type":"MASS","a":161,"citation":"NDS 112,2497 (2011)"},
{"type":"MASS","a":162,"citation":"NDS 195, 1 (2024)"},
{"type":"MASS","a":163,"citation":"NDS 111, 1211 (2010)"},
{"type":"MASS","a":164,"citation":"NDS 147, 1 (2018)"},
{"type":"MASS","a":165,"citation":"ENSDF"},
{"type":"MASS","a":166,"citation":"NDS 109, 1103 (2008)"},
{"type":"MASS","a":167,"citation":"NDS 191, 1 (2023)"},
{"type":"MASS","a":168,"citation":"NDS 111, 1807 (2010)"},
{"type":"MASS","a":169,"citation":"NDS 109, 2033 (2008)"},
{"type":"MASS","a":170,"citation":"NDS 153, 1 (2018)"},
{"type":"MASS","a":171,"citation":"NDS 151, 334 (2018)"},
{"type":"MASS","a":172,"citation":"NDS 75,199 (1995)"},
{"type":"MASS","a":173,"citation":"NDS 75,377 (1995)"},
{"type":"MASS","a":174,"citation":"NDS 87, 15 (1999)"},
{"type":"MASS","a":175,"citation":"NDS 206, 1 (2025)"},
{"type":"MASS","a":176,"citation":"NDS 107, 791 (2006)"},
{"type":"MASS","a":177,"citation":"NDS 159, 1 (2019)"},
{"type":"MASS","a":178,"citation":"NDS 110, 1473 (2009)"},
{"type":"MASS","a":179,"citation":"NDS 110, 265 (2009)"},
{"type":"MASS","a":180,"citation":"NDS 126, 151 (2015)"},
{"type":"MASS","a":181,"citation":"NDS 106, 367 (2005)"},
{"type":"MASS","a":182,"citation":"NDS 130, 21 (2015)"},
{"type":"MASS","a":183,"citation":"NDS 134, 149 (2016)"},
{"type":"MASS","a":184,"citation":"NDS 111,275 (2010)"},
{"type":"MASS","a":185,"citation":"NDS 106, 619 (2005)"},
{"type":"MASS","a":186,"citation":"NDS 183, 1 (2022)"},
{"type":"MASS","a":187,"citation":"NDS 110, 999 (2009)"},
{"type":"MASS","a":188,"citation":"NDS 150, 1 (2018)"},
{"type":"MASS","a":189,"citation":"NDS 142, 1 (2017)"},
{"type":"MASS","a":190,"citation":"NDS 169, 1 (2020)"},
{"type":"MASS","a":191,"citation":"NDS 195, 368 (2024)"},
{"type":"MASS","a":192,"citation":"NDS 113, 1871 (2012)"},
{"type":"MASS","a":193,"citation":"NDS 143, 1 (2017)"},
{"type":"MASS","a":194,"citation":"NDS 177, 1 (2021)"},
{"type":"MASS","a":195,"citation":"NDS 121, 395 (2014)"},
{"type":"MASS","a":196,"citation":"NDS 108, 1093 (2007)"},
{"type":"MASS","a":197,"citation":"NDS 104, 283 (2005)"},
{"type":"MASS","a":198,"citation":"NDS 133, 221 (2016)"},
{"type":"MASS","a":199,"citation":"NDS 108, 79 (2007)"},
{"type":"MASS","a":200,"citation":"NDS 192, 1 (2023)"},
{"type":"MASS","a":201,"citation":"NDS 187, 355 (2023)"},
{"type":"MASS","a":202,"citation":"NDS 196, 342 (2024)"},
{"type":"MASS","a":203,"citation":"NDS 177, 509 (2021)"},
{"type":"MASS","a":204,"citation":"NDS 111,141 (2010)"},
{"type":"MASS","a":205,"citation":"NDS 166, 1 (2020)"},
{"type":"MASS","a":206,"citation":"NDS 201, 346 (2025)"},
{"type":"MASS","a":207,"citation":"NDS 112, 707 (2011)"},
{"type":"MASS","a":208,"citation":"NDS 108,1583 (2007)"},
{"type":"MASS","a":209,"citation":"NDS 126, 373 (2015)"},
{"type":"MASS","a":210,"citation":"NDS 121, 561 (2014)"},
{"type":"MASS","a":211,"citation":"NDS 114, 661 (2013)"},
{"type":"MASS","a":212,"citation":"NDS 168, 117 (2020)"},
{"type":"MASS","a":213,"citation":"NDS 181, 475 (2022)"},
{"type":"MASS","a":214,"citation":"NDS 175, 1 (2021)"},
{"type":"MASS","a":215,"citation":"NDS 114, 2023 (2013)"},
{"type":"MASS","a":216,"citation":"NDS 108, 1057 (2007)"},
{"type":"MASS","a":217,"citation":"NDS 147, 382 (2018)"},
{"type":"MASS","a":218,"citation":"NDS 160, 405 (2019)"},
{"type":"MASS","a":219,"citation":"NDS 175, 1 (2021)"},
{"type":"MASS","a":220,"citation":"NDS 112, 1115 (2011)"},
{"type":"MASS","a":221,"citation":"NDS 108, 883 (2007)"},
{"type":"MASS","a":222,"citation":"NDS 192, 315 (2023)"},
{"type":"MASS","a":223,"citation":"NDS 93, 846 (2001)"},
{"type":"MASS","a":224,"citation":"ENSDF"},
{"type":"MASS","a":225,"citation":"NDS 110, 1409 (2009)"},
{"type":"MASS","a":226,"citation":"NDS 77,433 (1996)"},
{"type":"MASS","a":227,"citation":"NDS 132, 257 (2016)"},
{"type":"MASS","a":228,"citation":"NDS 116, 163 (2014)"},
{"type":"MASS","a":229,"citation":"NDS 208, 397 (2026)"},
{"type":"MASS","a":230,"citation":"NDS 197, 259 (2024)"},
{"type":"MASS","a":231,"citation":"NDS 185, 560 (2022)"},
{"type":"MASS","a":232,"citation":"NDS 107, 2579 (2006)"},
{"type":"MASS","a":233,"citation":"NDS 170, 499 (2020)"},
{"type":"MASS","a":234,"citation":"NDS 207, 351 (2026)"},
{"type":"MASS","a":235,"citation":"NDS 122, 205 (2014)"},
{"type":"MASS","a":236,"citation":"NDS 182, 2 (2022)"},
{"type":"MASS","a":237,"citation":"NDS 107, 3323 (2006)"},
{"type":"MASS","a":238,"citation":"NDS 127, 191 (2015)"},
{"type":"MASS","a":239,"citation":"NDS 122, 293 (2014)"},
{"type":"MASS","a":240,"citation":"NDS 206, 359 (2025)"},
{"type":"MASS","a":241,"citation":"NDS 130, 183 (2015)"},
{"type":"MASS","a":242,"citation":"NDS 186, 261 (2022)"},
{"type":"MASS","a":243,"citation":"NDS 121, 695 (2014)"},
{"type":"MASS","a":244,"citation":"NDS 146, 387 (2017)"},
{"type":"MASS","a":245,"citation":"NDS 189, 1 (2023)"},
{"type":"MASS","a":246,"citation":"NDS 198, 449 (2024)"},
{"type":"MASS","a":247,"citation":"NDS 125, 395 (2015)"},
{"type":"MASS","a":248,"citation":"NDS 204, 374 (2025)"},
{"type":"MASS","a":249,"citation":"NDS 195, 718 (2024)"},
{"type":"MASS","a":250,"citation":"NDS 94,131 (2001)"},
{"type":"MASS","a":251,"citation":"NDS 189, 111 (2023)"},
{"type":"MASS","a":252,"citation":"NDS 172, 543 (2021)"},
{"type":"MASS","a":253,"citation":"NDS 114, 1041 (2013)"},
{"type":"MASS","a":254,"citation":"NDS 156, 1 (2019)"},
{"type":"MASS","a":255,"citation":"NDS 114, 1041 (2013)"},
{"type":"MASS","a":256,"citation":"NDS 141, 327 (2017)"},
{"type":"MASS","a":257,"citation":"NDS 114, 1041 (2013)"},
{"type":"MASS","a":258,"citation":"NDS 144, 297 (2017)"},
{"type":"MASS","a":259,"citation":"NDS 114, 1041 (2013)"},
{"type":"MASS","a":260,"citation":"NDS 87, 301 (1999)"},
{"type":"MASS","a":261,"citation":"NDS 88, 155 (1999)"},
{"type":"MASS","a":262,"citation":"NDS 94, 131 (2001)"},
{"type":"MASS","a":263,"citation":"NDS 88, 155 (1999)"},
{"type":"MASS","a":264,"citation":"NDS 87, 309 (1999)"},
{"type":"MASS","a":265,"citation":"NDS 88, 155 (1999)"},
{"type":"MASS","a":266,"citation":"NDS 156, 70 (2019)"},
{"type":"MASS","a":267,"citation":"NDS 182, 130 (2022)"},
{"type":"MASS","a":268,"citation":"NDS 156, 148 (2019)"},
{"type":"MASS","a":269,"citation":"NDS 182, 167 (2022)"},
{"type":"MASS","a":270,"citation":"NDS 156, 70 (2019)"},
{"type":"MASS","a":271,"citation":"NDS 182, 130 (2022)"},
{"type":"MASS","a":272,"citation":"NDS 156, 148 (2019)"},
{"type":"MASS","a":273,"citation":"NDS 182, 167 (2022)"},
{"type":"MASS","a":274,"citation":"NDS 156, 70 (2019)"},
{"type":"MASS","a":275,"citation":"NDS 182, 130 (2022)"},
{"type":"MASS","a":276,"citation":"NDS 156, 148 (2019)"},
{"type":"MASS","a":277,"citation":"NDS 182, 167 (2022)"},
{"type":"MASS","a":278,"citation":"NDS 156, 70 (2019)"},
{"type":"MASS","a":279,"citation":"NDS 182, 130 (2022)"},
{"type":"MASS","a":280,"citation":"NDS 156, 148 (2019)"},
{"type":"MASS","a":281,"citation":"NDS 182, 167 (2022)"},
{"type":"MASS","a":282,"citation":"NDS 156, 70 (2019)"},
{"type":"MASS","a":283,"citation":"NDS 182, 130 (2022)"},
{"type":"MASS","a":284,"citation":"NDS 156, 148 (2019)"},
{"type":"MASS","a":285,"citation":"NDS 182, 167 (2022)"},
{"type":"MASS","a":286,"citation":"NDS 156, 70 (2019)"},
{"type":"MASS","a":287,"citation":"NDS 182, 130 (2022)"},
{"type":"MASS","a":288,"citation":"NDS 156, 148 (2019)"},
{"type":"MASS","a":289,"citation":"NDS 182, 167 (2022)"},
{"type":"MASS","a":290,"citation":"NDS 156, 70 (2019)"},
{"type":"MASS","a":291,"citation":"NDS 182, 130 (2022)"},
{"type":"MASS","a":292,"citation":"NDS 156, 148 (2019)"},
{"type":"MASS","a":293,"citation":"NDS 182, 167 (2022)"},
{"type":"MASS","a":294,"citation":"NDS 156, 70 (2019)"},
{"type":"MASS","a":298,"citation":"NDS 156, 70 (2019)"}]
"""

# ── 2. Normalise a NNDC citation string to the format used in the markdown ─────
def normalise_nndc(raw):
    """Convert NNDC abbreviation to match markdown citation format.
    Returns (journal_prefix, vol, page, year) tuple for comparison.
    """
    s = raw.strip().rstrip('.')
    if s == "ENSDF":
        return ("ENSDF", "", "", "")
    # NDS vol, page (year)
    m = re.match(r'NDS\s+(\d+)[,\s]+(\d+)\s*\((\d{4})\)', s)
    if m:
        vol, page, year = m.group(1), m.group(2), m.group(3)
        return ("NDS", vol, page, year)
    # NP Axxx vol page (year)  -- NP A or NP (no A)
    m = re.match(r'NP\s+A?(\d+)[,\s]+(\d+)\s*\((\d{4})\)', s)
    if m:
        vol, page, year = m.group(1), m.group(2), m.group(3)
        return ("NPA", vol, page, year)
    return ("UNKNOWN", s, "", "")

def normalise_md(raw):
    """Parse a markdown citation string to the same tuple format."""
    s = raw.strip()
    if not s or s in ('Continuous internal ENSDF', 'Not evaluated', 'Unpublished'):
        return ("ENSDF", "", "", "")
    # Nucl. Data Sheets vol, page (year)
    m = re.search(r'Nucl\.\s*Data\s*Sheets\s+(\d+)[,\s]+(\d+)\s*\((\d{4})\)', s)
    if m:
        return ("NDS", m.group(1), m.group(2), m.group(3))
    # Nucl. Phys. A vol, page (year)
    m = re.search(r'Nucl\.\s*Phys\.\s*A\s+(\d+)[,\s]+(\d+)\s*\((\d{4})\)', s)
    if m:
        return ("NPA", m.group(1), m.group(2), m.group(3))
    return ("UNKNOWN", s, "", "")

# ── 3. Parse NNDC entries ──────────────────────────────────────────────────
nndc = {}
for item in json.loads(NNDC_RAW):
    if item.get('type') == 'MASS':
        a = item['a']
        nndc[a] = normalise_nndc(item['citation'])

# ── 4. Parse Markdown entries ─────────────────────────────────────────────
md_raw = {}
text = Path('ENSDF_Mass_Chain_Evaluations.md').read_text(encoding='utf-8')
for ln in text.splitlines():
    if not ln.startswith('| ') or ln.startswith('|---'):
        continue
    p = [x.strip() for x in ln.strip('|').split('|')]
    if len(p) == 4 and p[0].isdigit():
        a = int(p[0])
        md_raw[a] = {'cite': p[1], 'doi': p[2], 'author': p[3]}

# ── 5. Compare ─────────────────────────────────────────────────────────────
print(f"NNDC mass entries: {len(nndc)}")
print(f"Markdown entries: {len(md_raw)}")
print()

mismatches = []
for a in sorted(nndc.keys()):
    if a not in md_raw:
        print(f"MISSING A={a} in markdown")
        continue
    nndc_t = nndc[a]
    md_t = normalise_md(md_raw[a]['cite'])
    
    if nndc_t[0] == 'ENSDF' and md_t[0] == 'ENSDF':
        continue  # both continuous, OK
    if nndc_t == md_t:
        continue  # exact match
    # Compare as (journal, vol, page, year)
    if nndc_t[0] == md_t[0] and nndc_t[1] == md_t[1] and nndc_t[3] == md_t[3]:
        # page may differ due to range vs first-page
        if nndc_t[2] != md_t[2]:
            # Could be legitimate DOI page range vs first page
            mismatches.append((a, 'PAGE_DIFF', nndc_t, md_t, md_raw[a]['cite']))
    else:
        mismatches.append((a, 'MISMATCH', nndc_t, md_t, md_raw[a]['cite']))

print(f"Total mismatches: {len(mismatches)}")
print()
ENSDF_CHAINS = []
for a in sorted(nndc.keys()):
    if nndc[a][0] == 'ENSDF':
        ENSDF_CHAINS.append(a)
print(f"NNDC ENSDF (continuous/unpublished) chains: {ENSDF_CHAINS}")
print()

for a, kind, nt, mt, md_cite in mismatches:
    print(f"A={a:4d} [{kind}]")
    print(f"  NNDC: {nt}")
    print(f"  MD:   {mt}  (cite='{md_cite}')")
    print()

# Special: markdown has published citations for NNDC-ENSDF entries
print("=== Markdown entries that claim published but NNDC says ENSDF ===")
for a in sorted(nndc.keys()):
    if a not in md_raw: continue
    if nndc[a][0] == 'ENSDF':
        md_t = normalise_md(md_raw[a]['cite'])
        if md_t[0] != 'ENSDF':
            print(f"  A={a}: markdown='{md_raw[a]['cite']}' but NNDC=ENSDF")
