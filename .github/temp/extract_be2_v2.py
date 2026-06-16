"""Extract BE2(DOWN) from ruler.rpt — debug version"""
import re

with open(r'd:\X\ND\Files\ruler.rpt', 'r') as f:
    content = f.read()

# Find all gamma sections (each starts with "--->gamma")
sections = re.split(r'--->gamma', content)
print(f'Total sections: {len(sections)}')

for i, sec in enumerate(sections):
    if i == 0:
        continue  # skip preamble
    eg = re.search(r'EG=([\d.]+)', sec)
    print(f'Sec {i}: EG={eg.group(1) if eg else "N/A"}')
    
    # Find MIN/MAX section
    mm = re.search(r'<2>.*?BE2\(DOWN\)[=>]([\d.>]+)\s*([+-][\d]+-[+-]?[\d]+)?', sec, re.DOTALL)
    if mm:
        print(f'  MIN/MAX: {mm.group(1)} {mm.group(2) or ""}')
    
    # Find MC section
    if 'not suitable' in sec:
        print(f'  MC: not suitable')
    else:
        mc = re.search(r'<3>.*?BE2\(DOWN\)=([\d.]+)\s*([+-][\d]+-[+-]?[\d]+)?', sec, re.DOTALL)
        if mc:
            print(f'  MC: {mc.group(1)} {mc.group(2) or ""}')
        else:
            # Try suggested approach
            sug = re.search(r'suggested.*?BE2DOWN=([\d.]+)\s+([+-][\d]+-[+-]?[\d]+)?', sec, re.DOTALL)
            if sug:
                print(f'  MC(sug): {sug.group(1)} {sug.group(2) or ""}')
    print()
