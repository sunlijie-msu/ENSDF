"""Check all delete-only G-records to see what existing comments triggered the delete-only classification."""
import json

with open('A34/Cl34/new/Cl34_adopted.ens', 'r') as f:
    lines = f.readlines()

# Target comments for each flag
target_A = 'cG E$From {+32}S({+3}He,p|g)'
target_B = 'cG RI$From {+32}S({+3}He,p|g)'
target_C = 'cG E$From {+24}Mg({+12}C,pn|g)'

# Delete-only ops from JSON analysis:
delete_only = {
    'FLAG=A': ['314.64', '461.00', '1740.2'],
    'FLAG=AB': ['204.58', '519.22', '564.67', '769.25', '1083.9', '1426.7'],
    'FLAG=B': ['1740.2_B', '927.6', '1697.6', '2011.4', '2157.8', '1145.4', '2230.1'],
    'FLAG=C': ['1224.1', '4677.4'],
}

# For each, find the G-record in current file and show comments
def find_g_record(energy_str):
    """Find the G-record with this energy and return surrounding lines."""
    for i, l in enumerate(lines):
        if ('  G ' + energy_str) in l or ('  G ' + energy_str.split('_')[0]) in l:
            if l[0:5].strip():
                return i
    return None

def get_comments_after(pos, n=6):
    result = []
    for j in range(pos, min(len(lines), pos+n+1)):
        result.append((j+1, lines[j].rstrip()))
    return result

print("=== FLAG=A delete-only G-records ===")
for e in delete_only['FLAG=A']:
    pos = find_g_record(e)
    if pos is not None:
        print(f"\nG {e} (line {pos+1}):")
        for lno, txt in get_comments_after(pos, 5):
            print(f"  {lno}: {txt}")
        # Check if exact target E$ is present
        blk = ''.join(l for l in lines[pos:pos+8])
        has_exact = target_A in blk
        print(f"  -> has exact '{target_A}': {has_exact}")

print("\n=== FLAG=AB delete-only G-records ===")
for e in delete_only['FLAG=AB']:
    pos = find_g_record(e)
    if pos is not None:
        blk = ''.join(l for l in lines[pos:pos+10])
        has_A = target_A in blk
        has_B = target_B in blk
        print(f"\nG {e} (line {pos+1}): has exact E$From3He={has_A}, has exact RI$From3He={has_B}")
        for lno, txt in get_comments_after(pos, 6):
            print(f"  {lno}: {txt}")

print("\n=== FLAG=B delete-only G-records ===")
for e in delete_only['FLAG=B']:
    e_clean = e.split('_')[0]
    pos = find_g_record(e_clean)
    if pos is not None:
        blk = ''.join(l for l in lines[pos:pos+8])
        has_B = target_B in blk
        print(f"\nG {e_clean} (line {pos+1}): has exact RI$From3He={has_B}")
        for lno, txt in get_comments_after(pos, 5):
            print(f"  {lno}: {txt}")

print("\n=== FLAG=C delete-only G-records ===")
for e in delete_only['FLAG=C']:
    pos = find_g_record(e)
    if pos is not None:
        blk = ''.join(l for l in lines[pos:pos+8])
        has_C = target_C in blk
        print(f"\nG {e} (line {pos+1}): has exact E$FromMg={has_C}")
        for lno, txt in get_comments_after(pos, 6):
            print(f"  {lno}: {txt}")
