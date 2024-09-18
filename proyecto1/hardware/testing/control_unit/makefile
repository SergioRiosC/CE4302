SIM = icarus
TOPLEVEL_LANG = verilog

# Incluye todos los archivos de SystemVerilog del proyecto
VERILOG_SOURCES = $(PWD)/control_unit.sv 

# Define el top-level del diseño y el archivo de testbench de Python
TOPLEVEL = control_unit
MODULE = test_control_unit


export COCOTB_REDUCED_LOG_FMT=1
# Comandos de simulación
include $(shell cocotb-config --makefiles)/Makefile.sim
