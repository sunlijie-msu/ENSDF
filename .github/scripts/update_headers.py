#!/usr/bin/env python3
"""Stamp ENSDF headers for a new mass-chain evaluation cycle.

For every .ens file in a `new/` folder (or a single given file):
  1. IDENTIFICATION record (line 1), cols 66-80 -> "ENSDF    <version>";
  2. insert the evaluator `H` record directly after the IDENTIFICATION record and its
     continuation records, leaving legacy H records unchanged;
  3. report unconverted sources (.old/.xundl) still left in `new/`.

NUCID and line length of the written records are validated before writing, and the
file's original end-of-line style is preserved.

Usage:
  python update_headers.py <chain|isotope|file> [--version 202609] [--author "..."]
                                                  [--cut 30-Sep-2026] [--check]
Exit code 1 if a header is malformed, a source is left unconverted, or --check finds work.
"""
import argparse
import os
import re
import sys

DEFAULTS = {"version": "202609", "author": "LIJIE SUN AND JUN CHEN", "cut": "30-Sep-2026"}
NUCID_RE = re.compile(r"^ ?\d{1,3}[A-Z][A-Za-z]? ?$")
SOURCE_EXTS = (".old", ".xundl")


def id_block_end(body):
    """Index just after the IDENTIFICATION record and its continuation records."""
    index = 1
    while index < len(body) and body[index][5:6] != " " and body[index][7:8] == " ":
        index += 1
    return index


def update(filepath, version, author, cut, write):
    """Stamp one file; return (status, message) with status in ok/unchanged/dry/error."""
    with open(filepath, encoding="utf-8", newline="") as stream:
        text = stream.read()

    eol = "\r\n" if "\r\n" in text else "\n"
    trailing_eol = text.endswith(eol)
    body = text.split(eol)
    if trailing_eol:
        body.pop()
    nucid = body[0][:5] if body else ""
    if not NUCID_RE.match(nucid):
        return "error", f"cannot read NUCID from line 1: {nucid!r}"
    if not body[0].isascii():
        return "error", "non-ASCII IDENTIFICATION record"

    id_line = body[0][:65].ljust(65) + f"ENSDF    {version}"
    h_line = f"{nucid}  H TYP=FUL$AUT={author}$CIT=ENSDF$CUT={cut}$".ljust(80)
    actions = []
    if id_line != body[0]:
        body[0] = id_line
        actions.append(f"ID record cols 66-80 -> ENSDF    {version}")
    stop = id_block_end(body)
    if not any(body[i][7:8] == "H" and f"AUT={author}" in body[i] for i in range(1, stop + 1)):
        body.insert(stop, h_line)
        actions.append(f"inserted evaluator H record at line {stop + 1}")
    if not actions:
        return "unchanged", "already updated"
    if any(len(line) != 80 for line in (body[0], h_line)):
        return "error", "refusing to write a malformed header"
    if not write:
        return "dry", "; ".join(actions)

    with open(filepath, "w", encoding="utf-8", newline="") as stream:
        stream.write(eol.join(body) + (eol if trailing_eol else ""))
    return "ok", "; ".join(actions)


def walk_new(path):
    """Yield (filepath, inside_new) for a single file, or for files under any `new/` folder."""
    if os.path.isfile(path):
        yield path, False
        return
    for root, _, names in os.walk(path):
        if os.path.basename(os.path.normpath(root)).lower() == "new":
            for name in sorted(names):
                yield os.path.join(root, name), True


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("path", help="chain folder, isotope folder or single .ens file")
    parser.add_argument("--version", default=DEFAULTS["version"], help="header stamp (default %(default)s)")
    parser.add_argument("--author", default=DEFAULTS["author"], help="H record AUT (default %(default)s)")
    parser.add_argument("--cut", default=DEFAULTS["cut"], help="H record CUT (default %(default)s)")
    parser.add_argument("--check", "--dry-run", action="store_true",
                        help="report what would change without writing")
    args = parser.parse_args()

    counts = {"ok": 0, "dry": 0, "unchanged": 0, "error": 0}
    leftovers = []
    for filepath, in_new in walk_new(args.path):
        ext = os.path.splitext(filepath)[1].lower()
        if in_new and ext in SOURCE_EXTS:
            leftovers.append(filepath)
        elif ext == ".ens":
            try:
                status, message = update(filepath, args.version, args.author, args.cut,
                                         not args.check)
            except OSError as exc:
                status, message = "error", str(exc)
            counts[status] += 1
            print(f"[{status.upper():8s}] {filepath}: {message}")
        elif not in_new:
            print(f"[SKIP    ] {filepath}: not an .ens file")

    for filepath in leftovers:
        print(f"[WARN    ] {filepath}: unconverted source in new/ - convert it to .ens first")

    print("\nSummary: {ok} updated, {dry} need updating, {unchanged} already current, "
          "{error} errors, {unconverted} unconverted sources"
          .format(unconverted=len(leftovers), **counts))
    sys.exit(1 if counts["error"] or leftovers or (args.check and counts["dry"]) else 0)


if __name__ == '__main__':
    main()
