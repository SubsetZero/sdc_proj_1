\* ILP_model *\
Minimize
Objective_Function: sv_a + sv_a.addr.03 + sv_add + sv_add1 + sv_add11
 + sv_add2 + sv_add4 + sv_add6 + sv_add7 + sv_add9 + sv_b + sv_c
 + sv_c.addr.01 + sv_cmp + sv_div + sv_i.02 + sv_inc + sv_mul + sv_mul10
 + sv_mul3 + sv_mul5 + sv_mul8 + sv_n + sv_rem + sv_xor + svbr_for.body
 + svcst__add1_0 + svcst__add2_0 + svcst__add4_0 + svcst__add_0 + svcst__cmp_0
 + svcst__i.02_0 + svcst__inc_0 + svret_for.end + svssink_0 + svssink_1
 + svssink_2 + svssrc_0 + svssrc_1 + svssrc_2
Subject To
c1: - sv_a + svssink_0 >= 1
c10: sv_mul8 - sv_rem >= 1
c11: - sv_mul8 + sv_xor >= 4
c12: sv_add11 - sv_xor >= 1
c13: - sv_add11 + svssink_1 >= 1
c14: sv_add7 - sv_c.addr.01 >= 1
c15: sv_add11 - sv_c.addr.01 >= 1
c16: sv_add2 - sv_c.addr.01 >= 1
c17: sv_add6 - sv_c.addr.01 >= 1
c18: sv_add9 - sv_c.addr.01 >= 1
c19: - sv_add2 + sv_mul3 >= 1
c2: - sv_c + svssink_0 >= 1
c20: - sv_add6 + sv_div >= 1
c21: - sv_add9 + sv_mul10 >= 1
c22: - sv_mul3 + sv_mul5 >= 4
c23: - sv_mul10 + sv_xor >= 4
c24: - sv_i.02 + sv_inc >= 1
c25: sv_cmp - sv_inc >= 1
c26: - sv_cmp + svbr_for.body >= 1
c27: - svbr_for.body + svssink_1 >= 0
c28: sv_i.02 - svcst__i.02_0 >= 0
c29: - sv_add + sv_mul >= 1
c3: - sv_b + svssink_0 >= 1
c30: - sv_mul + sv_mul3 >= 4
c31: sv_add - svcst__add_0 >= 0
c32: - sv_add1 + sv_mul >= 1
c33: sv_add1 - svcst__add1_0 >= 0
c34: sv_add2 - svcst__add2_0 >= 0
c35: sv_add4 - svcst__add4_0 >= 0
c36: sv_inc - svcst__inc_0 >= 0
c37: sv_cmp - svcst__cmp_0 >= 0
c38: - svret_for.end + svssink_2 >= 1
c39: sv_a - svssrc_0 >= 0
c4: - sv_n + svssink_0 >= 1
c40: sv_c - svssrc_0 >= 0
c41: sv_b - svssrc_0 >= 0
c42: sv_n - svssrc_0 >= 0
c43: sv_a.addr.03 - svssrc_1 >= 0
c44: sv_c.addr.01 - svssrc_1 >= 0
c45: svcst__i.02_0 - svssrc_1 >= 0
c46: svcst__add_0 - svssrc_1 >= 0
c47: svcst__add1_0 - svssrc_1 >= 0
c48: svcst__add2_0 - svssrc_1 >= 0
c49: svcst__add4_0 - svssrc_1 >= 0
c5: - sv_a.addr.03 + sv_add4 >= 1
c50: svcst__inc_0 - svssrc_1 >= 0
c51: svcst__cmp_0 - svssrc_1 >= 0
c52: svret_for.end - svssrc_2 >= 0
c53: sv_a.addr.03 - sv_rem >= -18
c54: - sv_add11 + sv_c.addr.01 >= -18
c55: sv_i.02 - sv_inc >= -18
c6: - sv_add4 + sv_mul5 >= 1
c7: sv_div - sv_mul5 >= 4
c8: sv_add7 - sv_div >= 1
c9: - sv_add7 + sv_rem >= 1
Bounds
 sv_a free
 sv_a.addr.03 free
 sv_add free
 sv_add1 free
 sv_add11 free
 sv_add2 free
 sv_add4 free
 sv_add6 free
 sv_add7 free
 sv_add9 free
 sv_b free
 sv_c free
 sv_c.addr.01 free
 sv_cmp free
 sv_div free
 sv_i.02 free
 sv_inc free
 sv_mul free
 sv_mul10 free
 sv_mul3 free
 sv_mul5 free
 sv_mul8 free
 sv_n free
 sv_rem free
 sv_xor free
 svbr_for.body free
 svcst__add1_0 free
 svcst__add2_0 free
 svcst__add4_0 free
 svcst__add_0 free
 svcst__cmp_0 free
 svcst__i.02_0 free
 svcst__inc_0 free
 svret_for.end free
 svssink_0 free
 svssink_1 free
 svssink_2 free
 0 <= svssrc_0
 0 <= svssrc_1
 0 <= svssrc_2
Generals
sv_a
sv_a.addr.03
sv_add
sv_add1
sv_add11
sv_add2
sv_add4
sv_add6
sv_add7
sv_add9
sv_b
sv_c
sv_c.addr.01
sv_cmp
sv_div
sv_i.02
sv_inc
sv_mul
sv_mul10
sv_mul3
sv_mul5
sv_mul8
sv_n
sv_rem
sv_xor
svbr_for.body
svcst__add1_0
svcst__add2_0
svcst__add4_0
svcst__add_0
svcst__cmp_0
svcst__i.02_0
svcst__inc_0
svret_for.end
svssink_0
svssink_1
svssink_2
svssrc_0
svssrc_1
svssrc_2
End
