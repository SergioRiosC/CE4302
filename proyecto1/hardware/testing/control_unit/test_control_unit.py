import cocotb
from cocotb.triggers import Timer
from cocotb.result import TestFailure

@cocotb.test()
async def control_unit_test(dut):
    """Test para la unidad de control"""

    # Casos de prueba: 
    test_cases = [
       #Formato
       #(op,    func3,        func11,  (reg_write, mem_write, mem_read, jump, jump_cond, alu_control, imm_src, result_src, vector_op))
        (0b000, 0b000, 0b00000000000, (1,                  0,        0,    0,         0,      0b0000,  0b0000,       0b00,         0)),#0 OP_A
        (0b001, 0b000, 0b00000000000, (1,                  0,        0,    0,         0,      0b0000,  0b0000,       0b00,         0)),#1 OP_B
        (0b001, 0b101, 0b00000000000, (1,                  0,        0,    0,         0,      0b0101,  0b0001,       0b00,         0)),#2 OP_B
        (0b010, 0b000, 0b00000000000, (0,                  1,        0,    0,         0,      0b0000,  0b0100,       0b00,         0)),#3 OP_C
        (0b010, 0b100, 0b00000000000, (0,                  1,        0,    0,         0,      0b0000,  0b0100,       0b00,         1)),#8 OP_C
        (0b011, 0b010, 0b00000000000, (1,                  0,        0,    1,         0,      0b0000,  0b1100,       0b10,         0)),#4 OP_D
        (0b100, 0b000, 0b00000000000, (1,                  0,        0,    0,         0,      0b0000,  0b0000,       0b00,         0)),#5 OP_E
        (0b101, 0b000, 0b00000000000, (1,                  0,        1,    0,         0,      0b0000,  0b0000,       0b01,         0)),#6 OP_F
        (0b110, 0b000, 0b00000000000, (0,                  0,        0,    0,         1,      0b0001,  0b1000,       0b00,         0)),#7 OP_G
    ]

    for i, (op, func3, func11, expected) in enumerate(test_cases):
        dut.op.value = op
        dut.func3.value = func3
        dut.func11.value = func11

        # Esperar a que las señales se propaguen
        await Timer(2, units='ns')

        # Comparacion de resultados 
        (exp_reg_write, exp_mem_write, exp_mem_read, exp_jump, exp_jump_cond, exp_alu_control, exp_imm_src, exp_result_src, exp_vector_op) = expected

        assert dut.reg_write.value == exp_reg_write, \
              f"Error en reg_write en test {i}, esperado {exp_reg_write}, obtenido {dut.reg_write.value}"
        
        assert dut.mem_write.value == exp_mem_write, \
            f"Error en mem_write en test {i}, esperado {exp_mem_write}, obtenido {dut.mem_write.value}"
        
        assert dut.mem_read.value == exp_mem_read, \
            f"Error en mem_read en test {i}, esperado {exp_mem_read}, obtenido {dut.mem_read.value}"
        
        assert dut.jump.value == exp_jump, \
            f"Error en jump en test {i}, esperado {exp_jump}, obtenido {dut.jump.value}"
        
        assert dut.jump_cond.value == exp_jump_cond, \
            f"Error en jump_cond en test {i}, esperado {exp_jump_cond}, obtenido {dut.jump_cond.value}"
        
        assert dut.alu_control.value == exp_alu_control, \
            f"Error en alu_control en test {i}, esperado {exp_alu_control}, obtenido {dut.alu_control.value}"
        
        assert dut.imm_src.value == exp_imm_src, \
            f"Error en imm_src en test {i}, esperado {exp_imm_src}, obtenido {dut.imm_src.value}"
        
        assert dut.result_src.value == exp_result_src, \
            f"Error en result_src en test {i}, esperado {exp_result_src}, obtenido {dut.result_src.value}"
        
        assert dut.vector_op.value == exp_vector_op, \
            f"Error en vector_op en test {i}, esperado {exp_vector_op}, obtenido {dut.vector_op.value}"

        dut._log.info(f"Test {i} pasado con op={op}, func3={func3}, func11={func11}")
