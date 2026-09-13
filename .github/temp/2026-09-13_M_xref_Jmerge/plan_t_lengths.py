"""Compute exact lengths/pads for planned standardized cL T$ comment lines (read-only)."""

PLANNED = {
    "6121.56": " 34S  cL T$lifetime |t<75 fs in {+31}P(|a,p|g) from 1972Jo10 with DSAM.",
    "6342.52": " 34S  cL T$lifetime |t<36 fs in {+31}P(|a,p|g) from 1972Jo10 with DSAM.",
    "6421.34": " 34S  cL T$lifetime |t<10 fs in {+31}P(|a,p|g) from 1972Jo10 with DSAM.",
    "6639": " 34S  cL T$lifetime |t=60 fs {I15} in {+31}P(|a,p|g) from 1977GrZH with DSAM.",
    "6742": " 34S  cL T$lifetime |t<10 fs in {+31}P(|a,p|g) from 1972Jo10 with DSAM.",
    "6828.83": " 34S  cL T$lifetime |t<67 fs in {+31}P(|a,p|g) from 1972Jo10 with DSAM.",
    "6890": " 34S  cL T$lifetime |t<20 fs in {+31}P(|a,p|g) from 1977GrZH with DSAM.",
    "7110": " 34S  cL T$lifetime |t<10 fs in {+31}P(|a,p|g) from 1972Jo10 with DSAM.",
    "7629.907": " 34S  cL T$lifetime |t=20 fs {I10} in {+31}P(|a,p|g) from 1977GrZH with DSAM.",
    "8503.6": " 34S  cL T$lifetime |t=40 fs {I10} in {+31}P(|a,p|g) from 1977GrZH with DSAM.",
}


def main():
    for key, text in PLANNED.items():
        n = len(text)
        print("%-10s len=%2d pad=%2d" % (key, n, 80 - n), repr(text))


if __name__ == "__main__":
    main()
