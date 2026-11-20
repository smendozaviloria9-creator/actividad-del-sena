import os

# Estructura de datos (Matriz / Lista de listas) para almacenar los registros en memoria
nomina_registros = []
ARCHIVO_TXT = "nomina_transcaribecol.txt"


def imprimir_volante_administrativo(nombre, cargo, ht, salario_bruto, he, tphe, salud, pension, arl, total_descuentos_ley, total_pagar):
    """Imprime el volante de pago con el formato exacto para personal Administrativo."""
    print("\n" + "*" * 66)
    print("*" * 23 + " VOLANTE DE PAGO " + "*" * 26)
    print("*" * 66)
    print(f"Nombre: {nombre}")
    print(f"Cargo: {cargo}")
    print(f"Horas Trabajadas(mes): {ht}")
    print(f"Salario Bruto: ${salario_bruto:,.0f}")
    print(f"Horas Extras: {he}")
    print(f"Total pago Horas Extras: ${tphe:,.0f}")
    print("\n" + "*" * 66)
    print("*" * 22 + " DESCUENTOS DE LEY " + "*" * 25)
    print("*" * 66)
    print(f"Salud(4%): ${salud:.0f}")
    print(f"Pensión(4%): ${pension:.0f}")
    print(f"ARL(0,522%): ${arl:.0f}")
    print(f"Total Descuentos: ${total_descuentos_ley:.0f}")
    print(f"\nTotal a pagar: ${total_pagar:,.0f}")
    print("\n" + "*" * 66)
    print("*" * 19 + " FIN DEL VOLANTE DE PAGO " + "*" * 22)
    print("*" * 66 + "\n")


def imprimir_volante_operativo(nombre, cargo, ht, salario_bruto, salud, pension, arl, porc_arl, total_descuentos, total_pagar):
    """Imprime el volante de pago adaptado para personal Operativo (Contrato de prestación de servicios)."""
    print("\n" + "*" * 66)
    print("*" * 23 + " VOLANTE DE PAGO " + "*" * 26)
    print("*" * 66)
    print(f"Nombre: {nombre}")
    print(f"Cargo: {cargo}")
    print(f"Horas Trabajadas(mes): {ht}")
    print(f"Salario Bruto: ${salario_bruto:,.0f}")
    print("\n" + "*" * 66)
    print("*" * 15 + " APORTES SEGURIDAD SOCIAL (IBC 40%) " + "*" * 15)
    print("*" * 66)
    print(f"Salud(12.5%): ${salud:.0f}")
    print(f"Pensión(16%): ${pension:.0f}")
    print(f"ARL({porc_arl}%): ${arl:.0f}")
    print(f"Total Descuentos: ${total_descuentos:.0f}")
    print(f"\nTotal a pagar: ${total_pagar:,.0f}")
    print("\n" + "*" * 66)
    print("*" * 19 + " FIN DEL VOLANTE DE PAGO " + "*" * 22)
    print("*" * 66 + "\n")


def registrar_administrativo():
    print("\n--- REGISTRO DE EMPLEADO ADMINISTRATIVO ---")
    nombre = input("Ingrese el nombre completo del empleado: ").strip()
    cargo = input("Ingrese el cargo administrativo (ej. Auxiliar Administrativo): ").strip()
    
    try:
        ht = int(input("Ingrese las horas trabajadas en el mes: "))
        he = int(input("Ingrese las horas extras trabajadas (0 si no aplica): "))
    except ValueError:
        print("Error: Las horas deben ser valores numéricos enteros.")
        return

    # Cálculos Administrativos
    valor_hora = 20000
    valor_hora_extra = 25000
    
    salario_bruto = ht * valor_hora
    tphe = he * valor_hora_extra
    base_prestaciones = salario_bruto + tphe
    
    salud = round(base_prestaciones * 0.04)
    pension = round(base_prestaciones * 0.04)
    arl = round(base_prestaciones * 0.00522)
    
    # En el volante de referencia, 'Total Descuentos' muestra la suma de Salud + Pensión ($104,000),
    # mientras que el 'Total a pagar' descuenta Salud, Pensión y ARL ($1,189,214).
    total_descuentos_ley = salud + pension
    total_pagar = base_prestaciones - (salud + pension + arl)

    # Guardar en la estructura de datos (Matriz)
    registro = [
        nombre, "ADMINISTRATIVO", cargo, ht, salario_bruto, 
        he, tphe, salud, pension, arl, total_pagar
    ]
    nomina_registros.append(registro)

    # Mostrar volante en pantalla
    imprimir_volante_administrativo(
        nombre, cargo, ht, salario_bruto, he, tphe, 
        salud, pension, arl, total_descuentos_ley, total_pagar
    )
    guardar_en_txt()


def registrar_operativo():
    print("\n--- REGISTRO DE EMPLEADO OPERATIVO (TRABAJADOR OFICIAL) ---")
    nombre = input("Ingrese el nombre completo del trabajador: ").strip()
    
    print("Seleccione el cargo operativo:")
    print("a. Conductor (160 horas mensuales - Riesgo II: 1.044%)")
    print("b. Oficios Generales (100 horas mensuales - Riesgo I: 0.522%)")
    print("c. Vigilancia (336 horas mensuales - Riesgo IV: 4.350%)")
    opcion_cargo = input("Opción (a/b/c): ").strip().lower()

    if opcion_cargo == 'a':
        cargo = "Conductor"
        ht = 160
        tasa_arl = 0.01044
        porc_arl_texto = "1,044"
    elif opcion_cargo == 'b':
        cargo = "Oficios Generales"
        ht = 100
        tasa_arl = 0.00522
        porc_arl_texto = "0,522"
    elif opcion_cargo == 'c':
        cargo = "Vigilancia"
        ht = 336
        tasa_arl = 0.04350
        porc_arl_texto = "4,350"
    else:
        print("Opción de cargo no válida.")
        return

    # Cálculos Operativos
    valor_hora = 40000
    salario_bruto = ht * valor_hora
    he = 0
    tphe = 0

    # Índice de Base de Cotización (IBC) = 40% del salario bruto
    ibc = salario_bruto * 0.40

    salud = round(ibc * 0.125)
    pension = round(ibc * 0.16)
    arl = round(ibc * tasa_arl)

    total_descuentos = salud + pension + arl
    total_pagar = salario_bruto - total_descuentos

    # Guardar en la estructura de datos (Matriz)
    registro = [
        nombre, "OPERATIVO", cargo, ht, salario_bruto, 
        he, tphe, salud, pension, arl, total_pagar
    ]
    nomina_registros.append(registro)

    # Mostrar volante en pantalla
    imprimir_volante_operativo(
        nombre, cargo, ht, salario_bruto, salud, pension, 
        arl, porc_arl_texto, total_descuentos, total_pagar
    )
    guardar_en_txt()


def mostrar_matriz_y_guardar():
    if not nomina_registros:
        print("\nNo hay empleados registrados en la nómina aún.")
        return

    encabezado = (
        f"{'Nombre':<28} {'Tipo':<15} {'Cargo':<22} {'HT':<5} "
        f"{'Salario':<10} {'HE':<4} {'TPHE':<8} {'Salud':<8} "
        f"{'Pension':<8} {'ARL':<8} {'Total a pagar':<14}"
    )
    print("\n" + "=" * 140)
    print("REGISTROS EN ESTRUCTURA DE DATOS (MATRIZ DE NÓMINA)")
    print("=" * 140)
    print(encabezado)
    print("-" * 140)

    for fila in nomina_registros:
        print(
            f"{fila[0]:<28} {fila[1]:<15} {fila[2]:<22} {fila[3]:<5} "
            f"{fila[4]:<10} {fila[5]:<4} {fila[6]:<8} {fila[7]:<8} "
            f"{fila[8]:<8} {fila[9]:<8} {fila[10]:<14}"
        )
    print("=" * 140)
    guardar_en_txt()
    print(f"\n[OK] Datos sincronizados correctamente en el archivo '{ARCHIVO_TXT}'.")


def guardar_en_txt():
    """Guarda toda la matriz en un archivo plano TXT con formato tabular."""
    with open(ARCHIVO_TXT, mode="w", encoding="utf-8") as archivo:
        encabezado = (
            f"{'Nombre':<28}\t{'Tipo':<15}\t{'Cargo':<22}\t{'HT':<5}\t"
            f"{'Salario':<10}\t{'HE':<4}\t{'TPHE':<8}\t{'Salud':<8}\t"
            f"{'Pension':<8}\t{'ARL':<8}\t{'Total a pagar'}\n"
        )
        archivo.write(encabezado)
        for fila in nomina_registros:
            linea = (
                f"{fila[0]:<28}\t{fila[1]:<15}\t{fila[2]:<22}\t{fila[3]:<5}\t"
                f"{fila[4]:<10}\t{fila[5]:<4}\t{fila[6]:<8}\t{fila[7]:<8}\t"
                f"{fila[8]:<8}\t{fila[9]:<8}\t{fila[10]}\n"
            )
            archivo.write(linea)


def cargar_datos_ejemplo():
    """Carga los dos casos de prueba de la guía para verificar los cálculos de inmediato."""
    # Caso 1: Ana María Jaimes González (Administrativo)
    nomina_registros.append([
        "Ana María Jaimes González", "ADMINISTRATIVO", "Auxiliar Administrativo",
        40, 800000, 20, 500000, 52000, 52000, 6786, 1189214
    ])
    # Caso 2: Blanca Luz Iglesias Serpa (Operativo - Oficios Generales)
    nomina_registros.append([
        "Blanca Luz Iglesias Serpa", "OPERATIVO", "Oficios Generales",
        100, 4000000, 0, 0, 200000, 256000, 8352, 3535648
    ])
    guardar_en_txt()
    print("\n[OK] Se han cargado los 2 registros de prueba de la guía y guardado en el archivo TXT.")


def menu_principal():
    while True:
        print("\n========================================================")
        print("   SISTEMA DE NÓMINA - TRANSCARIBECOL S.C.A.")
        print("========================================================")
        print("1. Registrar empleado Administrativo")
        print("2. Registrar empleado Operativo (Trabajador Oficial)")
        print("3. Ver tabla de nómina (Matriz) y exportar a TXT")
        print("4. Cargar datos de ejemplo de la guía (Ana María y Blanca Luz)")
        print("5. Salir")
        print("========================================================")
        
        opcion = input("Seleccione una opción (1-5): ").strip()
        
        if opcion == '1':
            registrar_administrativo()
        elif opcion == '2':
            registrar_operativo()
        elif opcion == '3':
            mostrar_matriz_y_guardar()
        elif opcion == '4':
            cargar_datos_ejemplo()
        elif opcion == '5':
            guardar_en_txt()
            print(f"\nArchivo '{ARCHIVO_TXT}' generado exitosamente. ¡Hasta luego!")
            break
        else:
            print("\nOpción no válida. Por favor, intente de nuevo.")


if __name__ == "__main__":
    menu_principal()