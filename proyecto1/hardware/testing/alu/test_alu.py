import cocotb
from cocotb.triggers import Timer

def calculate_overflow(op1, op2, result, alu_control):
    # Convertir a 32 bits
    op1 = op1 & 0xFFFFFFFF
    op2 = op2 & 0xFFFFFFFF
    result = result & 0xFFFFFFFF

    # Extraer los bits de signo (bit 31, o WIDTH-1)
    sign_op1 = (op1 >> 31) & 1
    sign_op2 = (op2 >> 31) & 1
    sign_result = (result >> 31) & 1

    # alu_control[0] en Python: solo necesitamos el bit 0
    alu_control_0 = alu_control & 1

    # Cálculo del overflow replicando la fórmula en Verilog
    overflow = not (alu_control_0 ^ sign_op1 ^ sign_op2) and (sign_op1 ^ sign_result)

    # Devolver 1 si hay overflow, 0 si no lo hay
    return 1 if overflow else 0

# Alu auxiliar
def alu_aux(op1, op2, alu_control):
    if alu_control == 0b0000:  # Suma
        result = op1 + op2
        carry = (result >> 32) & 1
        result = result & 0xFFFFFFFF  # Se toman los 32 bits inferiores
        
    elif alu_control == 0b0001:  # Resta
        result = op1 - op2
        if op1 - op2 < 0:
            
            result = (1 << 32) + (op1 - op2)
            
            result= (op1 - op2) & ((1 << 32) - 1)



        
        #overflow = 1 if ((op1 & 0x80000000 != op2 & 0x80000000) and (result & 0x80000000 != op1 & 0x80000000)) else 0
        carry = 1 if op1 >= op2 else 0
    elif alu_control == 0b0010:  # AND
        result = op1 & op2
        carry = 0
        
    elif alu_control == 0b0011:  # OR
        result = op1 | op2
        carry = 0
        
    elif alu_control == 0b0100:  # XOR
        result = op1 ^ op2
        carry = 0
        
    elif alu_control == 0b0101:  # Shift Logical Left
        result = op1 << op2
        carry = (result >> 32) & 1
        result = result & 0xFFFFFFFF
        
    elif alu_control == 0b0110:  # Shift Logical Right
        result = op1 >> op2
        carry = op1 & 1
        
    elif alu_control == 0b0111:  # Shift Arithmetic Right
        result = op1 >> op2 if op1 >= 0 else ((op1 + 0x100000000) >> op2)
        carry = op1 & 1
        
    elif alu_control == 0b1000:  # Multiplicacion
        result = op1 * op2
        carry = (result >> 32) & 1
        
        result = result & 0xFFFFFFFF
    else:
        result = 0
        carry = 0
    #Comprobacion de flags
    zero = 1 if result == 0 else 0
    negative = 1 if result <0 else 0
    overflow = calculate_overflow(op1, op2, result, alu_control)
     

    return result, carry, zero, negative, overflow

@cocotb.test()
async def alu_test(dut):
    """Test para la ALU"""

    # Sincronización inicial
    await Timer(2,units="ns")

    # Casos de prueba
    test_cases = [
        (57, 40, 0b0000),  # Suma
        (24, 56, 0b0001),  # Resta
        (1110101010, 0x0011100010, 0b0010),  # AND
        (0x0011100010, 0x1110101010, 0b0011),  # OR
        (0x1110101010, 0x0011100010, 0b0100),  # XOR
        (0x00101001, 0x00000110, 0b0101),  # Shift Logical Left
        (0x00001010, 0x00000101, 0b0110),  # Shift Logical Right
  
        (71, -24, 0b1000),  # Multiplicación
    ]

    # Iterar sobre cada operación y probar
    for op1, op2, alu_control in test_cases:
        # Asignar valores de entrada
        dut.op1.value = op1
        dut.op2.value = op2
        dut.alu_control.value = alu_control

        # Esperar un ciclo de reloj para que la ALU procese
        await Timer(2,units="ns")

        # Obtener los valores simulados desde el módulo Verilog
        dut_result = int(dut.result.value)
        #dut_flags = int(dut.flags.value)

        # Modelo de referencia para comparar
        model_result, model_carry, model_zero, model_negative, model_overflow = alu_aux(op1, op2, alu_control)

        # Verificar resultados

        assert dut.flags[3].value == model_overflow, \
            f"Error en overflow flag para op1={op1} op2={op2} alu_control={alu_control} Esperado={model_overflow}"

        assert dut.flags[2].value == model_carry, \
            f"Error en carry flag para op1={op1} op2={op2} alu_control={alu_control} Esperado={model_carry}"

        assert dut.flags[1].value == model_zero, \
            f"Error en zero flag para op1={op1} op2={op2} alu_control={alu_control} Esperado={model_zero}"

        assert dut.flags[0].value == model_negative, \
            f"Error en negative flag para op1={op1} op2={op2} alu_control={alu_control} Esperado={model_negative}"

        #assert dut_flags == ((model_negative << 3) | (model_zero << 2) | (model_carry << 1) | model_overflow), \
        #    f"Error en flags. Esperado :{bin((model_negative << 3) | (model_zero << 2) | (model_carry << 1) | model_overflow)}, obtenido {bin(dut_flags)}."

        assert dut_result == model_result, \
            f"Error en result para op1: {op1}, op2: {op2} control: {alu_control}. Esperado {model_result}, obtenido {dut_result}."
        

        dut._log.info(f"Test OK para alu_control={alu_control}, op1={op1}, op2={op2}, Resultado= {dut_result}.")
