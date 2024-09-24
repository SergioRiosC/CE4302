#!/bin/sh
name=escalar

compiler_dir = ../../../assembler/compiler

build: clean
	python3 gen_sbox_txt.py
	sh $(compiler_dir)/compile.sh $(name).SISA > output_files/$(name).txt
	python3 $(compiler_dir)/text2hex_mif.py -i output_files/$(name).txt \
		-o output_files/$(name)
	python3 $(compiler_dir)/text2hex_mif.py -i output_files/sbox.txt \
		-o output_files/sbox
	python3 $(compiler_dir)/text2hex_mif.py -i output_files/$rsbox.txt \
		-o output_files/rsbox


clean: 
	rm -rf output_files
	mkdir output_files