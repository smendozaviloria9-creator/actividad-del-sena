import datetime
import json
import os
import sys

# Rutas absolutas automáticas (evita fallos de carpeta de ejecución)
DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_USUARIOS = os.path.join(DIRECTORIO_ACTUAL, "usuarios.json")
ARCHIVO_EQUIPOS = os.path.join(DIRECTORIO_ACTUAL, "equipos.json")
ARCHIVO_PRESTAMOS = os.path.join(DIRECTORIO_ACTUAL, "prestamos.json")

FORMATO_FECHA = "%Y-%m-%d %H:%M:%S"

# Datos iniciales obligatorios si el archivo no existe o está en blanco
DATOS_INICIALES_USUARIOS = {
    "1001": {"nombre": "Ana Gomez", "contacto": "ana@correo.com", "sancionado": False},
    "1002": {"nombre": "Carlos Perez", "contacto": "3001234567", "sancionado": False}
}

DATOS_INICIALES_EQUIPOS = {
    "EQ-01": {"marca": "Lenovo", "modelo": "ThinkPad E14", "estado": "DISPONIBLE"},
    "EQ-02": {"marca": "HP", "modelo": "ProBook 440", "estado": "DISPONIBLE"}
}

def guardar_json(ruta, datos):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def cargar_o_reparar_json(ruta, datos_por_defecto):
    """Garantiza que el archivo exista y no esté en blanco."""
    if not os.path.exists(ruta) or os.path.getsize(ruta) == 0:
        guardar_json(ruta, datos_por_defecto)
        return datos_por_defecto
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # Si el JSON estaba mal escrito, lo repara con los datos base
        guardar_json(ruta, datos_por_defecto)
        return datos_por_defecto

# Inicialización segura
def inicializar_archivos():
    usuarios = cargar_o_reparar_json(ARCHIVO_USUARIOS, DATOS_INICIALES_USUARIOS)
    equipos = cargar_o_reparar_json(ARCHIVO_EQUIPOS, DATOS_INICIALES_EQUIPOS)
    prestamos = cargar_o_reparar_json(ARCHIVO_PRESTAMOS, [])
    return usuarios, equipos, prestamos

def registrar_prestamo():
    print("\n--- REGISTRAR PRESTAMO ---")
    usuarios, equipos, prestamos = inicializar_archivos()

    print("\nUsuarios registrados: " + ", ".join([f"{k} ({v['nombre']})" for k, v in usuarios.items()]))
    id_usuario = input("Documento de identidad: ").strip()

    if id_usuario not in usuarios:
        print(">> ERROR: Usuario no registrado.")
        return

    if usuarios[id_usuario].get("sancionado", False):
        print(">> RECHAZADO: Usuario con sancion activa.")
        return

    tiene_prestamo = any(p["id_usuario"] == id_usuario and p["estado"] == "ACTIVO" for p in prestamos)
    if tiene_prestamo:
        print(">> RECHAZADO: El usuario ya tiene un equipo prestado.")
        return

    print("\nEquipos en inventario: " + ", ".join([f"{k} [{v['estado']}]" for k, v in equipos.items()]))
    codigo_equipo = input("Codigo del equipo (ej: EQ-01): ").strip().upper()

    if codigo_equipo not in equipos:
        print(">> ERROR: El equipo no existe.")
        return

    if equipos[codigo_equipo]["estado"] != "DISPONIBLE":
        print(f">> RECHAZADO: El equipo no esta disponible (Estado: {equipos[codigo_equipo]['estado']}).")
        return

    try:
        horas = float(input("Horas de prestamo (ej: 2 o 4): "))
        if horas <= 0:
            print(">> ERROR: Las horas deben ser mayores a 0.")
            return
    except ValueError:
        print(">> ERROR: Ingrese un numero valido.")
        return

    ahora = datetime.datetime.now()
    fecha_limite = ahora + datetime.timedelta(hours=horas)

    nuevo_prestamo = {
        "id": len(prestamos) + 1,
        "id_usuario": id_usuario,
        "codigo_equipo": codigo_equipo,
        "fecha_salida": ahora.strftime(FORMATO_FECHA),
        "fecha_limite": fecha_limite.strftime(FORMATO_FECHA),
        "fecha_devolucion": None,
        "estado": "ACTIVO"
    }

    prestamos.append(nuevo_prestamo)
    equipos[codigo_equipo]["estado"] = "PRESTADO"

    guardar_json(ARCHIVO_PRESTAMOS, prestamos)
    guardar_json(ARCHIVO_EQUIPOS, equipos)

    print(f"\n>> PRESTAMO EXITOSO: Equipo {codigo_equipo} prestado a {usuarios[id_usuario]['nombre']}.")
    print(f">> Fecha limite: {fecha_limite.strftime(FORMATO_FECHA)}")

def registrar_devolucion():
    print("\n--- REGISTRAR DEVOLUCION ---")
    usuarios, equipos, prestamos = inicializar_archivos()

    activos = [p for p in prestamos if p["estado"] == "ACTIVO"]
    if not activos:
        print(">> No hay ningun prestamo activo por devolver.")
        return

    print("Equipos actualmente en prestamo: " + ", ".join([p["codigo_equipo"] for p in activos]))
    codigo_equipo = input("Codigo del equipo a devolver: ").strip().upper()

    prestamo_encontrado = None
    for p in prestamos:
        if p["codigo_equipo"] == codigo_equipo and p["estado"] == "ACTIVO":
            prestamo_encontrado = p
            break

    if not prestamo_encontrado:
        print(">> ERROR: No hay ningun prestamo activo con ese equipo.")
        return

    ahora = datetime.datetime.now()
    fecha_limite = datetime.datetime.strptime(prestamo_encontrado["fecha_limite"], FORMATO_FECHA)

    prestamo_encontrado["fecha_devolucion"] = ahora.strftime(FORMATO_FECHA)
    prestamo_encontrado["estado"] = "DEVUELTO"

    if ahora > fecha_limite:
        minutos = int((ahora - fecha_limite).total_seconds() // 60)
        print(f"\n>> ALERTA: Devolucion con mora ({minutos} minutos de retraso).")
    else:
        print("\n>> Devolucion realizada dentro del plazo.")

    tiene_cargador = input("¿Entrego cargador? (s/n): ").strip().lower() == "s"
    buen_estado = input("¿Portatil en buen estado? (s/n): ").strip().lower() == "s"

    if tiene_cargador and buen_estado:
        equipos[codigo_equipo]["estado"] = "DISPONIBLE"
        print(f">> Equipo {codigo_equipo} liberado y listo para prestamo.")
    else:
        equipos[codigo_equipo]["estado"] = "EN_REVISION"
        print(f">> Equipo {codigo_equipo} enviado a Mantenimiento/Revision.")

    guardar_json(ARCHIVO_PRESTAMOS, prestamos)
    guardar_json(ARCHIVO_EQUIPOS, equipos)

def consultar_pendientes():
    print("\n--- ESTADO DE PRESTAMOS ---")
    _, _, prestamos = inicializar_archivos()
    activos = [p for p in prestamos if p["estado"] == "ACTIVO"]

    if not activos:
        print("No hay prestamos activos en este momento.")
        return

    ahora = datetime.datetime.now()
    print(f"\n{'ID':<4} | {'USUARIO':<10} | {'EQUIPO':<8} | {'LIMITE':<20} | {'ESTADO'}")
    print("-" * 60)
    for p in activos:
        limite = datetime.datetime.strptime(p["fecha_limite"], FORMATO_FECHA)
        estado = "VENCIDO (MORA)" if ahora > limite else "ACTIVO (AL DIA)"
        print(f"{p['id']:<4} | {p['id_usuario']:<10} | {p['codigo_equipo']:<8} | {p['fecha_limite']:<20} | {estado}")

def main():
    inicializar_archivos()
    while True:
        print("\n" + "=" * 42)
        print("  GESTION DE PORTATILES (SENA GFPI-F-135) ")
        print("=" * 42)
        print("1. Registrar Prestamo")
        print("2. Registrar Devolucion")
        print("3. Consultar Prestamos Activos")
        print("4. Salir")
        
        opcion = input("Seleccione una opcion (1-4): ").strip()
        if opcion == "1":
            registrar_prestamo()
        elif opcion == "2":
            registrar_devolucion()
        elif opcion == "3":
            consultar_pendientes()
        elif opcion == "4":
            print("\nSaliendo del programa.")
            break
        else:
            print(">> Opcion invalida. Ingrese 1, 2, 3 o 4.")

if __name__ == "__main__":
    main()