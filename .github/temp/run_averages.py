"""
Run Java_Average.py for all Group A and Group C cases.
Collect Suggested Adopted Result from each run.
"""
import subprocess, sys, re

cases = [
    # Group A
    {"id": "A1", "level": 2157.9, "gamma": "927.6",   "args": ["9.1","1.5","8.54","0.31","19","6"],
     "src1": "1977Da02", "v1": "9.1", "u1": "15", "src2": "1983Wa27", "v2": "8.54", "u2": "31",
     "v3": "19", "u3": "6"},
    {"id": "A2", "level": 2157.9, "gamma": "2157.8",  "args": ["21.2","1.5","23.8","0.5","38","14"],
     "src1": "1977Da02", "v1": "21.2", "u1": "15", "src2": "1983Wa27", "v2": "23.8", "u2": "5",
     "v3": "38", "u3": "14"},
    {"id": "A3", "level": 3600.28, "gamma": "879.0",  "args": ["98","4","93.9","1.1","85","13"],
     "src1": "1977Da02", "v1": "98", "u1": "4", "src2": "1983Wa27", "v2": "93.9", "u2": "11",
     "v3": "85", "u3": "13"},
    {"id": "A4", "level": 3983.0,  "gamma": "1825.1", "args": ["46.0","3.2","42.3","1.7","72","17"],
     "src1": "1977Da02", "v1": "46.0", "u1": "32", "src2": "1983Wa27", "v2": "42.3", "u2": "17",
     "v3": "72", "u3": "17"},
    # Group C  (Da02 is src1, Gr29 is src2)
    {"id": "C01", "level": 6169.0,  "gamma": "2568.6",  "args": ["23.5","2.4","39","22"],
     "src1": "1977Da02", "v1": "23.5","u1": "24", "v3": "39","u3": "22"},
    {"id": "C02", "level": 6169.0,  "gamma": "2623.8",  "args": ["14.7","7.4","22","11"],
     "src1": "1977Da02", "v1": "14.7","u1": "74", "v3": "22","u3": "11"},
    {"id": "C03", "level": 6169.0,  "gamma": "4938.3",  "args": ["11.8","5.9","17","8"],
     "src1": "1977Da02", "v1": "11.8","u1": "59", "v3": "17","u3": "8"},
    {"id": "C04", "level": 6169.0,  "gamma": "6022.0",  "args": ["74","8","100","17"],
     "src1": "1977Da02", "v1": "74","u1": "8", "v3": "100","u3": "17"},
    {"id": "C05", "level": 6181.27, "gamma": "3600.8",  "args": ["18.2","1.8","17","4"],
     "src1": "1977Da02", "v1": "18.2","u1": "18", "v3": "17","u3": "4"},
    {"id": "C06", "level": 6181.27, "gamma": "4023.1",  "args": ["8.0","4.1","5.7","3.8"],
     "src1": "1977Da02", "v1": "8.0","u1": "41", "v3": "5.7","u3": "38"},
    {"id": "C07", "level": 6181.27, "gamma": "4293.69", "args": ["9.1","4.6","15","4"],
     "src1": "1977Da02", "v1": "9.1","u1": "46", "v3": "15","u3": "4"},
    {"id": "C08", "level": 6181.27, "gamma": "4950.55", "args": ["25.0","25","25","4"],
     "src1": "1977Da02", "v1": "25.0","u1": "25", "v3": "25","u3": "4"},
    {"id": "C09", "level": 6181.27, "gamma": "5719.6",  "args": ["10.2","5.2","11","4"],
     "src1": "1977Da02", "v1": "10.2","u1": "52", "v3": "11","u3": "4"},
    {"id": "C10", "level": 6181.27, "gamma": "6034.3",  "args": ["20.5","2.1","15.1","7.6"],
     "src1": "1977Da02", "v1": "20.5","u1": "21", "v3": "15.1","u3": "76"},
    {"id": "C11", "level": 6207.1,  "gamma": "2224.0",  "args": ["7.3","3.8","26","15"],
     "src1": "1977Da02", "v1": "7.3","u1": "38", "v3": "26","u3": "15"},
    {"id": "C12", "level": 6207.1,  "gamma": "2661.9",  "args": ["48","5","56","17"],
     "src1": "1977Da02", "v1": "48","u1": "5", "v3": "56","u3": "17"},
    {"id": "C13", "level": 6273.3,  "gamma": "4115.1",  "args": ["1.59","0.8","6.2","3.7"],
     "src1": "1977Da02", "v1": "1.59","u1": "80", "v3": "6.2","u3": "37"},
    {"id": "C14", "level": 6273.3,  "gamma": "4385.7",  "args": ["11.1","1.1","11.1","1.3"],
     "src1": "1977Da02", "v1": "11.1","u1": "11", "v3": "11.1","u3": "13"},
    {"id": "C15", "level": 6273.3,  "gamma": "5042.6",  "args": ["0.79","0.4","4.9","1.3"],
     "src1": "1977Da02", "v1": "0.79","u1": "40", "v3": "4.9","u3": "13"},
    {"id": "C16", "level": 6322.0,  "gamma": "3741.5",  "args": ["20.5","2.1","19","7"],
     "src1": "1977Da02", "v1": "20.5","u1": "21", "v3": "19","u3": "7"},
    {"id": "C17", "level": 6322.0,  "gamma": "5656.2",  "args": ["36","4","31","5"],
     "src1": "1977Da02", "v1": "36","u1": "4", "v3": "31","u3": "5"},
    {"id": "C18", "level": 6322.0,  "gamma": "5860.3",  "args": ["18.2","1.8","11.3","3.2"],
     "src1": "1977Da02", "v1": "18.2","u1": "18", "v3": "11.3","u3": "32"},
    {"id": "C19", "level": 6370.2,  "gamma": "3789.7",  "args": ["24.1","2.4","21","5"],
     "src1": "1977Da02", "v1": "24.1","u1": "24", "v3": "21","u3": "5"},
    {"id": "C20", "level": 6370.2,  "gamma": "5139.5",  "args": ["10.3","5.2","11.4","2.3"],
     "src1": "1977Da02", "v1": "10.3","u1": "52", "v3": "11.4","u3": "23"},
    {"id": "C21", "level": 6370.2,  "gamma": "5908.5",  "args": ["31.0","31","22.7","2.3"],
     "src1": "1977Da02", "v1": "31.0","u1": "31", "v3": "22.7","u3": "23"},
    {"id": "C22", "level": 6370.2,  "gamma": "6223.2",  "args": ["48","5","34.1","2.3"],
     "src1": "1977Da02", "v1": "48","u1": "5", "v3": "34.1","u3": "23"},
    {"id": "C23", "level": 6370.2,  "gamma": "6369.6",  "args": ["52","5","39","5"],
     "src1": "1977Da02", "v1": "52","u1": "5", "v3": "39","u3": "5"},
]

script = r".github/scripts/Java_Average.py"

print("=" * 80)
print("JAVA AVERAGE RESULTS")
print("=" * 80)

results = {}
for case in cases:
    cmd = [sys.executable, script] + case["args"]
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        out = e.output

    # Extract "Suggested Adopted Result" line
    sar = None
    weighted = None
    for line in out.splitlines():
        if "Suggested Adopted Result" in line:
            sar = line.strip()
        if "weighted" in line.lower() or "unweighted" in line.lower():
            weighted = line.strip()

    results[case["id"]] = {"sar": sar, "method": weighted, "raw": out}
    print(f"\n{case['id']}  L={case['level']}  G={case['gamma']}")
    print(f"  Input: {' '.join(case['args'])}")
    if sar:
        print(f"  {sar}")
    if weighted:
        print(f"  {weighted}")

print("\n\n--- FULL OUTPUT ---")
for case in cases:
    cid = case["id"]
    if cid in results:
        print(f"\n{'='*50}")
        print(f"{cid}: L={case['level']} G={case['gamma']}")
        print(results[cid]["raw"])
