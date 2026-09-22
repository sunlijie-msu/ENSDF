import hashlib
import os
import time

p = r"d:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens"
for i in range(13):
    st = os.stat(p)
    h = hashlib.sha1(open(p, "rb").read()).hexdigest()[:12]
    print(time.strftime("%H:%M:%S"), "size", st.st_size, "mtime", time.strftime("%H:%M:%S", time.localtime(st.st_mtime)), "sha", h)
    time.sleep(5)
