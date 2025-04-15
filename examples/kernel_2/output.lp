\* ILP_model *\
Minimize
Objective_Function: sv_a + sv_a.addr.0 + sv_b + sv_c + sv_cmp + sv_div
 + sv_mul + sv_mul1 + sv_mul2 + sv_mul3 + sv_mul4 + sv_n + sv_rem + sv_xor
 + svbr_entry + svcst__mul1_0 + svret_if.end + svssink_0 + svssink_1
 + svssink_2 + svssink_3 + svssrc_0 + svssrc_1 + svssrc_2 + svssrc_3
Subject To
c1: - sv_a.addr.0 + sv_xor >= 1
c10: - sv_b + sv_mul >= 1
c11: - sv_a + sv_mul >= 1
c12: - svbr_entry + svssink_0 >= 0
c13: sv_mul1 - svcst__mul1_0 >= 0
c14: sv_cmp - sv_n >= 1
c15: - sv_c + svssink_0 >= 1
c16: sv_div - sv_mul2 >= 4
c17: - sv_div + svssink_1 >= 1
c18: sv_a.addr.0 - svssrc_3 >= 0
c19: sv_mul4 - svssrc_3 >= 0
c2: - sv_xor + svret_if.end >= 1
c20: sv_b - svssrc_0 >= 0
c21: sv_a - svssrc_0 >= 0
c22: svcst__mul1_0 - svssrc_0 >= 0
c23: sv_n - svssrc_0 >= 0
c24: sv_c - svssrc_0 >= 0
c25: sv_mul3 - svssrc_2 >= 0
c26: sv_mul2 - svssrc_1 >= 0
c27: - sv_mul + sv_mul1 >= 1
c28: - sv_mul + sv_mul1 >= 1
c29: - sv_mul + sv_mul1 >= 1
c3: - svret_if.end + svssink_3 >= 1
c30: - sv_mul + sv_mul1 >= 1
c31: - sv_mul + sv_mul1 >= 1
c32: - sv_mul + sv_mul1 >= 1
c33: - sv_mul + sv_mul1 >= 1
c34: - sv_mul + sv_mul1 >= 1
c35: - sv_mul + sv_mul1 >= 1
c36: - sv_mul + sv_mul1 >= 1
c37: - sv_mul + sv_mul1 >= 1
c4: - sv_mul4 + sv_xor >= 4
c5: - sv_mul3 + sv_rem >= 4
c6: - sv_rem + svssink_2 >= 1
c7: - sv_mul + sv_mul1 >= 4
c8: sv_cmp - sv_mul1 >= 4
c9: - sv_cmp + svbr_entry >= 1
Bounds
 sv_a free
 sv_a.addr.0 free
 sv_b free
 sv_c free
 sv_cmp free
 sv_div free
 sv_mul free
 sv_mul1 free
 sv_mul2 free
 sv_mul3 free
 sv_mul4 free
 sv_n free
 sv_rem free
 sv_xor free
 svbr_entry free
 svcst__mul1_0 free
 svret_if.end free
 svssink_0 free
 svssink_1 free
 svssink_2 free
 svssink_3 free
 0 <= svssrc_0
 0 <= svssrc_1
 0 <= svssrc_2
 0 <= svssrc_3
Generals
sv_a
sv_a.addr.0
sv_b
sv_c
sv_cmp
sv_div
sv_mul
sv_mul1
sv_mul2
sv_mul3
sv_mul4
sv_n
sv_rem
sv_xor
svbr_entry
svcst__mul1_0
svret_if.end
svssink_0
svssink_1
svssink_2
svssink_3
svssrc_0
svssrc_1
svssrc_2
svssrc_3
End
