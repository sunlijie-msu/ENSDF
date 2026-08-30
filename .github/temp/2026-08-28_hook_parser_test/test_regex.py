import re
comment = '34S  cL E$weighted average of: 3305 {I2} (1972Cr08); 3302 {I10} (1963Br05)'
pat = r'(\d+\.?\d*)\s*\{I(\d+)\}\s*\((\d{4}[A-Z]{2}\d{2})\)'
print('comment:', comment)
pairs = re.findall(pat, comment)
print('pairs:', pairs)
# also test simpler
print('simple digit test:', re.findall(r'\{I(\d+)\}', comment))
print('ref test:', re.findall(r'\(\d{4}[A-Z]{2}\d{2}\)', comment))
