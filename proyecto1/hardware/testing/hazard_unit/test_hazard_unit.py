import cocotb
from cocotb.triggers import Timer
from cocotb.result import TestFailure

@cocotb.test()
async def hazard_unit_test(dut):
    """Test para la unidad de hazards"""

    # Definir los casos de prueba
    test_cases = [
        # Formato:
        #reset,de_rs1,de_rs2,ex_rs1,ex_rs2,ex_rd,ex_pc_src,ex_result_src,mem_rd,mem_reg_write,wb_rd,wb_reg_write,stall_all(if_stall,de_stall,ex_stall,mem_stall,wb_stall,de_flush,ex_flush,ex_op1_forward, ex_op2_forward)
        (0,         5,     6,     5,     6,    3,        0,         0b01,     3,            1,    0,           0,      0, (       0,       0,       0,        0,       0,       0,     0,     0b00,          0b00)),  # 0 Hazard con load-use
        (1,         5,     6,     5,     6,    3,        0,         0b00,     3,            1,    0,           0,      0, (       1,       1,       1,        1,       1,       1,     1,     0b00,          0b00)),  # 1 Reset activo
        (0,         5,     6,     5,     6,    3,        1,         0b00,     0,            0,    0,           0,      0, (       0,       0,       0,        0,       0,       1,     1,     0b00,          0b00)),  # 2 ex_pc_src activa el flush
        (0,         0,     0,     5,     6,    3,        0,         0b00,     3,            1,    0,           1,      0, (       0,       0,       0,        0,       0,       0,     0,     0b00,          0b00)),  # 3 Adelantamiento desde MEM
        (0,         5,     6,     5,     6,    3,        0,         0b01,     3,            1,    3,           1,      0, (       0,       0,       0,        0,       0,       0,     0,     0b00,          0b00)),  # 4 Hazard + adelanto desde WB y MEM
        (0,         0,     0,     5,     6,    3,        0,         0b00,     3,            1,    3,           0,      1, (       1,       1,       1,        1,       1,       0,     0,     0b00,          0b00))   # 5 stall_all activo
    ]
    for i, (reset, de_rs1, de_rs2, ex_rs1, ex_rs2, ex_rd, ex_pc_src, ex_result_src, mem_rd, mem_reg_write, wb_rd, wb_reg_write, stall_all, expected) in enumerate(test_cases):
       # Entradas
        dut.reset.value = reset
        dut.de_rs1.value = de_rs1
        dut.de_rs2.value = de_rs2
        dut.ex_rs1.value = ex_rs1
        dut.ex_rs2.value = ex_rs2
        dut.ex_rd.value = ex_rd
        dut.ex_pc_src.value = ex_pc_src
        dut.ex_result_src.value = ex_result_src
        dut.mem_rd.value = mem_rd
        dut.mem_reg_write.value = mem_reg_write
        dut.wb_rd.value = wb_rd
        dut.wb_reg_write.value = wb_reg_write
        dut.stall_all.value = stall_all

        # Esperar a que las señales se propaguen
        await Timer(2, units='ns')

        # Salidas esperadas
        (exp_if_stall, exp_de_stall, exp_ex_stall, exp_mem_stall, exp_wb_stall, exp_de_flush, exp_ex_flush, exp_ex_op1_forward, exp_ex_op2_forward) = expected

        # Comparacion de resultados
        assert dut.if_stall.value == exp_if_stall, \
            f"Error en if_stall en test {i}, esperado {exp_if_stall}, obtenido {dut.if_stall.value}"

        assert dut.de_stall.value == exp_de_stall, \
            f"Error en de_stall en test {i}, esperado {exp_de_stall}, obtenido {dut.de_stall.value}"

        assert dut.ex_stall.value == exp_ex_stall, \
            f"Error en ex_stall en test {i}, esperado {exp_ex_stall}, obtenido {dut.ex_stall.value}"

        assert dut.mem_stall.value == exp_mem_stall, \
            f"Error en mem_stall en test {i}, esperado {exp_mem_stall}, obtenido {dut.mem_stall.value}"

        assert dut.wb_stall.value == exp_wb_stall, \
            f"Error en wb_stall en test {i}, esperado {exp_wb_stall}, obtenido {dut.wb_stall.value}"

        assert dut.de_flush.value == exp_de_flush, \
            f"Error en de_flush en test {i}, esperado {exp_de_flush}, obtenido {dut.de_flush.value}"

        assert dut.ex_flush.value == exp_ex_flush, \
            f"Error en ex_flush en test {i}, esperado {exp_ex_flush}, obtenido {dut.ex_flush.value}"

        assert dut.ex_op1_forward.value == exp_ex_op1_forward, \
            f"Error en ex_op1_forward en test {i}, esperado {exp_ex_op1_forward}, obtenido {dut.ex_op1_forward.value}"

        assert dut.ex_op2_forward.value == exp_ex_op2_forward, \
            f"Error en ex_op2_forward en test {i}, esperado {exp_ex_op2_forward}, obtenido {dut.ex_op2_forward.value}"
            

        dut._log.info(f"Test {i} pasado con reset={reset}, de_rs1={de_rs1}, ex_rs1={ex_rs1}, ex_rd={ex_rd}, mem_rd={mem_rd}, wb_rd={wb_rd}, stall_all={stall_all}")
