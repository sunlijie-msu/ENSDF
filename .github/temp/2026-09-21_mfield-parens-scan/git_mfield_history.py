"""Read-only: find commits that changed G-record M field (cols 33-41) in S34_adopted.ens."""
import re
import subprocess

REPO = r"d:\X\ND\ENSDF"
PATH = "A34/S34/new/S34_adopted.ens"


def mfield(s):
    return s[32:41].strip() if len(s) >= 41 else ""


def main():
    log = subprocess.run(["git", "--no-pager", "log", "-p", "--unified=0",
                          "--format=%h|%ad|%s", "--date=short", "--", PATH],
                         cwd=REPO, capture_output=True).stdout.decode("utf-8",
                         "replace").split("\n")
    commit = None
    pending = []   # removed lines
    for s in log:
        if re.match(r"^[0-9a-f]{7,}\|", s):
            commit = s
            continue
        if s.startswith("---") or s.startswith("+++"):
            continue
        if s.startswith("-"):
            body = s[1:]
            if len(body) > 8 and body[7:8] == "G" and body[6:7] != "c":
                pending.append(body)
        elif s.startswith("+"):
            body = s[1:]
            if len(body) > 8 and body[7:8] == "G" and body[6:7] != "c":
                # match by energy (cols 10-19) against pending
                e = body[9:19].strip()
                old = None
                for o in pending:
                    if o[9:19].strip() == e:
                        old = o
                        break
                if old is not None and mfield(old) != mfield(body):
                    print("%-9s E=%-10s M: %-11s -> %-11s" %
                          (commit.split("|")[0], e, mfield(old), mfield(body)))
                    print("          %s" % commit.split("|", 2)[2][:70])
                pending = []
            else:
                pending = []
        else:
            pending = []


main()
