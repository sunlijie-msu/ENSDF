import pathlib
raw = pathlib.Path("A36/S36/new/S36_208pb_36s_36sg.ens").read_bytes()
txt = raw.decode("utf-8")
print("CRLF:", raw.count(b"\r\n"), "LF:", raw.count(b"\n"), "len:", len(raw))
for i, l in enumerate(txt.split("\n"), 1):
    print(i, len(l), repr(l))
