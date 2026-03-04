import json
import re
import urllib.request
import urllib.error

NNDC_URL = "https://www.nndc.bnl.gov/ensdf/EvaluationIndexServlet"
EXACT_JSON = ".github/temp/exact_dois.json"
OUT_JSON = ".github/temp/doi_metadata_validation.json"


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "mailto:ensdf_admin@example.com"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read().decode("utf-8"))


def normalize_space(text):
    return re.sub(r"\s+", " ", text.strip())


def parse_official(raw):
    raw = normalize_space(raw)
    if raw == "ENSDF":
        return {"kind": "ENSDF", "vol": "", "page": "", "year": ""}

    m = re.search(r"NDS\s*(\d+)\s*,?\s*(\d+)\s*\(?\s*(\d{4})\s*\)?\.?", raw, re.IGNORECASE)
    if m:
        return {"kind": "NDS", "vol": m.group(1), "page": m.group(2), "year": m.group(3)}

    m = re.search(r"NP\s*A?\s*(\d+)\s*,?\s*(\d+)\s*\(?\s*(\d{4})\s*\)?\.?", raw, re.IGNORECASE)
    if m:
        return {"kind": "NPA", "vol": m.group(1), "page": m.group(2), "year": m.group(3)}

    m = re.search(r"NDS\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d{4})", raw, re.IGNORECASE)
    if m:
        return {"kind": "NDS", "vol": m.group(1), "page": m.group(2), "year": m.group(3)}

    return {"kind": "UNKNOWN", "vol": "", "page": "", "year": ""}


def crossref_meta(doi):
    url = f"https://api.crossref.org/works/{doi}"
    req = urllib.request.Request(url, headers={"User-Agent": "mailto:ensdf_admin@example.com"})
    with urllib.request.urlopen(req, timeout=30) as r:
        item = json.loads(r.read().decode("utf-8")).get("message", {})

    journal = ""
    container = item.get("container-title", [])
    if container:
        journal = container[0]

    vol = str(item.get("volume", "") or "")
    page = str(item.get("page", "") or "")
    year = ""

    for key in ("published-print", "published-online", "issued"):
        val = item.get(key, {})
        parts = val.get("date-parts", []) if isinstance(val, dict) else []
        if parts and parts[0]:
            year = str(parts[0][0])
            break

    return {
        "journal": journal,
        "volume": vol,
        "page": page,
        "year": year,
        "title": (item.get("title", [""])[0] if item.get("title") else ""),
    }


def page_matches(cr_page, off_page):
    if not off_page:
        return True
    if not cr_page:
        return False
    first = cr_page.split("-")[0].strip()
    return first == off_page


def year_matches(cr_year, off_year):
    return (not off_year) or (cr_year == off_year)


def journal_matches(cr_journal, kind):
    text = (cr_journal or "").lower()
    if kind == "NDS":
        return "nuclear data sheets" in text
    if kind == "NPA":
        return "nuclear physics a" in text
    return True


def main():
    official_raw = fetch_json(NNDC_URL)
    official = {item["a"]: parse_official(item.get("citation", "")) for item in official_raw if item.get("type") == "MASS"}

    with open(EXACT_JSON, "r", encoding="utf-8") as f:
        exact = json.load(f)

    report = {
        "summary": {
            "checked": 0,
            "skipped_no_doi": 0,
            "meta_fetch_fail": 0,
            "journal_mismatch": [],
            "volume_mismatch": [],
            "page_mismatch": [],
            "year_mismatch": [],
        },
        "details": []
    }

    for a in sorted(official.keys()):
        key = str(a)
        if key not in exact:
            continue

        doi = (exact[key].get("doi") or "").strip()
        off = official[a]

        if off["kind"] == "ENSDF":
            continue

        if not doi:
            report["summary"]["skipped_no_doi"] += 1
            continue

        report["summary"]["checked"] += 1

        detail = {
            "a": a,
            "doi": doi,
            "official": off,
            "crossref": {},
            "journal_ok": None,
            "volume_ok": None,
            "page_ok": None,
            "year_ok": None,
            "error": "",
        }

        try:
            cr = crossref_meta(doi)
            detail["crossref"] = cr

            detail["journal_ok"] = journal_matches(cr["journal"], off["kind"])
            detail["volume_ok"] = (not off["vol"]) or (cr["volume"] == off["vol"])
            detail["page_ok"] = page_matches(cr["page"], off["page"])
            detail["year_ok"] = year_matches(cr["year"], off["year"])

            if not detail["journal_ok"]:
                report["summary"]["journal_mismatch"].append(a)
            if not detail["volume_ok"]:
                report["summary"]["volume_mismatch"].append(a)
            if not detail["page_ok"]:
                report["summary"]["page_mismatch"].append(a)
            if not detail["year_ok"]:
                report["summary"]["year_mismatch"].append(a)

        except Exception as e:
            report["summary"]["meta_fetch_fail"] += 1
            detail["error"] = str(e)

        report["details"].append(detail)

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    s = report["summary"]
    print("checked:", s["checked"])
    print("meta_fetch_fail:", s["meta_fetch_fail"])
    print("journal_mismatch:", len(s["journal_mismatch"]))
    print("volume_mismatch:", len(s["volume_mismatch"]))
    print("page_mismatch:", len(s["page_mismatch"]))
    print("year_mismatch:", len(s["year_mismatch"]))


if __name__ == "__main__":
    main()
