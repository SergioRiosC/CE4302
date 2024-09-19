import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge



test_cases = [
        # we3, a1, a2, a3, wd3, expected_rd1, expected_rd2
        (1, 3, 4, 3, 0x11111111111111111111111111111111, (0x11111111111111111111111111111111, 0)),
        (1, 0, 2, 5, 0x22222222222222222222222222222222, (0, 0)),
        (1, 3, 4, 7, 0x33333333333333333333333333333333, (0x11111111111111111111111111111111, 0x00000000000000000000000000000000)),
        (0, 1, 7, 5, 0x44444444444444444444444444444444, (0, 0x33333333333333333333333333333333)),
        (1, 24, 25, 0, 0x55555555555555555555555555555555, (0, 0))
    ]

@cocotb.test()
async def register_file_test(dut):
    """Testbench para el módulo register_file"""

    # Reloj
    cocotb.start_soon(Clock(dut.clk, 20, units="ns").start())  # 20ns para 50MHz
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    

    for i, (we3, a1, a2, a3, wd3, expected) in enumerate(test_cases):
        

        # Entradas
        dut.we3.value = we3
        dut.a1.value = a1
        dut.a2.value = a2
        dut.a3.value = a3
        dut.wd3.value = wd3

        await RisingEdge(dut.clk)
        await RisingEdge(dut.clk)
        await RisingEdge(dut.clk)  
    

        (exp_rd1, exp_rd2) = expected


        # Salidas
        assert hex(dut.rd1.value) == hex(exp_rd1), \
            f"Fallo de test {i} en 'rd1', esperado: {hex(exp_rd1)}, obtenido: {hex(dut.rd1.value)}"
        assert hex(dut.rd2.value) == hex(exp_rd2), \
            f"Fallo de test {i} en 'rd2', esperado: {hex(exp_rd2)}, obtenido: {hex(dut.rd2.value)}"

        # Resetear para siguiente test
        await RisingEdge(dut.clk)
