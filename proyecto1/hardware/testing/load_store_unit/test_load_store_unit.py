import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

# Definir casos de prueba
test_cases = [
    # (reset, vector_op, base_addr, in_writedata, in_readdata, expected_stall, expected_mem_addr, expected_out_readdata, expected_out_writedata)
    (1, 0, 0x1000, 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF, 0x12345678, 0, 0x1000, 0x12345678, 0xFFFFFFFF),
    (0, 1, 0x2000, 0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA, 0x87654321, 1, 0x2000, 0x87654321, 0xAAAAAAAA),
    (0, 1, 0x2000, 0xBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB, 0x12345678, 1, 0x2008, 0x87654321, 0xBBBBBBBB),
    (0, 0, 0x3000, 0xCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC, 0x87654321, 0, 0x3000, 0x87654321123456781234567887654321, 0xCCCCCCCC),
]

@cocotb.test()
async def load_store_unit_test(dut):
    """Testbench para la unidad de carga/almacenamiento"""
    
    # Reloj
    cocotb.start_soon(Clock(dut.clk, 20, units="ns").start())  # 20ns para 50MHz

    # Tiempos para reset se estabilice
    
    dut.reset.value = 1
    await RisingEdge(dut.clk)  
    await RisingEdge(dut.clk)  

    dut.reset.value = 0
    await RisingEdge(dut.clk)



    for i,(case) in enumerate(test_cases):
        reset, vector_op, base_addr, in_writedata, in_readdata, expected_stall, expected_mem_addr, expected_out_readdata, expected_out_writedata = case

        # Entradas
        dut.reset.value = reset
        dut.vector_op.value = vector_op
        dut.base_addr.value = base_addr
        dut.in_writedata.value = in_writedata
        dut.in_readdata.value = in_readdata

        
        await RisingEdge(dut.clk)

        
        # Salidas
        assert dut.stall.value == expected_stall, \
            f"Fallo en test {i} 'stall', esperado: {expected_stall}, obtenido: {dut.stall.value}"

        assert dut.current_mem_addr.value == expected_mem_addr, \
            f"Fallo en test {i} 'current_mem_addr', esperado: {expected_mem_addr}, obtenido: {dut.current_mem_addr.value}"

        assert dut.out_readdata.value == expected_out_readdata, \
            f"Fallo en test {i} 'out_readdata', esperado: {expected_out_readdata}, obtenido: {hex(dut.out_readdata.value)}"

        assert dut.out_writedata.value == expected_out_writedata, \
            f"Fallo en test {i} 'out_writedata', esperado: {expected_out_writedata}, obtenido: {dut.out_writedata.value}"

        # Resetear para siguiente test
        await RisingEdge(dut.clk)
