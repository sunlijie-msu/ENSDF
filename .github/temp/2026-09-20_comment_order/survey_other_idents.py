"""Survey position of 'other' cL identifiers (MOMM1/MOME2/BE2/Q/...) relative to
T$/S$ and to general (no-identifier) comments across all adopted files."""
import glob
import sys

sys.path.insert(0, __file__.rsplit("\\", 1)[0])
from check_order import parse  # noqa: E402

OTHER = ("MOMM1", "MOME2", "BE2", "QE2", "Q", "S")


def main():
    files = sorted(glob.glob("**/*_adopted.ens", recursive=True))
    seq_count = {}
    for f in files:
        try:
            blocks = parse(f)
        except Exception:
            continue
        for b in blocks:
            if b["kind"] != "cL":
                continue
            idents = [u["ident"] for u in b["units"]]
            toks = [i if i else "(gen)" for i in idents]
            others = [i for i in idents if i and i.upper().startswith(OTHER)]
            if not others:
                continue
            key = tuple(toks)
            seq_count[key] = seq_count.get(key, 0) + 1
    for k, v in sorted(seq_count.items(), key=lambda kv: -kv[1])[:60]:
        print("%3d  %s" % (v, list(k)))


if __name__ == "__main__":
    main()
