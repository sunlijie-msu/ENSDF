# 1985Ra15 Table V vs S34_ng_E_thermal ENSDF Cross-Check

## Configuration

- Source: `A34/S34/raw/1985RA15_Table_V.md`
- Target: `A34/S34/new/S34_ng_E_thermal.ens`
- Mapping: source Energy/Intensity columns -> target G E/DE and RI/DRI fields
- Matching: numeric gamma energy within +/-0.5 keV; parent level retained and reported
- Check-only: no ENSDF data records modified

## Summary

| Metric | Count |
|---|---:|
| Source rows | 271 |
| Target G records | 349 |
| Matched source rows | 271 |
| Unmatched source rows | 0 |
| Ambiguous energy matches | 9 |
| Unmatched target G records | 78 |
| Matched rows with one or more mismatches | 160 |

## Category Counts

| Category | Count |
|---|---:|
| RI format | 138 |
| RI starts column 22 | 127 |
| RI value | 72 |
| DRI uncertainty | 21 |
| DRI format | 21 |
| E numeric/rounding | 21 |
| E format | 21 |
| DE uncertainty | 20 |
| DE format | 20 |

## Mismatch Details

| Source line | Source E(DE) | Source RI(DRI) | Target line | Parent L E | Target E(DE) | Target RI(DRI) | Categories |
|---:|---|---|---:|---:|---|---|---|
| 12 | `571.7(6)` | `0.08(3)` | 206 | 6251.68 | `571.7(6)` | `.08(3)` | RI format, RI starts column 22 |
| 14 | `612.16(5)` | `0.263(28)` | 72 | 3916.408 | `612.16(5)` | `.26(3)` | RI value, DRI uncertainty, RI format, DRI format, RI starts column 22 |
| 15 | `631.13(6)` | `0.283(31)` | 219 | 6478.770 | `631.13(6)` | `.28(3)` | RI value, DRI uncertainty, RI format, DRI format, RI starts column 22 |
| 22 | `752.30(8)` | `0.222(26)` | 44 | - | `752.30(8)` | `.22(3)` | RI value, DRI uncertainty, RI format, DRI format, RI starts column 22 |
| 25 | `789.1(6)` | `0.39(7)` | 148 | 5679.927 | `789.1(6)` | `.39(7)` | RI format, RI starts column 22 |
| 31 | `941.59(6)` | `0.41(5)` | 246 | 7110.45 | `941.59(6)` | `.41(5)` | RI format, RI starts column 22 |
| 32 | `982.68(9)` | `0.187(27)` | 362 | 9598.41 | `982.68(9)` | `.19(3)` | RI value, DRI uncertainty, RI format, DRI format, RI starts column 22 |
| 33 | `989.08(28)` | `0.079(23)` | 247 | 7110.45 | `989.1(3)` | `0.079(23)` | E numeric/rounding, DE uncertainty, E format, DE format |
| 34 | `1029.23(8)` | `0.32(4)` | 45 | - | `1029.23(8)` | `.32(4)` | RI format, RI starts column 22 |
| 35 | `1035.82(17)` | `0.108(31)` | 46 | - | `1035.82(17)` | `0.11(3)` | RI value, DRI uncertainty, RI format, DRI format |
| 38 | `1113.27(9)` | `0.41(6)` | 118 | 5228.175 | `1113.27(9)` | `.41(6)` | RI format, RI starts column 22 |
| 39 | `1121.33(9)` | `0.35(5)` | 183 | 5998.10 | `1121.33(9)` | `.35(5)` | RI format, RI starts column 22 |
| 41 | `1156.39(7)` | `1.57(18)` | 222 | 6478.770 | `1156.39(7)` | `.57(18)` | RI value, RI format, RI starts column 22 |
| 44 | `1205.05(4)` | `0.61(6)` | 419 | 11417.223 | `1205.05(4)` | `.61(6)` | RI format, RI starts column 22 |
| 46 | `1237.61(5)` | `0.52(6)` | 421 | 11417.223 | `1237.61(5)` | `.52(6)` | RI format, RI starts column 22 |
| 47 | `1244.32(21)` | `0.120(26)` | 340 | 8874.02 | `1244.32(21)` | `0.12(3)` | DRI uncertainty, RI format, DRI format |
| 48 | `1247.92(6)` | `0.59(7)` | 128 | 5322.51 | `1247.92(6)` | `.59(7)` | RI format, RI starts column 22 |
| 49 | `1266.11(5)` | `0.66(7)` | 139 | 5380.99 | `1266.11(5)` | `.66(7)` | RI format, RI starts column 22 |
| 50 | `1274.30(4)` | `1.17(11)` | 239 | 6954.22 | `1274.30(4)` | `.17(11)` | RI value, RI format, RI starts column 22 |
| 51 | `1277.81(18)` | `0.190(26)` | 48 | - | `1277.81(18)` | `0.19(3)` | DRI uncertainty, RI format, DRI format |
| 53 | `1325.22(26)` | `0.33(7)` | 423 | 11417.223 | `1325.2(3)` | `0.33(7)` | E numeric/rounding, DE uncertainty, E format, DE format |
| 55 | `1364.4(4)` | `0.32(9)` | 380 | 10092.23 | `1364.4(4)` | `.32(9)` | RI format, RI starts column 22 |
| 60 | `1479.73(15)` | `0.263(32)` | 195 | 6168.86 | `1479.73(15)` | `0.26(3)` | RI value, DRI uncertainty, RI format, DRI format |
| 62 | `1486.7(8)` | `0.18(5)` | 51 | - | `1486.7(8)` | `.18(5)` | RI format, RI starts column 22 |
| 63 | `1525.39(6)` | `1.13(11)` | 236 | 6847.90 | `1525.39(6)` | `.13(11)` | RI value, RI format, RI starts column 22 |
| 65 | `1562.3(5)` | `0.80(20)` | 204 | 6251.22 | `1562.3(5)` | `.80(20)` | RI format, RI starts column 22 |
| 66 | `1564.8(5)` | `0.91(20)` | 152 | 5679.927 | `1564.8(5)` | `.91(20)` | RI format, RI starts column 22 |
| 67 | `1572.57(5)` | `5.6(6)` | 101 | 4876.839 | `1572.57(5)` | `.6(6)` | RI value, RI format, RI starts column 22 |
| 68 | `1580.50(6)` | `0.66(7)` | 425 | 11417.223 | `1580.50(6)` | `.66(7)` | RI format, RI starts column 22 |
| 71 | `1615.24(10)` | `2.25(27)` | 427 | 11417.223 | `1615.24(10)` | `2.3(3)` | RI value, DRI uncertainty, RI format, DRI format |
| 74 | `1631.641(25)` | `2.88(27)` | 240 | 6954.22 | `1631.641(25)` | `2.9(3)` | RI value, DRI uncertainty, RI format, DRI format |
| 77 | `1739.32(9)` | `0.48(6)` | 216 | 6428.12 | `1739.32(9)` | `.48(6)` | RI format, RI starts column 22 |
| 78 | `1751.431(29)` | `1.44(14)` | 428 | 11417.223 | `1751.43(3)` | `1.44(14)` | E numeric/rounding, DE uncertainty, E format, DE format |
| 79 | `1772.82(4)` | `1.40(14)` | 179 | 5847.53 | `1772.82(4)` | `.40(14)` | RI value, RI format, RI starts column 22 |
| 81 | `1795.28(30)` | `0.19(5)` | 295 | 8138.10 | `1795.3(3)` | `0.19(5)` | E numeric/rounding, DE uncertainty, E format, DE format |
| 84 | `1854.28(4)` | `1.28(13)` | 226 | 6478.770 | `1854.28(4)` | `.28(13)` | RI value, RI format, RI starts column 22 |
| 85 | `1871.04(8)` | `2.04(22)` | 431 | 11417.223 | `1871.04(8)` | `.04(22)` | RI value, RI format, RI starts column 22 |
| 86 | `1887.66(4)` | `1.78(17)` | 52 | - | `1887.66(4)` | `.78(17)` | RI value, RI format, RI starts column 22 |
| 89 | `1947.060(20)` | `29.2(26)` | 78 | 4074.667 | `1947.060(20)` | `29(3)` | RI value, DRI uncertainty, RI format, DRI format |
| 93 | `1984.2(4)` | `0.50(14)` | 54 | - | `1984.2(4)` | `.50(14)` | RI format, RI starts column 22 |
| 94 | `1987.19(3)` | `6.5(7)` | 84 | 4114.813 | `1987.19(3)` | `.5(7)` | RI value, RI format, RI starts column 22 |
| 95 | `1998.3(4)` | `0.14(5)` | 401 | 11024.94 | `1998.3(4)` | `.14(5)` | RI format, RI starts column 22 |
| 96 | `2046.29(5)` | `1.78(18)` | 55 | - | `2046.29(5)` | `.78(18)` | RI value, RI format, RI starts column 22 |
| 98 | `2076.89(8)` | `1.48(16)` | 142 | 5380.99 | `2076.89(8)` | `.48(16)` | RI value, RI format, RI starts column 22 |
| 100 | `2152.41(23)` | `0.17(9)` | 377 | 9933.35 | `2152.41(23)` | `0.17(5)` | DRI uncertainty, DRI format |
| 102 | `2209.10(6)` | `0.86(9)` | 432 | 11417.223 | `2209.10(6)` | `.86(9)` | RI format, RI starts column 22 |
| 104 | `2233.49(4)` | `5.0(5)` | 248 | 7110.45 | `2233.49(4)` | `.0(5)` | RI value, RI format, RI starts column 22 |
| 106 | `2282.17(4)` | `1.70(16)` | 56 | - | `2282.17(4)` | `.70(16)` | RI value, RI format, RI starts column 22 |
| 109 | `2328.8(5)` | `0.14(4)` | 255 | 7219.28 | `2328.8(5)` | `.14(4)` | RI format, RI starts column 22 |
| 111 | `2363.97(8)` | `2.1(11)` | 318 | 8615.74 | `2363.97(8)` | `.1(11)` | RI value, RI format, RI starts column 22 |
| 113 | `2390.82(6)` | `1.33(14)` | 435 | 11417.223 | `2390.82(6)` | `.33(14)` | RI value, RI format, RI starts column 22 |
| 114 | `2404.04(6)` | `1.07(11)` | 227 | 6478.770 | `2404.04(6)` | `.07(11)` | RI value, RI format, RI starts column 22 |
| 115 | `2441.31(4)` | `1.75(17)` | 57 | - | `2441.31(4)` | `.75(17)` | RI value, RI format, RI starts column 22 |
| 117 | `2475.15(4)` | `1.71(17)` | 58 | - | `2475.15(4)` | `.71(17)` | RI value, RI format, RI starts column 22 |
| 121 | `2543.13(9)` | `9.6(9)` | 180 | 5847.53 | `2543.13(10)` | `9.6(9)` | DE uncertainty, DE format |
| 123 | `2561.36(5)` | `3.6(4)` | 94 | 4688.98 | `2561.36(5)` | `.6(4)` | RI value, RI format, RI starts column 22 |
| 124 | `2611.7(4)` | `1.2(3)` | 437 | 11417.223 | `2611.7(4)` | `.2(3)` | RI value, RI format, RI starts column 22 |
| 127 | `2749.24(5)` | `7.0(7)` | 102 | 4876.839 | `2749.24(5)` | `.0(7)` | RI value, RI format, RI starts column 22 |
| 129 | `2762.10(8)` | `3.0(3)` | 111 | 4889.756 | `2762.10(8)` | `.0(3)` | RI value, RI format, RI starts column 22 |
| 130 | `2801.33(5)` | `10.1(10)` | 440 | 11417.223 | `2801.33(5)` | `0.1(10)` | RI value, RI format, RI starts column 22 |
| 131 | `2810.37(3)` | `0.87(13)` | 59 | - | `2810.3(3)` | `.87(13)` | E numeric/rounding, E format, RI format, RI starts column 22 |
| 133 | `2839.3(4)` | `1.00(16)` | 241 | 6954.22 | `2839.3(4)` | `.00(16)` | RI value, RI format, RI starts column 22 |
| 134 | `2843.7(6)` | `0.59(13)` | 391 | 10311.53 | `2843.7(6)` | `.59(13)` | RI format, RI starts column 22 |
| 135 | `2864.56(4)` | `10.9(11)` | 200 | 6168.86 | `2864.56(4)` | `0.9(11)` | RI value, RI format, RI starts column 22 |
| 136 | `2910.28(5)` | `10.0(10)` | 442 | 11417.223 | `2910.28(5)` | `0.0(10)` | RI value, RI format, RI starts column 22 |
| 137 | `2919.7(5)` | `0.43(11)` | 395 | 10650.11 | `2919.7(5)` | `.43(11)` | RI format, RI starts column 22 |
| 138 | `2940.42(31)` | `1.05(15)` | 276 | 7629.907 | `2940.4(3)` | `1.05(15)` | E numeric/rounding, DE uncertainty, E format, DE format |
| 140 | `2989.9(7)` | `0.18(9)` | 372 | 9836.70 | `2989.9(7)` | `.18(9)` | RI format, RI starts column 22 |
| 141 | `2995.8(6)` | `0.37(10)` | 249 | 7110.45 | `2995.8(6)` | `.37(10)` | RI format, RI starts column 22 |
| 142 | `3005.39(5)` | `10.0(10)` | 277 | 7629.907 | `3005.39(5)` | `0.0(10)` | RI value, RI format, RI starts column 22 |
| 144 | `3031.69(8)` | `4.6(6)` | 444 | 11417.223 | `3031.69(8)` | `.6(6)` | RI value, RI format, RI starts column 22 |
| 145 | `3038.18(32)` | `1.27(17)` | 209 | 6342.50 | `3038.2(3)` | `1.27(17)` | E numeric/rounding, DE uncertainty, E format, DE format |
| 146 | `3051.83(26)` | `0.64(12)` | 60 | - | `3051.8(3)` | `0.64(12)` | E numeric/rounding, DE uncertainty, E format, DE format |
| 147 | `3089.53(26)` | `0.56(11)` | 252 | 7164.47 | `3089.5(3)` | `0.56(11)` | E numeric/rounding, DE uncertainty, E format, DE format |
| 150 | `3174.37(5)` | `10.5(10)` | 228 | 6478.770 | `3174.37(5)` | `0.5(10)` | RI value, RI format, RI starts column 22 |
| 151 | `3183.9(7)` | `0.12(8)` | 313 | 8506.77 | `3183.9(7)` | `.12(8)` | RI format, RI starts column 22 |
| 152 | `3194.74(5)` | `7.4(8)` | 131 | 5322.51 | `3194.74(5)` | `.4(8)` | RI value, RI format, RI starts column 22 |
| 153 | `3211.69(9)` | `2.36(23)` | 446 | 11417.223 | `3211.69(9)` | `.36(23)` | RI value, RI format, RI starts column 22 |
| 155 | `3241.9(5)` | `0.36(7)` | 448 | 11417.223 | `3241.9(5)` | `.36(7)` | RI format, RI starts column 22 |
| 156 | `3253.21(6)` | `3.8(4)` | 143 | 5380.99 | `3253.21(6)` | `.8(4)` | RI value, RI format, RI starts column 22 |
| 159 | `3311.6(5)` | `0.62(11)` | 348 | 9158.71 | `3311.6(5)` | `.62(11)` | RI format, RI starts column 22 |
| 162 | `3451.5(9)` | `0.35(10)` | 262 | 7367.42 | `3451.5(9)` | `.35(10)` | RI format, RI starts column 22 |
| 164 | `3500.3(5)` | `0.48(11)` | 332 | 8727.63 | `3500.3(5)` | `.48(11)` | RI format, RI starts column 22 |
| 166 | `3552.08(4)` | `17.34(17)` | 156 | 5679.927 | `3552.08(4)` | `7.34(17)` | RI value, RI format, RI starts column 22 |
| 167 | `3581.2(4)` | `0.37(7)` | 305 | 8205.40 | `3581.2(4)` | `.37(7)` | RI format, RI starts column 22 |
| 168 | `3628.10(4)` | `17.6(16)` | 169 | 5755.875 | `3628.10(4)` | `7.6(16)` | RI value, RI format, RI starts column 22 |
| 169 | `3635.83(8)` | `5.2(6)` | 451 | 11417.223 | `3635.83(8)` | `.2(6)` | RI value, RI format, RI starts column 22 |
| 170 | `3644.8(8)` | `0.48(10)` | 345 | 9026.31 | `3644.8(8)` | `.48(10)` | RI format, RI starts column 22 |
| 171 | `3649.88(12)` | `3.11(31)` | 242 | 6954.22 | `3649.88(12)` | `3.1(3)` | RI value, DRI uncertainty, RI format, DRI format |
| 172 | `3664.8(4)` | `0.47(10)` | 381 | 10092.23 | `3664.8(4)` | `.47(10)` | RI format, RI starts column 22 |
| 176 | `3812.0(5)` | `0.25(6)` | 328 | 8702.35 | `3812.0(5)` | `.25(6)` | RI format, RI starts column 22 |
| 180 | `3990.7(7)` | `0.29(7)` | 320 | 8615.74 | `3990.7(7)` | `.29(7)` | RI format, RI starts column 22 |
| 181 | `3994.8(8)` | `0.25(7)` | 189 | 6121.49 | `3994.8(8)` | `.25(7)` | RI format, RI starts column 22 |
| 184 | `4074.418(20)` | `31.3(29)` | 80 | 4074.667 | `4074.418(20)` | `31(3)` | RI value, DRI uncertainty, RI format, DRI format |
| 185 | `4114.52(4)` | `8.6(9)` | 85 | 4114.813 | `4114.52(4)` | `.6(9)` | RI value, RI format, RI starts column 22 |
| 186 | `4197.69(9)` | `3.0(4)` | 458 | 11417.223 | `4197.69(9)` | `.0(4)` | RI value, RI format, RI starts column 22 |
| 189 | `4306.44(6)` | `8.3(8)` | 460 | 11417.223 | `4306.44(6)` | `.3(8)` | RI value, RI format, RI starts column 22 |
| 190 | `4325.397(30)` | `12.7(12)` | 280 | 7629.907 | `4325.40(3)` | `12.7(12)` | E numeric/rounding, DE uncertainty, E format, DE format |
| 191 | `4350.85(9)` | `6.2(7)` | 229 | 6478.770 | `4350.85(9)` | `.2(7)` | RI value, RI format, RI starts column 22 |
| 192 | `4391.77(29)` | `0.44(9)` | 314 | 8506.77 | `4391.8(3)` | `0.44(9)` | E numeric/rounding, DE uncertainty, E format, DE format |
| 195 | `4532.6(7)` | `0.23(7)` | 386 | 10212.15 | `4532.6(7)` | `.23(7)` | RI format, RI starts column 22 |
| 197 | `4568.9(4)` | `0.30(6)` | 462 | 11417.223 | `4568.9(4)` | `.30(6)` | RI format, RI starts column 22 |
| 198 | `4588.37(26)` | `0.59(10)` | 463 | 11417.223 | `4588.4(3)` | `0.59(10)` | E numeric/rounding, DE uncertainty, E format, DE format |
| 199 | `4624.2(5)` | `0.21(5)` | 92 | 4624.404 | `4624.2(5)` | `.21(5)` | RI format, RI starts column 22 |
| 200 | `4670.1(6)` | `0.11(6)` | 288 | 7974.72 | `4670.1(6)` | `.11(6)` | RI format, RI starts column 22 |
| 202 | `4758.79(27)` | `0.46(8)` | 341 | 8874.02 | `4758.8(3)` | `0.46(8)` | E numeric/rounding, DE uncertainty, E format, DE format |
| 203 | `4799.11(28)` | `0.52(8)` | 342 | 8874.02 | `4799.1(3)` | `0.52(8)` | E numeric/rounding, DE uncertainty, E format, DE format |
| 204 | `4826.0(5)` | `0.11(5)` | 243 | 6954.22 | `4826.0(5)` | `.11(5)` | RI format, RI starts column 22 |
| 205 | `4889.30(8)` | `2.68(26)` | 112 | 4889.756 | `4889.30(8)` | `.7(3)` | RI value, DRI uncertainty, RI format, DRI format, RI starts column 22 |
| 206 | `4903.4(5)` | `0.28(8)` | 402 | 11024.94 | `4903.4(5)` | `.28(8)` | RI format, RI starts column 22 |
| 207 | `4938.06(3)` | `22.2(21)` | 465 | 11417.223 | `4938.06(3)` | `2.2(21)` | RI value, RI format, RI starts column 22 |
| 209 | `4988.6(4)` | `0.63(9)` | 392 | 10311.53 | `4988.6(4)` | `.63(9)` | RI format, RI starts column 22 |
| 210 | `5036.4(7)` | `0.25(6)` | 253 | 7164.47 | `5036.4(7)` | `.25(6)` | RI format, RI starts column 22 |
| 211 | `5043.3(4)` | `1.59(26)` | 349 | 9158.71 | `5043.3(4)` | `.6(3)` | RI value, DRI uncertainty, RI format, DRI format, RI starts column 22 |
| 213 | `5084.2(5)` | `0.14(5)` | 350 | 9158.71 | `5084.2(5)` | `.14(5)` | RI format, RI starts column 22 |
| 214 | `5202.06(6)` | `3.00(29)` | 315 | 8506.77 | `5202.06(6)` | `.0(3)` | RI value, DRI uncertainty, RI format, DRI format, RI starts column 22 |
| 215 | `5239.8(4)` | `0.65(9)` | 263 | 7367.42 | `5239.8(4)` | `.65(9)` | RI format, RI starts column 22 |
| 216 | `5247.94(4)` | `11.8(11)` | 468 | 11417.223 | `5247.94(4)` | `1.8(11)` | RI value, RI format, RI starts column 22 |
| 217 | `5268.9(6)` | `0.27(7)` | 396 | 10650.11 | `5268.9(6)` | `.27(7)` | RI format, RI starts column 22 |
| 220 | `5380.59(9)` | `1.97(20)` | 144 | 5380.99 | `5380.59(9)` | `.97(20)` | RI value, RI format, RI starts column 22 |
| 221 | `5501.4(5)` | `0.46(9)` | 337 | 8805.66 | `5501.4(5)` | `.46(9)` | RI format, RI starts column 22 |
| 222 | `5569.30(5)` | `5.6(6)` | 471 | 11417.223 | `5569.30(5)` | `.6(6)` | RI value, RI format, RI starts column 22 |
| 224 | `5660.78(6)` | `18.4(18)` | 473 | 11417.223 | `5660.78(6)` | `8.4(18)` | RI value, RI format, RI starts column 22 |
| 225 | `5736.76(4)` | `43(4)` | 475 | 11417.223 | `5736.76(4)` | `3(4)` | RI value, RI format, RI starts column 22 |
| 226 | `5755.5(5)` | `0.51(8)` | 170 | 5755.875 | `5755.5(5)` | `.51(8)` | RI format, RI starts column 22 |
| 227 | `5847.4(5)` | `0.25(6)` | 289 | 7974.72 | `5847.4(5)` | `.25(6)` | RI format, RI starts column 22 |
| 228 | `5884.6(6)` | `0.27(6)` | 368 | 9801.89 | `5884.6(6)` | `.27(6)` | RI format, RI starts column 22 |
| 230 | `6010.3(3)` | `0.50(8)` | 297 | 8138.10 | `6010.3(3)` | `.50(8)` | RI format, RI starts column 22 |
| 231 | `6035.68(7)` | `4.4(5)` | 478 | 11417.223 | `6035.68(7)` | `.4(5)` | RI value, RI format, RI starts column 22 |
| 233 | `6094.4(4)` | `0.21(5)` | 480 | 11417.223 | `6094.4(4)` | `.21(5)` | RI format, RI starts column 22 |
| 234 | `6152.1(5)` | `0.18(5)` | 399 | 10840.64 | `6152.1(5)` | `.18(5)` | RI format, RI starts column 22 |
| 236 | `6188.45(6)` | `8.7(9)` | 481 | 11417.223 | `6188.45(6)` | `.7(9)` | RI value, RI format, RI starts column 22 |
| 238 | `6241.0(5)` | `0.45(7)` | 359 | 9546.09 | `6241.0(5)` | `.45(7)` | RI format, RI starts column 22 |
| 239 | `6341.58(32)` | `0.45(8)` | 210 | 6342.50 | `6341.6(3)` | `0.45(8)` | E numeric/rounding, DE uncertainty, E format, DE format |
| 240 | `6487.48(6)` | `3.6(4)` | 323 | 8615.74 | `6487.48(6)` | `.6(4)` | RI value, RI format, RI starts column 22 |
| 241 | `6496.22(23)` | `0.56(7)` | 369 | 9801.89 | `6496.62(23)` | `0.56(7)` | E numeric/rounding, E format |
| 242 | `6526.84(6)` | `5.5(6)` | 483 | 11417.223 | `6526.84(6)` | `.5(6)` | RI value, RI format, RI starts column 22 |
| 244 | `6573.6(4)` | `1.09(19)` | 329 | 8702.35 | `6573.6(4)` | `.09(19)` | RI value, RI format, RI starts column 22 |
| 245 | `6600.1(7)` | `0.23(5)` | 333 | 8727.63 | `6600.1(7)` | `.23(5)` | RI format, RI starts column 22 |
| 246 | `6727.5(9)` | `0.07(4)` | 486 | 11417.223 | `6727.5(9)` | `.07(4)` | RI format, RI starts column 22 |
| 247 | `6745.64(16)` | `2.71(30)` | 343 | 8874.02 | `6745.64(16)` | `2.7(3)` | RI value, DRI uncertainty, RI format, DRI format |
| 248 | `6792.10(3)` | `24.2(23)` | 487 | 11417.223 | `6792.10(3)` | `4.2(23)` | RI value, RI format, RI starts column 22 |
| 249 | `6846.37(32)` | `0.56(7)` | 237 | 6847.90 | `6846.4(3)` | `0.56(7)` | E numeric/rounding, DE uncertainty, E format, DE format |
| 250 | `7218.48(13)` | `2.71(28)` | 257 | 7219.28 | `7218.48(13)` | `2.7(3)` | RI value, DRI uncertainty, RI format, DRI format |
| 251 | `7302.2(8)` | `0.28(5)` | 490 | 11417.223 | `7302.2(8)` | `.28(5)` | RI format, RI starts column 22 |
| 252 | `7341.67(6)` | `36.5(34)` | 491 | 11417.223 | `7341.67(6)` | `6.5(14)` | RI value, DRI uncertainty, RI format, DRI format, RI starts column 22 |
| 253 | `7499.90(5)` | `62(6)` | 494 | 11417.223 | `7499.90(5)` | `2(6)` | RI value, RI format, RI starts column 22 |
| 254 | `7536.2(7)` | `0.44(10)` | 366 | 9665.74 | `7536.2(7)` | `.44(10)` | RI format, RI starts column 22 |
| 255 | `7675.0(8)` | `0.16(4)` | 370 | 9801.89 | `7675.0(8)` | `.16(4)` | RI format, RI starts column 22 |
| 256 | `7708.32(30)` | `0.44(7)` | 373 | 9836.70 | `7708.3(3)` | `0.44(7)` | E numeric/rounding, DE uncertainty, E format, DE format |
| 259 | `8036.6(7)` | `0.18(4)` | 293 | 8036.30 | `8036.6(7)` | `.18(4)` | RI format, RI starts column 22 |
| 260 | `8051.1(6)` | `0.26(5)` | 384 | 10179.59 | `8051.1(6)` | `.26(5)` | RI format, RI starts column 22 |
| 261 | `8083.49(31)` | `0.47(7)` | 387 | 10212.15 | `8083.5(3)` | `0.47(7)` | E numeric/rounding, DE uncertainty, E format, DE format |
| 262 | `8111.99(9)` | `6.1(7)` | 496 | 11417.223 | `8111.99(9)` | `.1(7)` | RI value, RI format, RI starts column 22 |
| 264 | `8173.8(9)` | `0.157(31)` | 301 | 8175.1 | `8173.8(9)` | `.16(3)` | RI value, DRI uncertainty, RI format, DRI format, RI starts column 22 |
| 266 | `8384.28(9)` | `3.43(33)` | 311 | 8385.40 | `8384.28(9)` | `.43(33)` | RI value, RI format, RI starts column 22 |
| 269 | `8804.4(4)` | `0.24(4)` | 338 | 8805.66 | `8804.4(4)` | `.24(4)` | RI format, RI starts column 22 |
| 271 | `9206.65(26)` | `0.35(5)` | 355 | 9208.04 | `9206.7(3)` | `0.35(5)` | E numeric/rounding, DE uncertainty, E format, DE format |
| 273 | `9544.83(28)` | `0.38(5)` | 360 | 9546.09 | `9544.8(3)` | `0.38(5)` | E numeric/rounding, DE uncertainty, E format, DE format |
| 274 | `9932.1(6)` | `0.082(19)` | 378 | 9933.35 | `9932.1(6)` | `.082(19)` | RI format, RI starts column 22 |

## Ambiguous Matches

| Source line | Source E | Candidate target line/parent/E |
|---:|---:|---|
| 33 | `989.08` | 247/7110.45/989.1; 265/7467.72/989.1 |
| 64 | `1544.41` | 196/6168.86/1544.41; 212/6421.42/1544.41 |
| 76 | `1732.39` | 178/5847.53/1732.7; 213/6421.42/1732.39 |
| 81 | `1795.28` | 295/8138.10/1795.3; 376/9933.35/1795.3 |
| 108 | `2326.2` | 336/8805.66/2326.2; 358/9546.09/2326.2 |
| 121 | `2543.13` | 180/5847.53/2543.13; 436/11417.223/2543.13 |
| 132 | `2817.76` | 188/6121.49/2817.76; 365/9665.74/2817.76 |
| 139 | `2945.8` | 300/8175.1/2945.8; 326/8702.35/2945.8 |
| 217 | `5268.9` | 396/10650.11/5268.9; 403/11024.94/5268.9 |

## Unmatched Source Rows

None. All source rows matched within +/-0.5 keV.

## Extra Target G Records

These target records have no unique source-row assignment under the energy-only comparison. Many are LT upper limits or transitions not listed in Table V.

| Target line | Parent L E | Target E(DE) | Target RI(DRI) |
|---:|---:|---|---|
| 76 | 4074.667 | `158.3()` | `.06(LT)` |
| 82 | 4114.813 | `198.4()` | `.03(LT)` |
| 83 | 4114.813 | `810.6()` | `.06(LT)` |
| 87 | 4624.404 | `549.7()` | `.05(LT)` |
| 88 | 4624.404 | `708.0()` | `.11(LT)` |
| 96 | 4876.839 | `187.9()` | `.03(LT)` |
| 97 | 4876.839 | `252.4()` | `.03(LT)` |
| 98 | 4876.839 | `762.0()` | `.11(LT)` |
| 99 | 4876.839 | `802.2()` | `.64(LT)` |
| 100 | 4876.839 | `960.4()` | `.08(LT)` |
| 103 | 4876.839 | `4876.8()` | `.25(LT)` |
| 105 | 4889.756 | `200.8()` | `.02(LT)` |
| 106 | 4889.756 | `265.4()` | `.02(LT)` |
| 107 | 4889.756 | `774.9()` | `.09(LT)` |
| 108 | 4889.756 | `815.1()` | `.06(LT)` |
| 109 | 4889.756 | `973.3()` | `.05(LT)` |
| 114 | 5228.175 | `338.4()` | `.03(LT)` |
| 115 | 5228.175 | `351.3()` | `.10(LT)` |
| 116 | 5228.175 | `539.2()` | `.04(LT)` |
| 117 | 5228.175 | `603.8()` | `.04(LT)` |
| 120 | 5228.175 | `1924.0()` | `.21(LT)` |
| 121 | 5228.175 | `3100.6()` | `.21(LT)` |
| 123 | 5322.51 | `432.8()` | `.06(LT)` |
| 124 | 5322.51 | `445.7()` | `.06(LT)` |
| 125 | 5322.51 | `633.5()` | `.11(LT)` |
| 127 | 5322.51 | `1207.7()` | `.16(LT)` |
| 129 | 5322.51 | `1406.1()` | `.10(LT)` |
| 130 | 5322.51 | `2018.3()` | `.11(LT)` |
| 132 | 5322.51 | `5322.5()` | `.24(LT)` |
| 134 | 5380.99 | `151.8()` | `.02(LT)` |
| 135 | 5380.99 | `491.2()` | `.06(LT)` |
| 136 | 5380.99 | `504.2()` | `.06(LT)` |
| 137 | 5380.99 | `692.0()` | `.06(LT)` |
| 138 | 5380.99 | `756.6()` | `.06(LT)` |
| 140 | 5380.99 | `1306.3()` | `.10(LT)` |
| 141 | 5380.99 | `1464.6()` | `.10(LT)` |
| 146 | 5679.927 | `357.4()` | `.05(LT)` |
| 147 | 5679.927 | `451.8()` | `.05(LT)` |
| 150 | 5679.927 | `990.9()` | `.11(LT)` |
| 153 | 5679.927 | `1605.3()` | `.11(LT)` |
| 154 | 5679.927 | `1763.5()` | `.11(LT)` |
| 157 | 5679.927 | `5679.9()` | `.53(LT)` |
| 159 | 5755.875 | `433.4()` | `.05(LT)` |
| 160 | 5755.875 | `527.7()` | `.05(LT)` |
| 161 | 5755.875 | `866.1()` | `.07(LT)` |
| 162 | 5755.875 | `879.0()` | `.07(LT)` |
| 163 | 5755.875 | `1066.9()` | `.09(LT)` |
| 164 | 5755.875 | `1131.5()` | `.09(LT)` |
| 166 | 5755.875 | `1681.2()` | `.09(LT)` |
| 167 | 5755.875 | `1839.5()` | `.70(LT)` |
| 172 | 5847.53 | `525.0()` | `.09(LT)` |
| 173 | 5847.53 | `619.4()` | `.09(LT)` |
| 174 | 5847.53 | `957.8()` | `.14(LT)` |
| 175 | 5847.53 | `970.7()` | `.14(LT)` |
| 176 | 5847.53 | `1158.6()` | `.26(LT)` |
| 177 | 5847.53 | `1223.1()` | `.20(LT)` |
| 178 | 5847.53 | `1732.7()` | `.75(LT)` |
| 192 | 6168.86 | `940.7()` | `.29(LT)` |
| 193 | 6168.86 | `1279.1()` | `.11(LT)` |
| 194 | 6168.86 | `1292.0()` | `.09(LT)` |
| 198 | 6168.86 | `2094.2()` | `.11(LT)` |
| 199 | 6168.86 | `2252.5()` | `.11(LT)` |
| 212 | 6421.42 | `1544.41(10)` | `2.58(24)` |
| 223 | 6478.770 | `1250.6()` | `.22(LT)` |
| 224 | 6478.770 | `1589.0()` | `.11(LT)` |
| 230 | 6478.770 | `6478.8()` | `.02(LT)` |
| 265 | 7467.72 | `989.1(3)` | `0.079(23)` |
| 273 | 7629.907 | `2307.4()` | `.13(LT)` |
| 274 | 7629.907 | `2401.7()` | `.13(LT)` |
| 275 | 7629.907 | `2740.2()` | `.18(LT)` |
| 279 | 7629.907 | `3713.5()` | `.18(LT)` |
| 281 | 7629.907 | `7629.9()` | `.33(LT)` |
| 326 | 8702.35 | `2945.8(10)` | `0.30(9)` |
| 358 | 9546.09 | `2326.2(10)` | `0.05(4)` |
| 365 | 9665.74 | `2817.76(25)` | `0.84(13)` |
| 376 | 9933.35 | `1795.3(3)` | `0.19(5)` |
| 403 | 11024.94 | `5268.9(6)` | `.27(7)` |
| 436 | 11417.223 | `2543.13(10)` | `9.6(9)` |

## Reproducible Spot Check

- Seed: `12520260817`; sample size: `41` (15.1%)
- Failures: `13`

| Source line | Target line | Result |
|---:|---:|---|
| 193 | 461 | PASS |
| 10 | 412 | PASS |
| 42 | 47 | PASS |
| 104 | 248 | FAIL: RI |
| 229 | 186 | PASS |
| 90 | 308 | PASS |
| 201 | 464 | PASS |
| 35 | 46 | FAIL: RI, DRI |
| 115 | 57 | FAIL: RI |
| 173 | 181 | PASS |
| 206 | 402 | PASS |
| 237 | 393 | PASS |
| 203 | 342 | FAIL: DE |
| 36 | 151 | PASS |
| 238 | 359 | PASS |
| 218 | 470 | PASS |
| 224 | 473 | FAIL: RI |
| 127 | 102 | FAIL: RI |
| 83 | 353 | PASS |
| 6 | 42 | PASS |
| 262 | 496 | FAIL: RI |
| 103 | 270 | PASS |
| 197 | 462 | PASS |
| 39 | 183 | PASS |
| 96 | 55 | FAIL: RI |
| 255 | 370 | PASS |
| 180 | 320 | PASS |
| 270 | 346 | PASS |
| 174 | 319 | PASS |
| 160 | 267 | PASS |
| 213 | 350 | PASS |
| 214 | 315 | FAIL: RI, DRI |
| 258 | 290 | PASS |
| 170 | 345 | PASS |
| 231 | 478 | FAIL: RI |
| 261 | 387 | FAIL: DE |
| 273 | 360 | FAIL: DE |
| 166 | 156 | FAIL: RI |
| 219 | 322 | PASS |
| 241 | 369 | PASS |
| 181 | 189 | PASS |

## Assessment

The source energy list is complete against the target at the selected tolerance, but the target requires correction or deliberate retention review before it can be called 100% consistent. The most widespread issue is RI field alignment/representation; 127 matched target records have a nonblank column 22, indicating RI begins one column early relative to ENSDF field definitions.
