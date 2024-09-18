SIM = icarus
TOPLEVEL_LANG = verilog

# Incluye todos los archivos de SystemVerilog del proyecto
VERILOG_SOURCES = $(PWD)/stage_instruction_fetsch.sv 

# Define el top-level del diseño y el archivo de testbench de Python
TOPLEVEL = stage_instruction_fetsch
MODULE = test_stage_instruction_fetsch

export COCOTB_REDUCED_LOG_FMT=1
# Comandos de simulación
include $(shell cocotb-config --makefiles)/Makefile.sim
