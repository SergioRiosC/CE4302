import cocotb
from cocotb.regression import TestFactory

@cocotb.coroutine
def alu_tb(dut):
    """Testbench for the ALU module."""
    
    # Initialize inputs
    dut.op1 <= 0
    dut.op2 <= 0
    dut.alu_control <= 0
    
    # Wait for a few clock cycles to ensure stable inputs
    yield cocotb.generators.wait(10)
    
    # Apply test cases
    test_cases = [
        # Overflow en Suma
        {"op1": 102, "op2": 102, "alu_control": 0, "expected_result": 0, "expected_overflow": 1},  # ALU_OP_SUM
        
        # Carry en Suma
        {"op1": 255, "op2": 1, "alu_control": 0, "expected_result": 0, "expected_carry": 1},  # ALU_OP_SUM
        
        # Zero en Suma
        {"op1": 1, "op2": -1, "alu_control": 0, "expected_result": 0, "expected_zero": 1},  # ALU_OP_SUM
        
        # Negativo en Suma
        {"op1": -128, "op2": 1, "alu_control": 0, "expected_result": 0, "expected_negative": 1},  # ALU_OP_SUM
        
        # Overflow en Resta
        {"op1": 0, "op2": -128, "alu_control": 1, "expected_result": 128, "expected_overflow": 1},  # ALU_OP_DIF
        
        # Zero en Operaciones Lógicas
        {"op1": 0, "op2": 0, "alu_control": 2, "expected_result": 0, "expected_zero": 1},  # ALU_OP_AND
        
        # Negativo en Operaciones Lógicas
        {"op1": -1, "op2": 1, "alu_control": 2, "expected_result": 1, "expected_negative": 1},  # ALU_OP_AND
    ]

    for test in test_cases:
        dut.op1 <= test["op1"]
        dut.op2 <= test["op2"]
        dut.alu_control <= test["alu_control"]
        
        # Wait for the result to settle
        yield cocotb.generators.wait(10)

        assert dut.result == test["expected_result"], \
            f"Failed for op1={test['op1']} op2={test['op2']} alu_control={test['alu_control']}. Expected {test['expected_result']}, got {dut.result}"

        assert dut.flags[3] == test.get("expected_overflow", 0), \
            f"Failed overflow flag for op1={test['op1']} op2={test['op2']} alu_control={test['alu_control']}"

        assert dut.flags[2] == test.get("expected_carry", 0), \
            f"Failed carry flag for op1={test['op1']} op2={test['op2']} alu_control={test['alu_control']}"

        assert dut.flags[1] == test.get("expected_zero", 0), \
            f"Failed zero flag for op1={test['op1']} op2={test['op2']} alu_control={test['alu_control']}"

        assert dut.flags[0] == test.get("expected_negative", 0), \
            f"Failed negative flag for op1={test['op1']} op2={test['op2']} alu_control={test['alu_control']}"
