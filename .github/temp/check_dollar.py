# -*- coding: utf-8 -*-
f = open('.github/temp/replacements.json', encoding='latin-1').read()
pos = f.find('34CL cG RI')
print('Around cG RI marker:', repr(f[pos:pos+40]))
