datasets mapped: 28  unmapped: []
tokens audited: 1074  findings: 332
[('MISSING-PARENTHETICAL', 283), ('J-CONFLICT', 15), ('MISSING-ADOPTED', 13), ('NO-OWN-LEVEL', 5), ('UNCLAIMED-LEVEL', 5), ('SWAPPED', 3), ('STAR-ONCE', 2), ('SHARED-NO-STAR', 2), ('FAR-PIN', 2), ('UNCITED-LEVEL', 2)]

### NO-OWN-LEVEL (5)
| C | 9336(20) (1+) | `C` | nearest 9326(10) (1+) | level already claimed by adopted 9327.3(6) 1+ via C(9326) |
| E | 7879.2(9) 1+ | `E` | nearest 7875.2(9) 1+ | level outside window |
| F | 8237.9(4) 1- | `F` | nearest 8240(8) 1+ | level already claimed by adopted 8203(20) (1+) via F |
| X | 3269.2(8) (2) | `X` | nearest 3260  | level already claimed by adopted 3263.64(18) 2+ via X |
| X | 3273.8(7) (2) | `X` | nearest 3260  | level already claimed by adopted 3263.64(18) 2+ via X |

### UNCLAIMED-LEVEL (5)
| C | 10107(10) 1+ | `C` | 10119 1+ | dE=12.0; that adopted level's token owns 10095 1 |
| C | 12283(10) (1) | `C` | 12300 1(-) | dE=17.0; that adopted level's token owns 12293(10) 1+ |
| C | 6468.4(7) (1+) | `C(6474)` | 6468(5)  | dE=0.4; that adopted level's token owns 6474 (1) |
| C | 6854.5(10) 3- | `C(6844)` | 6854(5) 3- | dE=0.5; that adopted level's token owns 6844(10) 3- |
| C | 8962.0(7) 1+ | `C(8988)` | 8959 1+ | dE=3.0; that adopted level's token owns 8988 1+ |

### SWAPPED (3)
| C | 6468.4(7) (1+) | `C(6474)` | unclaimed 6468(5)  | token names 6474 (dE=5.6); unclaimed level is dE=0.4 |
| C | 6854.5(10) 3- | `C(6844)` | unclaimed 6854(5) 3- | token names 6844 (dE=10.5); unclaimed level is dE=0.5 |
| C | 8962.0(7) 1+ | `C(8988)` | unclaimed 8959 1+ | token names 8988 (dE=26.0); unclaimed level is dE=3.0 |

### SHARED-NO-STAR (2)
| C | 7585.6(6)  | `C(7590)` | 7590 (1) | 2 adopted levels claim this dataset level, none starred |
| C | 7603(8) (1-) | `C(7590)` | 7590 (1) | 2 adopted levels claim this dataset level, none starred |

### FAR-PIN (2)
| C | 8962.0(7) 1+ | `C(8988)` | 8988 1+ | dE=26.0 beyond window 15.1 |
| H | 4752.2(7) 4+ | `H(4720)` | 4720  | dE=32.2 beyond window 30.1 |

### J-CONFLICT (15)
| C | 10073(10) 1+ | `C(10071)` | 10071 1(-) | J incompatible, dE=2.0, documented in adopted comment |
| C | 13016.5(10) (13-) | `C(13029)` | 13029 1 | J incompatible, dE=12.5, UNDOCUMENTED |
| C | 9407(10) (2-) | `C(9421)` | 9421 (1) | J incompatible, dE=14.0, UNDOCUMENTED |
| C | 9523.7(9) 1- | `C(9526)` | 9526(10) (1+) | J incompatible, dE=2.3, documented in adopted comment |
| E | 9843(5) 1+ | `E` | 9843.0(15) 2+ | J incompatible, dE=0.0, documented in adopted comment |
| F | 10029(5) 3- | `F` | 10036(10) (2-) | J incompatible, dE=7.0, documented in adopted comment |
| F | 11052(10) (1+) | `F` | 11041(10) (2+) | J incompatible, dE=11.0, documented in adopted comment |
| F | 12386(10) (1+) | `F` | 12386(10) (2+) | J incompatible, dE=0.0, documented in adopted comment |
| F | 8514.8(4) 1- | `F` | 8516(8) 1+ | J incompatible, dE=1.2, documented in adopted comment |
| F | 8880.9(6) 1- | `F` | 8875(8) 1+ | J incompatible, dE=5.9, documented in adopted comment |
| F | 9369.3(6) 1- | `F` | 9368(10) 1+,(2-) | J incompatible, dE=1.3, documented in adopted comment |
| F | 9523.7(9) 1- | `F` | 9513(10) 1+,(2-) | J incompatible, dE=10.7, documented in adopted comment |
| F | 9554.8(21) 1 | `F` | 9552(10) (2-) | J incompatible, dE=2.8, documented in adopted comment |
| F | 9870(5) 3- | `F` | 9870(10) (2-) | J incompatible, dE=0.0, documented in adopted comment |
| U | 4358.6(6) (2+,3,4+) | `U` | 4361.2(14) (5) | J incompatible, dE=2.6, UNDOCUMENTED |

### STAR-ONCE (2)
| C | 7616.5(10) (1) | `C(7590*)` |  | starred token used on one adopted level only |
| C | 9037(8) (1+) | `C(9044*)` |  | starred token used on one adopted level only |

### UNCITED-LEVEL (2)
| C | 10744(5) 4+ | `(no C)` | 10744(5) 4+ | dE=0.0, J compatible |
| U | 7180(25) 3- | `(no U)` | 7231.8(9)  | dE=51.8, J compatible |

### MISSING-ADOPTED (13)
| C | 9191.5(5) 1- | `-` | 9193(10) (1+) | only J-incompatible adopted level nearby (dE=1.5) |
| E | - | `-` | 2014.9(4)  | no adopted level within window |
| E | - | `-` | 2034.6(3) 2 | no adopted level within window |
| E | - | `-` | 2385.1(9) (2) | no adopted level within window |
| E | - | `-` | 2598.4(3)  | no adopted level within window |
| E | - | `-` | 2632.8(13) (1) | no adopted level within window |
| E | - | `-` | 2741.8(7) (2) | no adopted level within window |
| E | - | `-` | 3202.2(3)  | no adopted level within window |
| E | - | `-` | 3253.7(4)  | no adopted level within window |
| E | 7860(5) 4+ | `-` | 7875.2(9) 1+ | only J-incompatible adopted level nearby (dE=15.2) |
| E | 8514.8(4) 1- | `-` | 8512.4(1) 1+ | only J-incompatible adopted level nearby (dE=2.4) |
| P | - | `-` | 5662  | no adopted level within window |
| S | - | `-` | 5662  | no adopted level within window |

### MISSING-PARENTHETICAL (283)
| A | 1454.20(8) 2+ | `A` | 1454.56(15) 2+ | dE=0.4; convention is A(1454.56) |
| A | 2775.39(13) 2+ | `A` | 2776.1(3) 2+ | dE=0.7; convention is A(2776.1) |
| A | 2902.07(16) 1+ | `A` | 2902.86(21) 1+ | dE=0.8; convention is A(2902.86) |
| A | 2942.54(15) 0+ | `A` | 2943.3(3) 0+ | dE=0.8; convention is A(2943.3) |
| A | 3037.83(14) 2+ | `A` | 3038.7(5) 2+ | dE=0.9; convention is A(3038.7) |
| A | 3263.64(18) 2+ | `A` | 3264.64(16) 2+ | dE=1.0; convention is A(3264.64) |
| A | 3531.10(19) 0+ | `A` | 3532.2(8) 0+ | dE=1.1; convention is A(3532.2) |
| A | 3593.70(19) 2+ | `A` | 3594.99(25) 2+ | dE=1.3; convention is A(3594.99) |
| A | 3898.8(4) 2+ | `A` | 3899.5(9) 2+ | dE=0.7; convention is A(3899.5) |
| A | 4448.91(33) 2+,1+,0+ | `A` | 4450.0(4) 2+,1+,0+ | dE=1.1; convention is A(4450) |
| B | 1454.20(8) 2+ | `B` | 1454.3(1) 2+ | dE=0.1; convention is B(1454.3) |
| B | 2775.39(13) 2+ | `B` | 2775.7(3) 2+ | dE=0.3; convention is B(2775.7) |
| B | 2902.07(16) 1+ | `B` | 2903.5(11) 1+ | dE=1.4; convention is B(2903.5) |
| B | 3531.10(19) 0+ | `B` | 3531.4(6) 0+ | dE=0.3; convention is B(3531.4) |
| B | 3620.10(18) 4+ | `B` | 3620.9(5) 4+ | dE=0.8; convention is B(3620.9) |
| B | 3774.82(22) 3+ | `B` | 3776.0(5) 3+ | dE=1.2; convention is B(3776) |
| B | 4108.19(24) 2+ | `B` | 4107.6(7) 2+ | dE=0.6; convention is B(4107.6) |
| B | 4294.86(34) 4+ | `B` | 4295.5(11) 4+ | dE=0.6; convention is B(4295.5) |
| B | 4404.23(34) 4+ | `B` | 4406.0(9) 4+ | dE=1.8; convention is B(4406) |
| C | 10107(10) 1+ | `C` | 10095 1 | dE=12.0; convention is C(10095) |
| C | 1454.20(8) 2+ | `C` | 1454.0(2) 2+ | dE=0.2; convention is C(1454) |
| C | 2775.39(13) 2+ | `C` | 2775.2(3) 2+ | dE=0.2; convention is C(2775.2) |
| C | 2902.07(16) 1+ | `C` | 2901.5(5) 1+ | dE=0.6; convention is C(2901.5) |
| C | 3263.64(18) 2+ | `C` | 3263.4(3) 2+ | dE=0.2; convention is C(3263.4) |
| C | 3420.52(15) 3+ | `C` | 3420.3(3) 3+ | dE=0.2; convention is C(3420.3) |
| C | 3531.10(19) 0+ | `C` | 3530.9(4) 0+ | dE=0.2; convention is C(3530.9) |
| C | 3593.70(19) 2+ | `C` | 3593.4(4) (1,2+) | dE=0.3; convention is C(3593.4) |
| C | 3774.82(22) 3+ | `C` | 3774.5(4) 3+ | dE=0.3; convention is C(3774.5) |
| C | 3898.8(4) 2+ | `C` | 3898.2(4) 2+ | dE=0.6; convention is C(3898.2) |
| C | 4108.19(24) 2+ | `C` | 4107.6(5) 2+ | dE=0.6; convention is C(4107.6) |
| C | 4294.86(34) 4+ | `C` | 4294(5) 4(+) | dE=0.9; convention is C(4294) |
| C | 4347.9(12)  | `C` | 4346.6(15)  | dE=1.3; convention is C(4346.6) |
| C | 4358.6(6) (2+,3,4+) | `C` | 4355(5) (2+,3,4+) | dE=3.6; convention is C(4355) |
| C | 4382.96(26) (5+) | `C` | 4380(5) (5+) | dE=3.0; convention is C(4380) |
| C | 4404.23(34) 4+ | `C` | 4404.8(13) 4+ | dE=0.6; convention is C(4404.8) |
| C | 4474.6(5) 3- | `C` | 4475.3(8) 3- | dE=0.7; convention is C(4475.3) |
| C | 4538.0(6) 0+ | `C` | 4536.1(8) 0+ | dE=1.9; convention is C(4536.1) |
| C | 4574.3(5) 1 | `C` | 4578(7)  | dE=3.7; convention is C(4578) |
| C | 4752.2(7) 4+ | `C` | 4755(5) 4+ | dE=2.8; convention is C(4755) |
| C | 4964.72(26) (5+) | `C` | 4962(5)  | dE=2.7; convention is C(4962) |
| C | 5127.39(29) 6+ | `C` | 5128(10) 6+ | dE=0.6; convention is C(5128) |
| C | 5384.5(4) 6+ | `C` | 5380(5)  | dE=4.5; convention is C(5380) |
| C | 5436.3(10) 4+ | `C` | 5432(5) 4+ | dE=4.3; convention is C(5432) |
| C | 5452.5(4) 1 | `C` | 5460(10)  | dE=7.5; convention is C(5460) |
| C | 5472.3(7) 4+ | `C` | 5470(5) 4+ | dE=2.3; convention is C(5470) |
| C | 5594.2(6) 4+ | `C` | 5592(5)  | dE=2.2; convention is C(5592) |
| C | 6067.5(4) (7+) | `C` | 6066(10)  | dE=1.5; convention is C(6066) |
| C | 6084.6(4) 7- | `C` | 6080(5)  | dE=4.6; convention is C(6080) |
| C | 8395.2(4) 1- | `C` | 8392(10)  | dE=3.2; convention is C(8392) |
| C | 8514.8(4) 1- | `C` | 8517(10) [1-] | dE=2.2; convention is C(8517) |
| C | 8553.4(13) 1(+) | `C` | 8556(10) 1(+) | dE=2.6; convention is C(8556) |
| C | 8601.2(7) 1+ | `C` | 8602(10) 1+ | dE=0.8; convention is C(8602) |
| C | 8680.0(8) 1+ | `C` | 8677(10) 1+ | dE=3.0; convention is C(8677) |
| C | 8858.1(6) 1+ | `C` | 8856(10) 1(+) | dE=2.1; convention is C(8856) |
| C | 8880.9(6) 1- | `C` | 8880(10) [1-] | dE=0.9; convention is C(8880) |
| C | 9074.2(6) 1+ | `C` | 9073 1+ | dE=1.2; convention is C(9073) |
| C | 9157.7(7) 1+ | `C` | 9156(10) 1+ | dE=1.7; convention is C(9156) |
| C | 9750(10) 1+ | `C` | 9739(10) 1+ | dE=11.0; convention is C(9739) |
| C | 9843(5) 1+ | `C` | 9835(10) 1+ | dE=8.0; convention is C(9835) |
| D | 1454.20(8) 2+ | `D` | 1456(8) 2+ | dE=1.8; convention is D(1456) |
| D | 18000  | `D` | 17.8E3(4)  | dE=200.0; convention is D(17800) |
| D | 2459.22(12) 4+ | `D` | 2462(8) 4+ | dE=2.8; convention is D(2462) |
| D | 2775.39(13) 2+ | `D` | 2771(8) 2+ | dE=4.4; convention is D(2771) |
| D | 3037.83(14) 2+ | `D` | 3035(8) 2+ | dE=2.8; convention is D(3035) |
| D | 3263.64(18) 2+ | `D` | 3266(8) 2+ | dE=2.4; convention is D(3266) |
| D | 3420.52(15) 3+ | `D` | 3414 3+ | dE=6.5; convention is D(3414) |
| D | 3593.70(19) 2+ | `D` | 3588 2+ | dE=5.7; convention is D(3588) |
| D | 3620.10(18) 4+ | `D` | 3618(8) 4+ | dE=2.1; convention is D(3618) |
| D | 3774.82(22) 3+ | `D` | 3773 3+ | dE=1.8; convention is D(3773) |
| D | 3898.8(4) 2+ | `D` | 3908(8) 2+ | dE=9.2; convention is D(3908) |
| D | 4108.19(24) 2+ | `D` | 4105(8) 2+ | dE=3.2; convention is D(4105) |
| D | 4347.9(12)  | `D` | 4350  | dE=2.1; convention is D(4350) |
| D | 4404.23(34) 4+ | `D` | 4405 4+ | dE=0.8; convention is D(4405) |
| D | 4448.91(33) 2+,1+,0+ | `D` | 4444 2+,1+,0+ | dE=4.9; convention is D(4444) |
| D | 4474.6(5) 3- | `D` | 4472(8) 3- | dE=2.6; convention is D(4472) |
| D | 4538.0(6) 0+ | `D` | 4530 0+ | dE=8.0; convention is D(4530) |
| D | 4752.2(7) 4+ | `D` | 4750(8) 4+ | dE=2.2; convention is D(4750) |
| D | 5127.39(29) 6+ | `D` | 5122(8) 6+ | dE=5.4; convention is D(5122) |
| D | 5394.3(9)  | `D` | 5408  | dE=13.7; convention is D(5408) |
| D | 5588.9(7) (5-) | `D` | 5590 (5-) | dE=1.1; convention is D(5590) |
| D | 5590.3(10) 2+ | `D` | 5582(8) 2+ | dE=8.3; convention is D(5582) |
| D | 6027.7(4) 1- | `D` | 6024(8) 1- | dE=3.7; convention is D(6024) |
| D | 6308.5(6) 3- | `D` | 6318(8) 3- | dE=9.5; convention is D(6318) |
| D | 6854.5(10) 3- | `D` | 6847(15) 3- | dE=7.5; convention is D(6847) |
| D | 7054.5(10) 1- | `D` | 7056(15) 1- | dE=1.5; convention is D(7056) |
| D | 7210.4(10) 3- | `D` | 7212(15)  | dE=1.6; convention is D(7212) |
| D | 7514.5(10) 3- | `D` | 7521(15) 3- | dE=6.5; convention is D(7521) |
| D | 7721(10)  | `D` | 7734(15)  | dE=13.0; convention is D(7734) |
| E | 3263.64(18) 2+ | `E` | 3263.9(6) 2 | dE=0.3; convention is E(3263.9) |
| E | 3593.70(19) 2+ | `E` | 3595.2(9)  | dE=1.5; convention is E(3595.2) |
| E | 3898.8(4) 2+ | `E` | 3898 2+ | dE=0.8; convention is E(3898) |
| E | 4108.19(24) 2+ | `E` | 4106.4(10)  | dE=1.8; convention is E(4106.4) |
| E | 7048.7(9) 1- | `E` | 7047.3(5) 1- | dE=1.4; convention is E(7047.3) |
| E | 7389.3(4) 1+ | `E` | 7388.8(4) 1+ | dE=0.5; convention is E(7388.8) |
| E | 7808.4(5) 1- | `E` | 7807.3(5) 1- | dE=1.1; convention is E(7807.3) |
| E | 8237.9(4) 1- | `E` | 8237.3(4) 1- | dE=0.6; convention is E(8237.3) |
| E | 8395.2(4) 1- | `E` | 8394.0(7) 1- | dE=1.2; convention is E(8394) |
| E | 8461.7(7) 1+ | `E` | 8459.9(6) 1+ | dE=1.8; convention is E(8459.9) |
| E | 8514.8(4) 1- | `E` | 8514.1(4) 1- | dE=0.7; convention is E(8514.1) |
| E | 8601.2(7) 1+ | `E` | 8600.2(6) 1+ | dE=1.0; convention is E(8600.2) |
| E | 8778.6(5) 1+ | `E` | 8777.9(5) 1+ | dE=0.7; convention is E(8777.9) |
| E | 8858.1(6) 1+ | `E` | 8857.4(6) 1+ | dE=0.7; convention is E(8857.4) |
| E | 8880.9(6) 1- | `E` | 8880.2(6) 1- | dE=0.7; convention is E(8880.2) |
| E | 8935.3(5) 1- | `E` | 8934.6(5) 1- | dE=0.7; convention is E(8934.6) |
| E | 9074.2(6) 1+ | `E` | 9073.4(6) 1+ | dE=0.8; convention is E(9073.4) |
| E | 9191.5(5) 1- | `E` | 9190.7(5) 1- | dE=0.8; convention is E(9190.7) |
| E | 9327.3(6) 1+ | `E` | 9326.4(8) 1+ | dE=0.9; convention is E(9326.4) |
| E | 9369.3(6) 1- | `E` | 9368.5(6) 1- | dE=0.8; convention is E(9368.5) |
| F | 10029(5) 3- | `F` | 10036(10) (2-) | dE=7.0; convention is F(10036) |
| F | 11052(10) (1+) | `F` | 11041(10) (2+) | dE=11.0; convention is F(11041) |
| F | 1454.20(8) 2+ | `F` | 1454(5) 2+ | dE=0.2; convention is F(1454) |
| F | 2459.22(12) 4+ | `F` | 2459(5) 4+ | dE=0.2; convention is F(2459) |
| F | 2775.39(13) 2+ | `F` | 2775(5) 2+ | dE=0.4; convention is F(2775) |
| F | 2942.54(15) 0+ | `F` | 2940  | dE=2.5; convention is F(2940) |
| F | 3037.83(14) 2+ | `F` | 3038(5) 2+ | dE=0.2; convention is F(3038) |
| F | 3263.64(18) 2+ | `F` | 3264(5) 2+ | dE=0.4; convention is F(3264) |
| F | 3531.10(19) 0+ | `F` | 3530 0+ | dE=1.1; convention is F(3530) |
| F | 3898.8(4) 2+ | `F` | 3898(5) 2+ | dE=0.8; convention is F(3898) |
| F | 4474.6(5) 3- | `F` | 4470(5) 3- | dE=4.6; convention is F(4470) |
| F | 4538.0(6) 0+ | `F` | 4540 0+ | dE=2.0; convention is F(4540) |
| F | 4752.2(7) 4+ | `F` | 4750(5) 4+ | dE=2.2; convention is F(4750) |
| F | 5127.39(29) 6+ | `F` | 5125(10) 6+ | dE=2.4; convention is F(5125) |
| F | 5436.3(10) 4+ | `F` | 5430(15) 4(+) | dE=6.3; convention is F(5430) |
| F | 6018.4(10) 3- | `F` | 6017(15)  | dE=1.4; convention is F(6017) |
| F | 6027.7(4) 1- | `F` | 6031(8) 2+,(1-) | dE=3.3; convention is F(6031) |
| F | 6274.4(10) 4(+) | `F` | 6280(15) 4(+) | dE=5.6; convention is F(6280) |
| F | 6468.4(7) (1+) | `F` | 6475(8) 1+,(2-) | dE=6.6; convention is F(6475) |
| F | 6763.5(10) 3- | `F` | 6768(8)  | dE=4.5; convention is F(6768) |
| F | 6854.5(10) 3- | `F` | 6851(8) 3- | dE=3.5; convention is F(6851) |
| F | 7210.4(10) 3- | `F` | 7209(8) 3- | dE=1.4; convention is F(7209) |
| F | 7300.5(10) 3- | `F` | 7290(8)  | dE=10.5; convention is F(7290) |
| F | 7389.3(4) 1+ | `F` | 7388(8) 1+ | dE=1.3; convention is F(7388) |
| F | 7514.5(10) 3- | `F` | 7500(8) 3- | dE=14.5; convention is F(7500) |
| F | 7680.6(10) 1- | `F` | 7684(8) 1- | dE=3.4; convention is F(7684) |
| F | 8203(20) (1+) | `F` | 8240(8) 1+ | dE=37.0; convention is F(8240) |
| F | 8514.8(4) 1- | `F` | 8516(8) 1+ | dE=1.2; convention is F(8516) |
| F | 8845(5) 3- | `F` | 8854(8) 2+,3- | dE=9.0; convention is F(8854) |
| F | 8880.9(6) 1- | `F` | 8875(8) 1+ | dE=5.9; convention is F(8875) |
| F | 8935.3(5) 1- | `F` | 8926(8) (1-) | dE=9.3; convention is F(8926) |
| F | 8962.0(7) 1+ | `F` | 8967(8) 1+,(2-) | dE=5.0; convention is F(8967) |
| F | 9074.2(6) 1+ | `F` | 9073(10) 1+ | dE=1.2; convention is F(9073) |
| F | 9157.7(7) 1+ | `F` | 9163(10) 1+ | dE=5.3; convention is F(9163) |
| F | 9369.3(6) 1- | `F` | 9368(10) 1+,(2-) | dE=1.3; convention is F(9368) |
| F | 9458(5) 3- | `F` | 9468(10)  | dE=10.0; convention is F(9468) |
| F | 9523.7(9) 1- | `F` | 9513(10) 1+,(2-) | dE=10.7; convention is F(9513) |
| F | 9554.8(21) 1 | `F` | 9552(10) (2-) | dE=2.8; convention is F(9552) |
| G | 11497(10) (3-) | `G` | 11510(40)  | dE=13.0; convention is G(11510) |
| G | 1454.20(8) 2+ | `G` | 1459(6)  | dE=4.8; convention is G(1459) |
| G | 2459.22(12) 4+ | `G` | 2461(7)  | dE=1.8; convention is G(2461) |
| G | 2775.39(13) 2+ | `G` | 2774(9)  | dE=1.4; convention is G(2774) |
| G | 2942.54(15) 0+ | `G` | 2939(20)  | dE=3.5; convention is G(2939) |
| G | 3037.83(14) 2+ | `G` | 3037(9)  | dE=0.8; convention is G(3037) |
| G | 3263.64(18) 2+ | `G` | 3266(9)  | dE=2.4; convention is G(3266) |
| G | 3420.52(15) 3+ | `G` | 3421(20)  | dE=0.5; convention is G(3421) |
| G | 3620.10(18) 4+ | `G` | 3618(6)  | dE=2.1; convention is G(3618) |
| G | 3774.82(22) 3+ | `G` | 3773(7)  | dE=1.8; convention is G(3773) |
| G | 3898.8(4) 2+ | `G` | 3889(10)  | dE=9.8; convention is G(3889) |
| G | 4108.19(24) 2+ | `G` | 4103(10)  | dE=5.2; convention is G(4103) |
| G | 4294.86(34) 4+ | `G` | 4298(20)  | dE=3.1; convention is G(4298) |
| G | 4347.9(12)  | `G` | 4337(20)  | dE=10.9; convention is G(4337) |
| G | 4404.23(34) 4+ | `G` | 4397(8)  | dE=7.2; convention is G(4397) |
| G | 4474.6(5) 3- | `G` | 4471(20)  | dE=3.6; convention is G(4471) |
| G | 4518.3(7)  | `G` | 4515(20)  | dE=3.3; convention is G(4515) |
| G | 4752.2(7) 4+ | `G` | 4750(7)  | dE=2.2; convention is G(4750) |
| G | 5472.3(7) 4+ | `G` | 5488(11)  | dE=15.7; convention is G(5488) |
| G | 6854.5(10) 3- | `G` | 6860(40)  | dE=5.5; convention is G(6860) |
| H | 1454.20(8) 2+ | `H` | 1460  | dE=5.8; convention is H(1460) |
| H | 2459.22(12) 4+ | `H` | 2460  | dE=0.8; convention is H(2460) |
| H | 2942.54(15) 0+ | `H` | 2940  | dE=2.5; convention is H(2940) |
| H | 3037.83(14) 2+ | `H` | 3040  | dE=2.2; convention is H(3040) |
| H | 3263.64(18) 2+ | `H` | 3260  | dE=3.6; convention is H(3260) |
| H | 3620.10(18) 4+ | `H` | 3600  | dE=20.1; convention is H(3600) |
| H | 4108.19(24) 2+ | `H` | 4100  | dE=8.2; convention is H(4100) |
| H | 5590.3(10) 2+ | `H` | 5570  | dE=20.3; convention is H(5570) |
| H | 5896.4(7)  | `H` | 5890  | dE=6.4; convention is H(5890) |
| H | 7514.5(10) 3- | `H` | 7500  | dE=14.5; convention is H(7500) |
| I | 1454.20(8) 2+ | `I` | 1450  | dE=4.2; convention is I(1450) |
| I | 2459.22(12) 4+ | `I` | 2460  | dE=0.8; convention is I(2460) |
| I | 2775.39(13) 2+ | `I` | 2770  | dE=5.4; convention is I(2770) |
| I | 3037.83(14) 2+ | `I` | 3040  | dE=2.2; convention is I(3040) |
| I | 3263.64(18) 2+ | `I` | 3270  | dE=6.4; convention is I(3270) |
| I | 3593.70(19) 2+ | `I` | 3570  | dE=23.7; convention is I(3570) |
| I | 3898.8(4) 2+ | `I` | 3900  | dE=1.2; convention is I(3900) |
| I | 4108.19(24) 2+ | `I` | 4100  | dE=8.2; convention is I(4100) |
| I | 4448.91(33) 2+,1+,0+ | `I` | 4430  | dE=18.9; convention is I(4430) |
| I | 4474.6(5) 3- | `I` | 4500  | dE=25.4; convention is I(4500) |
| I | 4752.2(7) 4+ | `I` | 4750  | dE=2.2; convention is I(4750) |
| K | 1454.20(8) 2+ | `K` | 1454  | dE=0.2; convention is K(1454) |
| K | 2459.22(12) 4+ | `K` | 2459  | dE=0.2; convention is K(2459) |
| K | 2775.39(13) 2+ | `K` | 2775  | dE=0.4; convention is K(2775) |
| K | 2942.54(15) 0+ | `K` | 2943  | dE=0.5; convention is K(2943) |
| K | 3037.83(14) 2+ | `K` | 3038  | dE=0.2; convention is K(3038) |
| K | 3263.64(18) 2+ | `K` | 3264  | dE=0.4; convention is K(3264) |
| K | 3531.10(19) 0+ | `K` | 3530  | dE=1.1; convention is K(3530) |
| K | 3898.8(4) 2+ | `K` | 3890  | dE=8.8; convention is K(3890) |
| K | 4108.19(24) 2+ | `K` | 4110  | dE=1.8; convention is K(4110) |
| K | 4474.6(5) 3- | `K` | 4470  | dE=4.6; convention is K(4470) |
| K | 5127.39(29) 6+ | `K` | 5130  | dE=2.6; convention is K(5130) |
| K | 5384.5(4) 6+ | `K` | 5380  | dE=4.5; convention is K(5380) |
| K | 5588.9(7) (5-) | `K` | 5590  | dE=1.1; convention is K(5590) |
| K | 5896.4(7)  | `K` | 5890  | dE=6.4; convention is K(5890) |
| K | 6027.7(4) 1- | `K` | 6020  | dE=7.7; convention is K(6020) |
| K | 6763.5(10) 3- | `K` | 6760  | dE=3.5; convention is K(6760) |
| K | 6854.5(10) 3- | `K` | 6860  | dE=5.5; convention is K(6860) |
| K | 7210.4(10) 3- | `K` | 7230  | dE=19.6; convention is K(7230) |
| K | 7820(8) 4(+) | `K` | 7850  | dE=30.0; convention is K(7850) |
| L | 1454.20(8) 2+ | `L` | 1440(30)  | dE=14.2; convention is L(1440) |
| L | 2775.39(13) 2+ | `L` | 2820(30)  | dE=44.6; convention is L(2820) |
| L | 3524(5) 4+ | `L` | 3500(30)  | dE=24.0; convention is L(3500) |
| L | 4020  | `L` | 4050(30)  | dE=30.0; convention is L(4050) |
| L | 4474.6(5) 3- | `L` | 4470(30)  | dE=4.6; convention is L(4470) |
| L | 5064.3(10)  | `L` | 5030(30)  | dE=34.3; convention is L(5030) |
| M | 1454.20(8) 2+ | `M` | 1450 2+ | dE=4.2; convention is M(1450) |
| M | 2459.22(12) 4+ | `M` | 2450 4+ | dE=9.2; convention is M(2450) |
| M | 4574.3(5) 1 | `M` | 4600 1 | dE=25.7; convention is M(4600) |
| M | 7710.3(6) 1+ | `M` | 7700 1+ | dE=10.3; convention is M(7700) |
| N | 1454.20(8) 2+ | `N` | 1450(20) 2+ | dE=4.2; convention is N(1450) |
| N | 2459.22(12) 4+ | `N` | 2460(20) 4+ | dE=0.8; convention is N(2460) |
| N | 2775.39(13) 2+ | `N` | 2770(20) 2+ | dE=5.4; convention is N(2770) |
| N | 3263.64(18) 2+ | `N` | 3260(20) 2+ | dE=3.6; convention is N(3260) |
| N | 3420.52(15) 3+ | `N` | 3430(20) 3+ | dE=9.5; convention is N(3430) |
| N | 3531.10(19) 0+ | `N` | 3540(20) 0+ | dE=8.9; convention is N(3540) |
| N | 3774.82(22) 3+ | `N` | 3760(20) 3+ | dE=14.8; convention is N(3760) |
| N | 3898.8(4) 2+ | `N` | 3900(20) 2+ | dE=1.2; convention is N(3900) |
| N | 4108.19(24) 2+ | `N` | 4110(20) 2+ | dE=1.8; convention is N(4110) |
| N | 4294.86(34) 4+ | `N` | 4290(20) 4+ | dE=4.9; convention is N(4290) |
| N | 4474.6(5) 3- | `N` | 4470(20) 3- | dE=4.6; convention is N(4470) |
| N | 5170.3(10)  | `N` | 5220(50)  | dE=49.7; convention is N(5220) |
| N | 5594.2(6) 4+ | `N` | 5590(50) 4+ | dE=4.2; convention is N(5590) |
| N | 7210.4(10) 3- | `N` | 7.2E+3(1) 3- | dE=10.4; convention is N(7200) |
| N | 7808.4(5) 1- | `N` | 7800(50) 1- | dE=8.4; convention is N(7800) |
| O | 3531.10(19) 0+ | `O` | 3550(30)  | dE=18.9; convention is O(3550) |
| P | 1454.20(8) 2+ | `P` | 1454 2+ | dE=0.2; convention is P(1454) |
| P | 2459.22(12) 4+ | `P` | 2459 4+ | dE=0.2; convention is P(2459) |
| P | 3620.10(18) 4+ | `P` | 3619 4+ | dE=1.1; convention is P(3619) |
| P | 4382.96(26) (5+) | `P` | 4381 (5+) | dE=2.0; convention is P(4381) |
| P | 5127.39(29) 6+ | `P` | 5125 6+ | dE=2.4; convention is P(5125) |
| Q | 1454.20(8) 2+ | `Q` | 1450 2+ | dE=4.2; convention is Q(1450) |
| R | 1454.20(8) 2+ | `R` | 1454.0(10) 2+ | dE=0.2; convention is R(1454) |
| R | 7446.1(5) (9+) | `R` | 7444.5(20) (9+) | dE=1.6; convention is R(7444.5) |
| S | 1454.20(8) 2+ | `S` | 1454 2+ | dE=0.2; convention is S(1454) |
| S | 2459.22(12) 4+ | `S` | 2459 4+ | dE=0.2; convention is S(2459) |
| S | 3620.10(18) 4+ | `S` | 3619 4+ | dE=1.1; convention is S(3619) |
| S | 4382.96(26) (5+) | `S` | 4381 (5+) | dE=2.0; convention is S(4381) |
| S | 5127.39(29) 6+ | `S` | 5125 6+ | dE=2.4; convention is S(5125) |
| T | 1454.20(8) 2+ | `T` | 1454.32(10) 2+ | dE=0.1; convention is T(1454.32) |
| T | 2459.22(12) 4+ | `T` | 2459.5(5) 4+ | dE=0.3; convention is T(2459.5) |
| T | 3420.52(15) 3+ | `T` | 3421.7(7) 3+ | dE=1.2; convention is T(3421.7) |
| T | 3620.10(18) 4+ | `T` | 3619.9(6) 4+ | dE=0.2; convention is T(3619.9) |
| T | 5384.5(4) 6+ | `T` | 5384.0(7) 6+ | dE=0.5; convention is T(5384) |
| U | 1454.20(8) 2+ | `U` | 1454.4(4) 2+ | dE=0.2; convention is U(1454.4) |
| U | 2459.22(12) 4+ | `U` | 2459.5(6) 4+ | dE=0.3; convention is U(2459.5) |
| U | 3620.10(18) 4+ | `U` | 3620.7(6) 4+ | dE=0.6; convention is U(3620.7) |
| U | 4105.89(26) (4+) | `U` | 4108.0(7) 4+ | dE=2.1; convention is U(4108) |
| U | 4358.6(6) (2+,3,4+) | `U` | 4361.2(14) (5) | dE=2.6; convention is U(4361.2) |
| U | 4382.96(26) (5+) | `U` | 4383.6(6) 5+ | dE=0.6; convention is U(4383.6) |
| U | 4964.72(26) (5+) | `U` | 4963.8(14) (5)+ | dE=0.9; convention is U(4963.8) |
| U | 5127.39(29) 6+ | `U` | 5128.2(7) 6+ | dE=0.8; convention is U(5128.2) |
| U | 5384.5(4) 6+ | `U` | 5386.0(7) 6+ | dE=1.5; convention is U(5386) |
| U | 6067.5(4) (7+) | `U` | 6068.3(7) (7+) | dE=0.8; convention is U(6068.3) |
| U | 6219.9(4) (7+) | `U` | 6220.6(8) 7+ | dE=0.7; convention is U(6220.6) |
| U | 6604.5(4) (8+) | `U` | 6605.0(8) 8+ | dE=0.5; convention is U(6605) |
| U | 8120.7(4) (9+) | `U` | 8121.6(10) (9+) | dE=0.9; convention is U(8121.6) |
| V | 1454.20(8) 2+ | `V` | 1450 2+ | dE=4.2; convention is V(1450) |
| X | 1454.20(8) 2+ | `X` | 1454 2+ | dE=0.2; convention is X(1454) |
| X | 2459.22(12) 4+ | `X` | 2460  | dE=0.8; convention is X(2460) |
| X | 2775.39(13) 2+ | `X` | 2780  | dE=4.6; convention is X(2780) |
| X | 3037.83(14) 2+ | `X` | 3040  | dE=2.2; convention is X(3040) |
| X | 3263.64(18) 2+ | `X` | 3260  | dE=3.6; convention is X(3260) |
| X | 3898.8(4) 2+ | `X` | 3900  | dE=1.2; convention is X(3900) |
| X | 4752.2(7) 4+ | `X` | 4750  | dE=2.2; convention is X(4750) |
| Y | 1454.20(8) 2+ | `Y` | 1454 2+ | dE=0.2; convention is Y(1454) |
| Y | 2459.22(12) 4+ | `Y` | 2459 4+ | dE=0.2; convention is Y(2459) |
| Y | 5127.39(29) 6+ | `Y` | 5127 6+ | dE=0.4; convention is Y(5127) |
| Y | 5384.5(4) 6+ | `Y` | 5384 6+ | dE=0.5; convention is Y(5384) |
| Y | 5588.9(7) (5-) | `Y` | 5588 (5-) | dE=0.9; convention is Y(5588) |
| Y | 6067.5(4) (7+) | `Y` | 6067 (7+) | dE=0.5; convention is Y(6067) |
| Y | 6084.6(4) 7- | `Y` | 6084 7- | dE=0.6; convention is Y(6084) |
| Y | 6604.5(4) (8+) | `Y` | 6604 (8+) | dE=0.5; convention is Y(6604) |
| Z | 1454.20(8) 2+ | `Z` | 1453.5(20) 2+ | dE=0.7; convention is Z(1453.5) |
| Z | 2459.22(12) 4+ | `Z` | 2457.1(28) 4+ | dE=2.1; convention is Z(2457.1) |
| j | 1454.20(8) 2+ | `j` | 1450 2+ | dE=4.2; convention is j(1450) |
| j | 4474.6(5) 3- | `j` | 4470 3- | dE=4.6; convention is j(4470) |

### MALFORMED (3)
| 7109(8) (2+) | `XREF=F(7109*) L(*)` | embedded space |
| 7113.5(7) (1,2+) | `XREF=CF(7109*) L(*)` | embedded space |
| 9251(10) (1+) | `XREF=C(9245)(9193)F` | second '(...)' after C(9245) |
