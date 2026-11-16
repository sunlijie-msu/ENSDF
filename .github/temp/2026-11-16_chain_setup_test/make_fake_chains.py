#!/usr/bin/env python3
"""Create throwaway fake chains to test setup_chain_folders.py end to end."""

import pathlib

BASE = pathlib.Path(r"D:\X\ND\ENSDF\.github\temp\2026-11-16_chain_setup_test")


def write(path, text="dummy\n"):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


# Happy path: flat chain that must end up in the A60 layout.
write(BASE / "A99" / "A99_cover.new", "cover\n")
write(BASE / "A99" / "Xx99" / "Xx99_adopted.new")
write(BASE / "A99" / "Xx99" / "Xx99_adopted.old")
write(BASE / "A99" / "Xx99" / "Xx99_x_xundl-1.ens")
write(BASE / "A99" / "Xx99" / "Xx99_x_xundl-1.xundl")
write(BASE / "A99" / "Yy99" / "Yy99_decay.new")            # no .old twin
write(BASE / "A99" / "Yy99" / "new" / "Yy99_old_rel.ens")  # already in place
write(BASE / "A99" / "Yy99" / "old" / "Yy99_old_rel.old")

# Conflict path: destination holds different bytes.
write(BASE / "B99" / "Bb99" / "Bb99_c.ens", "different content\n")
write(BASE / "B99" / "Bb99" / "Bb99_c.new", "working version\n")

print("fake chains created under", BASE)
