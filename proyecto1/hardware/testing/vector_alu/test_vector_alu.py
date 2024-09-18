import cocotb
from cocotb.triggers import RisingEdge, FallingEdge
from cocotb.clock import Clock
from cocotb.result import TestFailure

# Definimos el test principal
@cocotb.test()
async def test_top(dut):
    """ Test básico para verificar el comportamiento del reset y el clock """

    # Inicializamos el reloj a 50 MHz
    cocotb.start_soon(Clock(dut.CLOCK_50, 20, units="ns").start())  # 20ns para 50MHz

    # Inicializamos el reset
    dut.SW[0].value = 1  # Reset activado
    dut.SW[1].value = 0  # Modo normal (sin debug)
    
    # Esperamos algunos ciclos de reloj con reset activado
    for _ in range(5):
        await RisingEdge(dut.CLOCK_50)
    
    # Desactivamos el reset
    dut.SW[0].value = 0

    # Verificamos que la señal addr[0] reflejada en LEDR[0] cambie con el tiempo
    previous_ledr = dut.LEDR[0].value
    for _ in range(10):  # Verificamos durante algunos ciclos de reloj
        await RisingEdge(dut.CLOCK_50)
        current_ledr = dut.LEDR[0].value

        if current_ledr != previous_ledr:
            dut._log.info(f"LEDR[0] cambió: {previous_ledr} -> {current_ledr}")
        previous_ledr = current_ledr

    # Si no hubo cambios, fallamos la prueba
    if previous_ledr == dut.LEDR[0].value:
        raise TestFailure("LEDR[0] no cambió durante la simulación")

    dut._log.info("Prueba completada con éxito.")
