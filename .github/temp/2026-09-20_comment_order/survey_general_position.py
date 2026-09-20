"""Survey how adopted ENSDF files order cL identifiers relative to a general
(no-identifier) comment, i.e. whether general comments precede or follow
identifier-bearing comments such as MOMM1$/MOME2$/BE2$/Q$.
"""
import glob
import re
import sys

sys.path.insert(0, __file__.rsplit("\\", 1)[0])
from check_order import parse  # noqa: E402


def main():
    files = glob.glob("**/*_adopted.ens", recursive=True)
    counts = {}
    examples = {}
    for f in files:
        try:
            blocks = parse(f)
        except Exception:
            continue
        for b in blocks:
            if b["kind"] != "cL":
                continue
            idents = [u["ident"] for u in b["units"]]
            has_gen = any(i is None or i == "" for i in idents)
            has_ident = any(i not in (None, "") for i in idents)
            if not (has_gen and has_ident):
                continue
            first_gen = min(k for k, i in enumerate(idents) if i is None or i == "")
            last_ident = max(k for k, i in enumerate(idents) if i not in (None, ""))
            key = "general_first" if first_gen < last_ident else "general_last"
            counts[key] = counts.get(key, 0) + 1
            examples.setdefault(key, []).append((f, b["start"], idents))
    print(counts)
    for k, v in examples.items():
        print("\n--", k)
        for f, s, idents in v[:12]:
            print("  %-60s %5d %s" % (f, s, idents))


if __name__ == "__main__":
    main()
