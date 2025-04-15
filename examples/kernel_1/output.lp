\* ILP_model *\
Minimize
Objective_Function: sv_a + sv_a.addr.0 + sv_add + sv_add7 + sv_b + sv_c
 + sv_c.addr.0 + sv_cmp + sv_div + sv_mul + sv_mul1 + sv_mul2 + sv_mul4
 + sv_mul9 + sv_n + sv_rem + sv_shr + sv_shr3 + sv_shr6 + sv_shr8 + sv_sub
 + svbr_entry + svret_if.end + svssink_0 + svssink_1 + svssink_2 + svssrc_0
 + svssrc_1 + svssrc_2
Subject To
c1: - sv_c.addr.0 + sv_shr8 >= 1
c10: - sv_shr6 + svssink_1 >= 1
c11: - sv_add + sv_mul >= 1
c12: - sv_mul + sv_shr >= 4
c13: sv_mul1 - sv_shr >= 1
c14: sv_add - sv_b >= 1
c15: - sv_b + sv_sub >= 1
c16: - sv_b + sv_mul2 >= 1
c17: sv_cmp - sv_sub >= 1
c18: sv_div - sv_mul2 >= 4
c19: - sv_cmp + svbr_entry >= 1
c2: sv_mul9 - sv_shr8 >= 1
c20: - sv_div + sv_rem >= 1
c21: - sv_a + sv_add >= 1
c22: - sv_mul1 + sv_sub >= 4
c23: sv_mul - sv_n >= 1
c24: sv_div - sv_n >= 1
c25: sv_cmp - sv_rem >= 1
c26: - sv_c + sv_shr >= 1
c27: - sv_c + sv_mul2 >= 1
c28: - sv_c + sv_mul1 >= 1
c29: - sv_c + sv_rem >= 1
c3: - sv_mul9 + svret_if.end >= 4
c30: - svbr_entry + svssink_0 >= 0
c31: sv_c.addr.0 - svssrc_2 >= 0
c32: sv_a.addr.0 - svssrc_2 >= 0
c33: sv_shr3 - svssrc_1 >= 0
c34: sv_b - svssrc_0 >= 0
c35: sv_a - svssrc_0 >= 0
c36: sv_n - svssrc_0 >= 0
c37: sv_c - svssrc_0 >= 0
c38: sv_mul - sv_mul2 >= 1
c39: - sv_mul + sv_mul1 >= 1
c4: - sv_a.addr.0 + sv_add7 >= 1
c40: sv_mul - sv_mul2 >= 1
c41: - sv_mul + sv_mul1 >= 1
c42: sv_mul - sv_mul2 >= 1
c43: - sv_mul + sv_mul1 >= 1
c44: sv_mul - sv_mul2 >= 1
c45: - sv_mul + sv_mul1 >= 1
c46: sv_mul - sv_mul2 >= 1
c47: - sv_mul + sv_mul1 >= 1
c48: sv_mul - sv_mul2 >= 1
c49: - sv_mul + sv_mul1 >= 1
c5: - sv_add7 + sv_mul9 >= 1
c50: sv_mul - sv_mul2 >= 1
c51: - sv_mul + sv_mul1 >= 1
c52: sv_mul - sv_mul2 >= 1
c53: - sv_mul + sv_mul1 >= 1
c54: sv_mul - sv_mul2 >= 1
c55: - sv_mul + sv_mul1 >= 1
c56: sv_mul - sv_mul2 >= 1
c57: - sv_mul + sv_mul1 >= 1
c58: sv_mul - sv_mul2 >= 1
c59: - sv_mul + sv_mul1 >= 1
c6: - svret_if.end + svssink_2 >= 1
c60: sv_mul - sv_mul2 >= 1
c61: - sv_mul + sv_mul1 >= 1
c62: sv_mul - sv_mul2 >= 1
c63: - sv_mul + sv_mul1 >= 1
c64: sv_mul - sv_mul2 >= 1
c65: - sv_mul + sv_mul1 >= 1
c66: sv_mul - sv_mul2 >= 1
c67: - sv_mul + sv_mul1 >= 1
c68: sv_mul - sv_mul2 >= 1
c69: - sv_mul + sv_mul1 >= 1
c7: sv_mul4 - sv_shr3 >= 1
c8: - sv_shr3 + sv_shr6 >= 1
c9: - sv_mul4 + svssink_1 >= 4
Bounds
 sv_a free
 sv_a.addr.0 free
 sv_add free
 sv_add7 free
 sv_b free
 sv_c free
 sv_c.addr.0 free
 sv_cmp free
 sv_div free
 sv_mul free
 sv_mul1 free
 sv_mul2 free
 sv_mul4 free
 sv_mul9 free
 sv_n free
 sv_rem free
 sv_shr free
 sv_shr3 free
 sv_shr6 free
 sv_shr8 free
 sv_sub free
 svbr_entry free
 svret_if.end free
 svssink_0 free
 svssink_1 free
 svssink_2 free
 0 <= svssrc_0
 0 <= svssrc_1
 0 <= svssrc_2
Generals
sv_a
sv_a.addr.0
sv_add
sv_add7
sv_b
sv_c
sv_c.addr.0
sv_cmp
sv_div
sv_mul
sv_mul1
sv_mul2
sv_mul4
sv_mul9
sv_n
sv_rem
sv_shr
sv_shr3
sv_shr6
sv_shr8
sv_sub
svbr_entry
svret_if.end
svssink_0
svssink_1
svssink_2
svssrc_0
svssrc_1
svssrc_2
End
