path = 'A34/Al34/new/Al34_adopted.ens'
with open(path, encoding='utf-8') as fh:
    content = fh.read()

old = (
' 34AL cL J$4-, 5- from g factor measurement (2008Hi01).                         \n'
' 34AL cL T$unweighted average of 53.73 ms {I13} in U(p,{+34}Al) from 2019Li41 by\n'
' 34AL2cL fitting time distribution gated on 929|g in {+34}Si, 51.5 ms {I9} in   \n'
' 34AL3cL {+9}Be({+40}Ar,{+34}Al) from 2017Ha23 and 2017Ha34 by fitting          \n'
' 34AL4cL implant-|b-929|g decay curve, 54.4 ms {I5} in {+9}Be({+36}S,{+34}Al)   \n'
' 34AL5cL from 2012Ro25 by fitting |b decay curve in coincidence with 926-keV    \n'
' 34AL6cL |b-delayed |g in {+34}Si, 56.3 ms {I5} in U(p,{+34}Al) from 2001Nu01 by\n'
' 34AL7cL |b and |g counting rates. Others: 50 ms {I25} (1986Du07), 70 ms {I25}  \n'
' 34AL8cL (1988Mu08), and 42 ms {I6} (1995ReZZ).                                 \n'
' 34AL  L 46.56     11 1+               16.6 MS   8\n'
)

new = (
' 34AL cL J$4-, 5- from g factor measurement (2008Hi01).                         \n'
' 34AL cL T$54.4 ms {I5} in {+9}Be({+36}S,{+34}Al) from 2012Ro25 with fit of |b\n'
' 34AL2cL decay curve in coincidence with 926-keV |b-delayed |g in {+34}Si.\n'
' 34AL3cL 51.5 ms {I9} in {+9}Be({+40}Ar,{+34}Al) from 2017Ha23, 2017Ha34 with\n'
' 34AL4cL fit of implant-|b-929|g decay curve. 53.73 ms {I13} in U(p,{+34}Al)\n'
' 34AL5cL from 2019Li41 with fit of time distribution gated on 929|g in {+34}Si.\n'
' 34AL6cL 56.3 ms {I5} in U(p,{+34}Al) from 2001Nu01 with |b multiscaling and\n'
' 34AL7cL |g counting. Others: 50 ms {I25} (1986Du07), 70 ms {I25} (1988Mu08),\n'
' 34AL8cL and 42 ms {I6} (1995ReZZ).\n'
' 34AL  L 46.56     11 1+               16.6 MS   8\n'
)

if old in content:
    content2 = content.replace(old, new, 1)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(content2)
    print('SUCCESS: replacement applied')
else:
    print('ERROR: old string not found')
    # Find where J$ comment is
    j = content.find(' 34AL cL J$4-')
    if j >= 0:
        print('J$ found at char', j)
        print(repr(content[j:j+600]))
