# ENSDF Comment Cleanup Instructions

## General cG E,RI Comment Strategy

**Principle:** Establish the most common data source as default in a general comment, then document exceptions individually.

### General Comment Format
```
 NUCID cG E,RI$From {DOMINANT_DATASET} unless otherwise noted. E|g values 
 NUCID2cG without uncertainties are deduced from level-energy differences.       
```

### Individual Comment Rules

| Scenario | Action |
|----------|--------|
| E or RI from default dataset only | No individual comment needed |
| E|g without uncertainty | No comment needed (deduced from level difference) |
| Weighted/unweighted average from multiple datasets | Add cG E$ or cG RI$ with average details |
| Value from non-default dataset | Add cG E$ or cG RI$ stating source |
| Other values exist but not used for averaging | Add "other: VALUE from DATASET" |

### Comment Ordering (per ENSDF rules)
```
cG E$ → cG RI$ → cG M$ → cG MR$ → other identifiers
```

### Examples

**Weighted average:**
```
 34AR cG E$weighted average of 1197.5 {I4} from {+12}C({+24}Mg,{+34}Ar|g) and   
 34AR2cG 1196.5 {I4} from {+32}S({+3}He,n|g)                                    
```

**Non-default source with other value:**
```
 34AR cG RI$from {+32}S({+3}He,n|g). Other: 100 from {+12}C({+24}Mg,{+34}Ar|g)  
```

**Non-default source only:**
```
 34AR cG RI$from {+32}S({+3}He,n|g)                                             
```

### What to Avoid

- ❌ Redundant comments restating the default source
- ❌ Individual cG E,RI$ for gammas that match the general comment default
- ❌ Comments for deduced energies (no uncertainty = level difference)

### Checklist

1. Identify dominant dataset for E,RI → use in general comment
2. For each gamma with uncertainty:
   - From default only → no comment
   - From multiple datasets → add average comment
   - From non-default → add source comment with "Other:" if applicable
3. Remove any redundant comments matching the default
