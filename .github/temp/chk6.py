import pathlib
ls = pathlib.Path(".github/temp/ws_test.txt").read_bytes().decode().split("\n")
for i, l in enumerate(ls):
    print(i + 1, len(l), repr(l))
