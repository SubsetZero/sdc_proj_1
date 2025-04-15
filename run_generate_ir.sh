#!/bin/bash

pwd
cat ./filelist.lst | while read filename; do
	echo "Running LLVM frontend for example \"${filename}\""
	( cd examples/${filename}; ls; ../../src/main_flow/llvm_ir.sh )
	
done
