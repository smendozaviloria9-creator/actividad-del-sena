# actividad-del-sena
# 🗂️ Portafolio de Evidencias - Programación de Software (SENA)

![Estado](https://img.shields.io/badge/Estado-Completado-success)
![Lenguaje](https://img.shields.io/badge/Python-3.x-blue)
![Ficha](https://img.shields.io/badge/Ficha-233104-orange)

Repositorio con el código fuente, estructuras de persistencia y documentación técnica de las actividades prácticas desarrolladas en Python durante la etapa de formación.

---

## 📋 Información General

* **Programa:** Técnico en Programación de Software (`233104`)
* **Centro de Formación:** SENA - Regional Atlántico (Barranquilla)
* **Aprendiz:** Sebastián David Mendoza Viloria

---

## 📊 Índice de Actividades

| # | Actividad / Proyecto | Archivos Principales | Persistencia / Salida |
| :-: | :--- | :--- | :--- |
| **01** | **Cálculo de Subtotal y Descuentos en Compras** | `prueba.py` | Salida por consola |
| **02** | **Gestión de Préstamo de Portátiles (GFPI-F-135)** | `main.py` | `usuarios.json`, `equipos.json`, `prestamos.json` |
| **03** | **Sistema de Liquidación de Nómina (TransCaribeCol)** | `main (1).py` | `nomina_transcaribecol.txt` |

---

## 🧩 Explicación Detallada de cada Actividad

### 1. Cálculo de Subtotal y Descuentos Condicionales (`prueba.py`)
* **¿Qué hace?** Simula la facturación básica de productos (botellas y frutas), calcula el subtotal de la compra y evalúa mediante una estructura condicional si el monto alcanza el tope mínimo (`$10.000`) para aplicar un descuento automático.
* **Conceptos aplicados:**
  * Declaración de variables y operadores aritméticos.
  * Estructuras condicionales (`if / else`) con banderas booleanas (`aplico_descuento`).
  * Formateo de cadenas con *f-strings* y operador ternario en salida por consola.

---

### 2. Sistema de Gestión de Préstamo de Portátiles (`main.py`)
* **¿Qué hace?** Aplicación de consola alineada con el control del formato **SENA GFPI-F-135** para administrar el inventario, entrega y devolución de equipos portátiles a aprendices/usuarios.
* **Funcionalidades principales:**
  * **Validaciones de seguridad:** Verifica que el usuario exista, no tenga sanciones activas y no posea otro préstamo vigente; además valida que el equipo esté `DISPONIBLE`.
  * **Control de tiempos y mora:** Calcula automáticamente la fecha límite de entrega según las horas solicitadas (`datetime`) y detecta retrasos en minutos al momento de la devolución.
  * **Inspección de estado:** Al devolver un equipo, verifica la entrega de cargador y estado físico; si falta algo, cambia el estado del portátil a `EN_REVISION`.
  * **Autoreparación de datos:** Incluye una función (`cargar_o_reparar_json`) que crea o restaura los archivos JSON base si están vacíos o corruptos.
* **Archivos asociados:** `usuarios.json`, `equipos.json` y `prestamos.json`.

---

### 3. Sistema de Nómina - TransCaribeCol S.C.A. (`main (1).py`)
* **¿Qué hace?** Sistema contable por consola que liquida el pago mensual y genera volantes detallados para dos tipos de vinculación laboral:
  1. **Personal Administrativo:** Calcula salario base (`$20.000/h`), horas extras (`$25.000/h`) y deducciones de ley sobre el total devengado (Salud 4%, Pensión 4% y ARL 0.522%).
  2. **Personal Operativo (Prestación de Servicios / Oficiales):** Liquidación por cargo (*Conductor*, *Oficios Generales*, *Vigilancia*) a `$40.000/h`, calculando aportes sobre el **IBC del 40%** (Salud 12.5%, Pensión 16% y ARL variable según nivel de riesgo I, II o IV).
* **Funcionalidades principales:**
  * Almacenamiento temporal en memoria mediante una **matriz (lista de listas)**.
  * Impresión de volantes de pago formateados en consola y casos de prueba precargados.
  * Exportación y sincronización automática de toda la tabla de nómina en el archivo plano `nomina_transcaribecol.txt`.

---

## 🚀 Ejecución Local

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/smendozaviloria9-creator/](https://github.com/smendozaviloria9-creator/)[nombre-del-repo].git
   cd [nombre-del-repo]
