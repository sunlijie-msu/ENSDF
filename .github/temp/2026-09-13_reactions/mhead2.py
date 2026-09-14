import subprocess
head = subprocess.run(["git", "show", "HEAD:A34/S34/new/S34_adopted.ens"],
                      capture_output=True, text=True, encoding="ascii").stdout.split("\n")
cur = open("A34/S34/new/S34_adopted.ens", encoding="ascii").read().split("\n")
for n in range(576, 585):
    print("HEAD %d len=%-3d %r" % (n, len(head[n - 1]), head[n - 1]))
    print("CUR  %d len=%-3d %r" % (n, len(cur[n - 1]), cur[n - 1]))
