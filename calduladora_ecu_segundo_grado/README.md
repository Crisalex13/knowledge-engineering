# Calculadora de Ecuaciones de 2° Grado — Documentación Técnica

> `calculadora_ecu_segundo_grado_terminal.py`

---

## Descripción general

Tutor interactivo de terminal que enseña a un estudiante a resolver
cualquier ecuación cuadrática usando la **Fórmula General**.

El programa no entrega la respuesta de golpe: divide el proceso en
pasos desbloqueados por ENTER, explicando *por qué* se hace cada
operación antes de mostrar el resultado numérico.

---

## Requisitos

- Python 3.6 o superior
- Sin dependencias externas (`import math` de la biblioteca estándar)

```bash
python3 calculadora_ecu_segundo_grado_terminal.py
```

---

## Arquitectura — Funciones principales

```
calculadora_ecu_segundo_grado_terminal.py
│
├── fmt_eq(a, b, c)            → Formatea la ecuación con notación Unicode (x², →, ±)
├── pausa(msg)                 → Detiene la ejecución hasta que el usuario presiona ENTER
├── obtener_valor(mensaje)     → Solicita un float con validación de entrada
├── mostrar_formula_general()  → Explica la Fórmula General en 5 bloques desbloqueables
└── resolver_ecuacion()        → Flujo principal: normalización → discriminante → solución
```

---

## Flujo algorítmico completo

```
INICIO
  │
  ▼
mostrar_formula_general()
  │  Bloque 1: muestra  x = (-b ± √(b²-4ac)) / 2a
  │  Bloque 2: explica el origen (completar el cuadrado)
  │  Bloque 3: define a, b, c
  │  Bloque 4: define el Discriminante Δ y sus tres casos
  │  Bloque 5: explica el signo ± y el denominador 2a
  │  (cada bloque se desbloquea con ENTER)
  │
  ▼
resolver_ecuacion()
  │
  ├─► El usuario elige la estructura de la ecuación (1–5)
  │
  ├─► NORMALIZACIÓN  (ver detalle abajo)
  │     Convierte cualquier forma a:  ax² + bx + c = 0
  │     Produce:  a_final, b_final, c_final
  │
  ├─► VALIDACIÓN DE GRADO
  │     Si a_final == 0:
  │       La ecuación baja a 1° grado
  │       Si b_final ≠ 0  →  x = -c / b
  │       Si b_final == 0 →  inconsistencia (sin solución)
  │       FIN
  │
  ├─► PASO 2 — DISCRIMINANTE
  │     Δ = b² - 4ac
  │     Si Δ < 0  →  sin soluciones reales  →  FIN
  │     Si Δ = 0  →  raíz doble  (continúa)
  │     Si Δ > 0  →  dos soluciones reales  (continúa)
  │
  └─► PASO 3 — FÓRMULA GENERAL
        den  = 2 × a
        raiz = √Δ
        x₁   = (-b + raiz) / den      ← camino  +
        x₂   = (-b - raiz) / den      ← camino  -
        Muestra cada operación desglosada antes del resultado final

FIN  →  ¿Resolver otra ecuación? (s/n)
```

---

## Las 5 formas de entrada y su normalización

Toda ecuación cuadrática se puede escribir de distintas maneras.
El programa acepta 5 estructuras y las transforma a la **forma estándar**
`ax² + bx + c = 0` antes de aplicar la Fórmula General.

### Forma 1 — Estructura base

```
Entrada:   ax² + bx + c = 0
Acción:    ninguna (ya está normalizada)

a_final = a
b_final = b
c_final = c
```

### Forma 2 — Término independiente separado

```
Entrada:   ax² + bx = c
Acción:    restar c en ambos lados (inverso aditivo)

a_final = a
b_final = b
c_final = -c          ← c pasa al otro lado con signo cambiado
```

### Forma 3 — Términos separados

```
Entrada:   ax² = bx + c
Acción:    restar (bx + c) en ambos lados

a_final =  a
b_final = -b           ← b pasa al otro lado
c_final = -c           ← c pasa al otro lado
```

### Forma 4 — Sin término lineal

```
Entrada:   ax² = c
Acción:    restar c en ambos lados; b no existe → b = 0

a_final =  a
b_final =  0.0         ← implícito (el término "bx" no aparece)
c_final = -c
```

### Forma 5 — Ecuación racional (con fracciones)

```
Entrada:   a/x² + b/x + c = 0
Acción:    multiplicar toda la ecuación por x²  (MCM = x²)

   x² · (a/x²)  →  a              (x² / x² = 1)
   x² · (b/x)   →  bx             (x² / x  = x)
   x² · c       →  cx²

Reordenando por grado descendente:

a_final = c            ← lo que era el término independiente
b_final = b            ← el coef. de 1/x se mantiene
c_final = a            ← el numerador de 1/x² pasa a ser el indep.
```

---

## Algoritmo del Discriminante

```python
delta = b_final**2 - (4 * a_final * c_final)

if delta < 0:
    # La parábola no toca el eje X
    # No existe raíz cuadrada real de un número negativo

elif delta == 0:
    # La parábola toca el eje X en exactamente un punto
    # x₁ = x₂  (raíz doble)

else:   # delta > 0
    # La parábola corta el eje X en dos puntos distintos
    # x₁ ≠ x₂
```

El discriminante se calcula **antes** de `math.sqrt()` precisamente
para evitar un `ValueError` de Python al pasar un número negativo a
la raíz cuadrada.

---

## Algoritmo de la Fórmula General

```python
raiz = math.sqrt(delta)     # √Δ
den  = 2 * a_final          # denominador: 2a

x1 = (-b_final + raiz) / den   # camino  +
x2 = (-b_final - raiz) / den   # camino  -
```

El programa muestra cada sub-cálculo en pasos separados:

```
Denominador  →  2a  =  2 × 6  =  12
Raiz cuadrada  →  √Δ  =  √48  =  6.9282

             -(0)  ±  6.9282
   x  =  ─────────────────────────
                   12

Camino 1  →  usamos  +
    Numerador  =  0  +  6.9282  =  6.9282
    x₁  =  6.9282  /  12  =  0.5774

Camino 2  →  usamos  -
    Numerador  =  0  -  6.9282  =  -6.9282
    x₂  =  -6.9282  /  12  =  -0.5774
```

---

## Función auxiliar: `fmt_eq(a, b, c)`

Convierte los coeficientes numéricos en una cadena legible con
notación de pizarrón (Unicode):

```python
fmt_eq(1, -5, 6)    →   "x² - 5x + 6 = 0"
fmt_eq(2, 0, -8)    →   "2x² - 8 = 0"
fmt_eq(-1, 1, 0)    →   "-x² + x = 0"
```

Reglas internas:
- Si `a == 1` → omite el coeficiente ("x²" en lugar de "1x²")
- Si `a == -1` → escribe "-x²"
- Términos con valor 0 no se imprimen
- El operador `+` o `-` entre términos se agrega automáticamente
  según el signo del coeficiente

---

## Tabla de casos matemáticos cubiertos

| Caso | Condición | Resultado |
|---|---|---|
| Dos soluciones reales | Δ > 0 | x₁ ≠ x₂ |
| Raíz doble | Δ = 0 | x₁ = x₂ |
| Sin solución real | Δ < 0 | La parábola no corta el eje X |
| Ecuación lineal | a = 0, b ≠ 0 | x = −c / b |
| Inconsistencia | a = 0, b = 0 | Sin solución |

---

## Ejemplo de sesión completa

```
Ecuación de entrada:   2x² = 3x + 2

Forma elegida:  3  (ax² = bx + c)
  a ingresado:  2
  b ingresado:  3   →  b_final = -3
  c ingresado:  2   →  c_final = -2

Ecuación normalizada:  2x² - 3x - 2 = 0

Δ = (-3)² - 4 · 2 · (-2) = 9 + 16 = 25

Denominador  2a  =  2 × 2  =  4
Raiz cuadrada  √25  =  5.0000

Camino 1 (+):   (-(-3) + 5) / 4  =  8 / 4  =  2.0000
Camino 2 (-):   (-(-3) - 5) / 4  = -2 / 4  = -0.5000

SOLUCIONES:
  x₁ = 2.0000
  x₂ = -0.5000
```
## Ejemplo practico del sistema

Explicacion de como inicia el sistema:
![Explicacion sistema 1](../imgs/imagenes%202%20grado/2%20grado%20parte%201.png)


![Explicacion sistema 2](../imgs/imagenes%202%20grado/2%20grado%20parte%202.png)

![Explicacion sistema 3](../imgs/imagenes%202%20grado/2%20grado%20parte%203.png)

![Explicacion sistema 1](../imgs/imagenes%202%20grado/2%20grado%20parte%204.png)

![Explicacion sistema 1](../imgs/imagenes%202%20grado/2%20grado%20parte%205.png)

![Explicacion sistema 1](../imgs/imagenes%202%20grado/2-grado%20parte%206.png)

Aqui vamos a realizar un nuestro 1 ejemplo:

```
x² - 5x + 6 = 0
```


![Ejemplo 1](../imgs/imagenes%202%20grado/aplicacion%201.png)

![Ejemplo 1](../imgs/imagenes%202%20grado/aplicacion%201.1.png)

![Ejemplo 1](../imgs/imagenes%202%20grado/aplicacion%201.2.png)

![Ejemplo 1](../imgs/imagenes%202%20grado/aplicacion%201.3.png)

Como nosotros lo veriamos:

![Ejemplo 1](../imgs/imagenes%202%20grado/ejemplo%202%20grado%20parte%201.png)

![Ejemplo 1](../imgs/imagenes%202%20grado/ejemplo%202%20grado%20parte%201.1.png)

Aqui vamos a realizar un nuestro 2 ejemplo:

```
2x² + 3x = 5
```

![Ejemplo 2](../imgs/imagenes%202%20grado/aplicacion%202.png)

![Ejemplo 2](../imgs/imagenes%202%20grado/aplicacion%202.1.png)

![Ejemplo 2](../imgs/imagenes%202%20grado/aplicacion%202.2.png)

![Ejemplo 2](../imgs/imagenes%202%20grado/aplicacion%202.3.png)

Como nosotros lo veriamos:

![Ejemplo 2](../imgs/imagenes%202%20grado/ejemplo%202%20grado%202.png)

=======
![Ejemplo 1](../imgs/imagenes%202%20grado/aplicacion%201.png)
![Ejemplo 1](../imgs/imagenes%202%20grado/aplicacion%201.1.png)
![Ejemplo 1](../imgs/imagenes%202%20grado/aplicacion%201.2.png)
![Ejemplo 1](../imgs/imagenes%202%20grado/aplicacion%201.3.png)

Como nosotros lo veriamos:
![Ejemplo 1](../imgs/imagenes%202%20grado/ejemplo%202%20grado%20parte%201.png)
![Ejemplo 1](../imgs/imagenes%202%20grado/ejemplo%202%20grado%20parte%201.1.png)



Aqui vamos a realizar un nuestro 2 ejemplo:
```
2x² + 3x = 5
```
![Ejemplo 2](../imgs/imagenes%202%20grado/aplicacion%202.png)
![Ejemplo 2](../imgs/imagenes%202%20grado/aplicacion%202.1.png)
![Ejemplo 2](../imgs/imagenes%202%20grado/aplicacion%202.2.png)
![Ejemplo 2](../imgs/imagenes%202%20grado/aplicacion%202.3.png)

Como nosotros lo veriamos:
![Ejemplo 2](../imgs/imagenes%202%20grado/ejemplo%202%20grado%202.png)

![Ejemplo 2](../imgs/imagenes%202%20grado/ejemplo%202%20grado%202.1.png)


