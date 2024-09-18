SIM = icarus
TOPLEVEL_LANG = verilog

# Incluye todos los archivos de SystemVerilog del proyecto
VERILOG_SOURCES = $(PWD)/register_file.sv 

# Define el top-level del diseño y el archivo de testbench de Python
TOPLEVEL = register_file
MODULE = test_register_file

export COCOTB_REDUCED_LOG_FMT=1
# Comandos de simulación
include $(shell cocotb-config --makefiles)/Makefile.sim
