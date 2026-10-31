for p in [r"A60/A60_13NDS.ens", r"A75/A75_13NDS.ens",
          r"XUNDL/A58/Ni58/new/Ni58_adopted.ens",
          r"XUNDL/A58/Fe58/new/Fe58_adopted.ens"]:
    for l in open(p, encoding="utf-8", errors="replace"):
        l = l.rstrip("\n").ljust(80)
        if l[5] == " " and l[6] == " " and l[7] == "Q":
            print(p)
            print("  10-19", repr(l[9:19]), " 20-21", repr(l[19:21]), " 22-29", repr(l[21:29]),
                  " 30-31", repr(l[29:31]))
            print("  32-39", repr(l[31:39]), " 40-41", repr(l[39:41]), " 42-49", repr(l[41:49]),
                  " 50-51", repr(l[49:51]))
            print("  52-59", repr(l[51:59]), " 60-61", repr(l[59:61]), " 62-79", repr(l[61:79]))
            break
