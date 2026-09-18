"""Measure @ positions on the 11 R2-batch1 lines."""
raw = open(r"A34/S34/new/S34_adopted.ens", encoding="utf-8", newline="").read().replace("\r\n", "\n")
targets = [("7282", 36), ("8458", 24), ("8496", 25), ("10623", 34), ("8639", 45),
           ("10766", 31), ("8802", 51), ("8865", 51), ("7783", 24), ("8959", 24), ("11086", 34)]
for g, clen in targets:
    for ln in raw.split("\n"):
        if ln.startswith(" 34S   G " + g + " ") and len(ln) >= 76 and ("@" in ln or (g in ("10623", "8639", "10766", "8802", "8865", "11086") and ln[76:77] in ("@", " "))):
            if "@" in ln:
                i = ln.index("@")
                print(f"G {g}: @ idx={i}  rendered run={i - clen}  expected run={76 - clen}  len={len(ln)}")
            else:
                print(f"G {g}: no @  col77={ln[76]!r} len={len(ln)}")
            break
