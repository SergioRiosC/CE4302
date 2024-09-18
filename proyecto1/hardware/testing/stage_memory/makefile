SIM = icarus
TOPLEVEL_LANG = verilog

# Incluye todos los archivos de SystemVerilog del proyecto
VERILOG_SOURCES = $(PWD)/stage_memory.sv 

# Define el top-level del diseño y el archivo de testbench de Python
TOPLEVEL = stage_memory
MODULE = test_stage_memory

export COCOTB_REDUCED_LOG_FMT=1
# Comandos de simulación
include $(shell cocotb-config --makefiles)/Makefile.sim
