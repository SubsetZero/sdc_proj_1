############################################################################################################################################
############################################################################################################################################
#
#	REGEX
#
############################################################################################################################################
#	INFO:
#				 The complete list of instruction syntax is at https://llvm.org/docs/LangRef.html#instruction-reference
############################################################################################################################################
#	LIST REGEX:
#				- common regex (fast_math_flags, iarith_flags)
#				- binary_instructions : regex for 2-input 1-output operators
#				- unary_instructions : regex for 1-input 1-output operators
#				- memory_instructions : regex for memory operators
#				- control_instructions : regex for control operations
#				- all_regex_instructions : regex containing all instruction types
############################################################################################################################################
############################################################################################################################################


# common regex
fast_math_flags = r'(nnan )?(ninf )?(nsz )?(arcp )?(contract )?(afn )?(reassoc )?(fast )?'
iarith_flags    = r'(nuw )?(nsw )?'

# regex for 2-input 1-output operators
binary_instructions = {
	'add':  r'(\S+) = add '  + iarith_flags + '(\S+) (\S+), (\S+)',    # <result> = add nuw nsw <ty> <op1>, <op2>  ; yields ty:result
	'fadd': r'(\S+) = fadd ' + fast_math_flags + '(\S+) (\S+), (\S+)', 
	'sub':  r'(\S+) = sub '  + iarith_flags + '(\S+) (\S+), (\S+)',    
	'mul':  r'(\S+) = mul '  + iarith_flags + '(\S+) (\S+), (\S+)',    
	'fmul': r'(\S+) = fmul ' + fast_math_flags + '(\S+) (\S+), (\S+)', 
	'udiv': r'(\S+) = udiv ' + r'(exact )?' + '(\S+) (\S+), (\S+)', 
	'sdiv': r'(\S+) = sdiv ' + r'(exact )?' + '(\S+) (\S+), (\S+)', 
	'fdiv': r'(\S+) = fdiv ' + fast_math_flags + '(\S+) (\S+), (\S+)', 
	'urem': r'(\S+) = urem (\S+) (\S+), (\S+)', 
	'srem': r'(\S+) = srem (\S+) (\S+), (\S+)', 
	'frem': r'(\S+) = frem ' + fast_math_flags + '(\S+) (\S+), (\S+)', 
	'shl':  r'(\S+) = shl ' + r'(exact )?' + '(\S+) (\S+), (\S+)',    
	'lshr':  r'(\S+) = lshr ' + r'(exact )?' + '(\S+) (\S+), (\S+)',    
	'ashr':  r'(\S+) = ashr ' + r'(exact )?' + '(\S+) (\S+), (\S+)',    
	'and':   r'(\S+) = and (\S+) (\S+), (\S+)', 
	'or':   r'(\S+) = or (\S+) (\S+), (\S+)', 
	'xor':   r'(\S+) = xor (\S+) (\S+), (\S+)', 
	'icmp': r'(\S+) = icmp (\S+) (\S+) (\S+), (\S+)'                   # <result> = icmp <cond> <ty> <op1>, <op2>   ; yields i1 or <N x i1>:result
}

# regex for 1-input 1-output operators
unary_instructions = {
	'fneg': r'(\S+) = fneg ' + fast_math_flags + '(\S+) (\S+)',        # <result> = fneg float %val          ; yields float:result = -%var
	'zext': r'(\S+) = zext (\S+) (\S+) to (\S+)',
	'sext': r'(\S+) = sext (\S+) (\S+) to (\S+)'
}

# regex for memory operators
memory_instructions = {
	'load':  r'(\S+) = load (volatile )?(\S+), (\S+) ([\w%]+),?\s?(align \S+)?,?\s?',
	'store': r'store (volatile )?(\S+) (\S+), (\S+) ([\w%]+),?\s?(align \S+)?,?\s?',
	'getelementptr': r'(\S+) = getelementptr inbounds (\S+), (\S+) (\S+), (\S+) (\S+)' #<result> = getelementptr inbounds <ty>, ptr <ptrval>{, [inrange] <ty> <idx>}*
}

# regex for control operations
control_instructions = {
	'ret':  r'ret (\S+)? (\S+)',                                       # ret <type> <value> ; Return a value from a non-void function
	'br':   r'br i1 (\S+), label (\S+), label (\S+)',                  # br i1 <cond>, label <iftrue>, label <iffalse>
	'jmp':   r'label (\S+)',                                            # br label <dest>          ; Unconditional branch
	'phi': r'(\S+) = phi ' + fast_math_flags + '(\S+) (\[ \S+, \S+ \]),?\s?(\[ \S+, \S+ \])?'
}

# regex containing all instruction types
all_regex_instructions = { **binary_instructions, **unary_instructions, **memory_instructions, **control_instructions}
