"""Verify BOTH old and new literals for the 10447 removal before sending."""
P = r"A34/S34/new/S34_adopted.ens"
raw = open(P, encoding="utf-8", newline="").read().replace("\r\n", "\n")
SUF = "\n 34S X L XREF=L         "

OLD = " 34S   L 10447     5                                                        A   " + SUF
NEW = " 34S   L 10447     5                                                            " + SUF

for tag, S in (("OLD", OLD), ("NEW", NEW)):
    print(f"{tag}: len={len(S)} count={raw.count(S)}")
    print(f"   head={S[:22]!r}")
    print(f"   tail={S[-40:]!r}")
