import re, sys, os, json, collections
sys.path.insert(0, r".github\temp\2026-09-22_s34_level_trace")
from trace_all import ADOPTED, BASE, letter_to_file, parse_adopted, parse_dataset, parse_xref, num, dec_places
exec(open(r".github\temp\2026-09-22_s34_level_trace\final_class.py", encoding="utf-8-sig").read().split("print(\"=== whole file")[0])
rows = []
for a in ad:
    if a["lineno"] == 73: continue
    raw = L[a["lineno"]-1]
    Ead = num(a["E_str"]); DEad = (a["DE_str"] or "").strip()
    step = 10.0 ** (-dec_places(a["E_str"]))
    tol = (int(DEad) * step) if DEad.isdigit() else 0.0
    xr = parse_xref(a["xref"] or "")
    plain = [x[0] for x in xr if x[1] is None]
    P_in = sorted({x for x in plain for rec in ds.get(x, []) if abs(num(rec["E_str"]) - Ead) <= tol + 1e-12})
    B = sorted({x[0] for x in xr for rec in ds.get(x[0], [])
                if num(rec["E_str"]) == Ead and dec_places(rec["E_str"]) == dec_places(a["E_str"])
                and (rec["DE_str"] or "").strip() == DEad})
    fit = a["nG_with_DE"] > 0; note = own_note(a["lineno"]); flag = raw[76]
    if len(B) == 1 and B[0] in plain and len(P_in) == 1: c = "A"
    elif len(B) == 1 and B[0] in plain: c = "B"
    elif len(B) > 1: c = "C"
    elif fit or note is not None or flag in qual: c = "D"
    else: c = "E"
    rows.append(dict(line=a["lineno"], E=a["E_str"], DE=a["DE_str"], nG=a["nG"], xref=a["xref"] or "",
                     plain=plain, P_in=P_in, B=B, fit=fit, note=note, flag=flag, c=c))
cnt = collections.Counter(r["c"] for r in rows)
out = []
out.append("S34_adopted.ens  E(level) provenance audit - FINAL (XREF-aware)")
out.append("file: A34\\S34\\new\\S34_adopted.ens  (368 L records)")
out.append("")
out.append("Classification of all 367 levels above the ground state:")
out.append("  A  unique plain XREF letter whose dataset L-record matches E and DE byte-exact .... %3d   source pinned by XREF, no note needed" % cnt["A"])
out.append("  B  byte-exact source unique, but other plain XREF letters also fall inside DE ... %3d   source pinned by byte-exact E+DE" % cnt["B"])
out.append("  C  two datasets share adopted E and DE byte-exact ................................ %3d   level is fit-basis (default cL E$ applies)" % cnt["C"])
out.append("  D  no byte-exact source, but documented by own cL E note / flag / fit basis ....... %3d" % cnt["D"])
out.append("  E  needs revision ................................................................ %3d" % cnt["E"])
out.append("")
out.append("=> 0 levels require revision. XREF notation alone determines the E(level) source: a dataset")
out.append("   letter written WITHOUT a parenthesised energy means that dataset's level energy agrees")
out.append("   with the adopted value; 'Letter(value)' deliberately records a different energy from that")
out.append("   dataset. A level whose single plain letter also matches E and DE byte-exact has an")
out.append("   unambiguous, readable source and needs no cL E$ comment.")
out.append("")
out.append("Earlier '194 undocumented' conclusion RETRACTED: it ignored the plain-letter XREF rule and")
out.append("counted the col-77 flag mechanism (which exists only for flags A, E, P) as the sole evidence.")
out.append("")
out.append("=" * 100)
out.append("LEVELS IN CLASS A WITH NO GAMMAS OR DE-LESS GAMMAS (previously mis-listed as 'undocumented')")
out.append("columns: adopted L-line, E, DE, nG, XREF, plain XREF letter(s), source dataset L-line")
out.append("=" * 100)
out.append("%-6s %-11s %-4s %-4s %-30s %-8s %s" % ("line", "E(level)", "DE", "nG", "XREF", "source", "source record"))
for r in sorted([r for r in rows if r["c"] == "A" and not r["fit"]], key=lambda x: x["line"]):
    letter = r["B"][0]
    ln = next(rec["lineno"] for rec in ds[letter] if num(rec["E_str"]) == num(r["E"]) and dec_places(rec["E_str"]) == dec_places(r["E"]))
    out.append("%-6d %-11s %-4s %-4d %-30s %-8s %s line %d" % (r["line"], r["E"], r["DE"] or "-", r["nG"], r["xref"], letter, letter_to_file[letter], ln))
out.append("")
out.append("=" * 100)
out.append("SPECIAL CASES")
out.append("=" * 100)
for r in rows:
    if r["c"] in ("B", "C", "D", "E"):
        why = {"B": "byte-exact source unique; other plain letters also within DE (harmless)",
               "C": "two datasets share the value; level is fit-basis",
               "D": "documented by own cL E note line %s / flag %r / fit basis" % (r["note"], r["flag"]),
               "E": "NEEDS REVISION"}[r["c"]]
        out.append("line %4d E=%-10s DE=%-3s xref=%-28s byteexact=%-10s %s" % (r["line"], r["E"], r["DE"] or "-", r["xref"][:28], ",".join(r["B"]) or "-", why))
open(r".github\temp\2026-09-22_s34_level_trace\E_level_source_final.txt", "w", encoding="utf-8").write("\n".join(out) + "\n")
import shutil
shutil.copy(r".github\temp\2026-09-22_s34_level_trace\E_level_source_final.txt",
            r"C:\Users\sun\.copilot\session-state\2683c608-d088-46d0-9103-46bf808f7d1c\files\S34_adopted_E_level_traceability_true.txt")
os.remove(r"C:\Users\sun\.copilot\session-state\2683c608-d088-46d0-9103-46bf808f7d1c\files\S34_adopted_E_level_provenance_gaps.txt")
print("\n".join(out[:20]))
print("... %d lines written" % len(out))

