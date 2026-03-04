import json
import re
import urllib.request
import urllib.error
from urllib.parse import quote

NNDC_URL = "https://www.nndc.bnl.gov/ensdf/EvaluationIndexServlet"
MD_PATH = "ENSDF_Mass_Chain_Evaluations.md"
OUT_PATH = ".github/temp/mass_chain_validation_report.json"


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "mailto:ensdf_admin@example.com"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def normalize_space(text):
    return re.sub(r"\s+", " ", text.strip())


def parse_official_citation(raw):
    raw = normalize_space(raw)
    if raw == "ENSDF":
        return {"kind": "ENSDF", "journal": "ENSDF", "volume": "", "page": "", "year": ""}

    m = re.search(r"NDS\s*(\d+)\s*,?\s*(\d+)\s*\(?\s*(\d{4})\s*\)?\.?", raw, re.IGNORECASE)
    if m:
        return {
            "kind": "NDS",
            "journal": "Nuclear Data Sheets",
            "volume": m.group(1),
            "page": m.group(2),
            "year": m.group(3),
        }

    m = re.search(r"NDS\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d{4})", raw, re.IGNORECASE)
    if m:
        return {
            "kind": "NDS",
            "journal": "Nuclear Data Sheets",
            "volume": m.group(1),
            "page": m.group(2),
            "year": m.group(3),
        }

    m = re.search(r"NP\s*A?\s*(\d+)\s*,?\s*(\d+)\s*\(?\s*(\d{4})\s*\)?\.?", raw, re.IGNORECASE)
    if m:
        return {
            "kind": "NPA",
            "journal": "Nuclear Physics A",
            "volume": m.group(1),
            "page": m.group(2),
            "year": m.group(3),
        }

    return {"kind": "UNKNOWN", "journal": raw, "volume": "", "page": "", "year": ""}


def parse_markdown_row(line):
    if not line.startswith("| "):
        return None
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) != 4:
        return None
    if not cells[0].isdigit():
        return None

    a = int(cells[0])
    citation = cells[1]
    doi_cell = cells[2]
    authors = cells[3]

    doi = ""
    m = re.search(r"\[(.*?)\]\(https?://doi\.org/.*?\)", doi_cell)
    if m:
        doi = m.group(1).strip()

    return {
        "a": a,
        "citation": citation,
        "doi": doi,
        "authors": authors,
        "raw_line": line.rstrip("\n"),
    }


def load_markdown_rows(path):
    rows = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            row = parse_markdown_row(line)
            if row:
                rows[row["a"]] = row
    return rows


def citation_matches(md_citation, official):
    md = normalize_space(md_citation)
    if official["kind"] == "ENSDF":
        return md.lower().startswith("continuous internal ensdf")

    # Accept full journal format but enforce same vol/page/year
    if official["kind"] in ("NDS", "NPA"):
        vol, page, year = official["volume"], official["page"], official["year"]
        return (vol in md) and (page in md) and (f"({year})" in md)

    return False


def doi_accessible(doi):
    if not doi:
        return None, ""
    url = f"https://doi.org/{quote(doi, safe='/().-_')}"
    req = urllib.request.Request(url, headers={"User-Agent": "mailto:ensdf_admin@example.com"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            final_url = r.geturl()
            return True, final_url
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, str(e)


def main():
    official_raw = fetch_json(NNDC_URL)
    official = {item["a"]: item for item in official_raw if item.get("type") == "MASS"}
    md_rows = load_markdown_rows(MD_PATH)

    results = {
        "summary": {
            "official_mass_count": len(official),
            "markdown_mass_count": len(md_rows),
            "missing_in_markdown": [],
            "extra_in_markdown": [],
            "citation_mismatch": [],
            "doi_missing_when_expected": [],
            "doi_access_fail": [],
        },
        "details": [],
    }

    for a in sorted(official.keys()):
        if a not in md_rows:
            results["summary"]["missing_in_markdown"].append(a)
            continue

        row = md_rows[a]
        off = parse_official_citation(official[a].get("citation", ""))

        detail = {
            "a": a,
            "official_citation": official[a].get("citation", ""),
            "markdown_citation": row["citation"],
            "markdown_doi": row["doi"],
            "citation_match": citation_matches(row["citation"], off),
            "doi_accessible": None,
            "doi_access_info": "",
        }

        if not detail["citation_match"]:
            results["summary"]["citation_mismatch"].append(a)

        expects_doi = off["kind"] in ("NDS", "NPA")
        if expects_doi and not row["doi"]:
            results["summary"]["doi_missing_when_expected"].append(a)
        elif row["doi"]:
            ok, info = doi_accessible(row["doi"])
            detail["doi_accessible"] = ok
            detail["doi_access_info"] = info
            if ok is False:
                results["summary"]["doi_access_fail"].append(a)

        results["details"].append(detail)

    for a in sorted(md_rows.keys()):
        if a not in official:
            # 295-299 may be represented as Not evaluated in markdown
            results["summary"]["extra_in_markdown"].append(a)

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    s = results["summary"]
    print("official_mass_count:", s["official_mass_count"])
    print("markdown_mass_count:", s["markdown_mass_count"])
    print("missing_in_markdown:", len(s["missing_in_markdown"]))
    print("extra_in_markdown:", len(s["extra_in_markdown"]))
    print("citation_mismatch:", len(s["citation_mismatch"]))
    print("doi_missing_when_expected:", len(s["doi_missing_when_expected"]))
    print("doi_access_fail:", len(s["doi_access_fail"]))


if __name__ == "__main__":
    main()
