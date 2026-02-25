import math

# ─────────────────────────────────────────────────────────────────────────────
#  SIMBOLOS DE PIZARRON (Unicode)
# ─────────────────────────────────────────────────────────────────────────────
#  ²  ³  ¹  √  ±  Δ  →  ·  ─  =

def fmt_eq(a, b, c):
    """Devuelve la ecuacion normalizada con notacion de pizarron."""
    def coef(v, var):
        if v == 1:   return f"{var}"
        if v == -1:  return f"-{var}"
        return f"{v:g}{var}"

    partes = []
    if a != 0:
        partes.append(coef(a, "x²"))
    if b != 0:
        term = coef(b, "x")
        if partes and b > 0:
            term = "+ " + term
        elif partes and b < 0:
            term = "- " + coef(-b, "x")
        partes.append(term)
    if c != 0:
        if partes and c > 0:
            partes.append(f"+ {c:g}")
        elif partes and c < 0:
            partes.append(f"- {-c:g}")
        else:
            partes.append(f"{c:g}")
    return " ".join(partes) + " = 0" if partes else "0 = 0"


# ─────────────────────────────────────────────────────────────────────────────
#  UTILIDADES
# ─────────────────────────────────────────────────────────────────────────────

def pausa(msg="  [ Presiona ENTER para continuar... ]"):
    input(f"\n{msg}")
    print()


def obtener_valor(mensaje):
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("  Entrada invalida. Usa numeros (punto para decimales).")


# ─────────────────────────────────────────────────────────────────────────────
#  INTRODUCCION: FORMULA GENERAL
# ─────────────────────────────────────────────────────────────────────────────

def mostrar_formula_general():

    # --- Bloque 1: La formula ---
    print("\n" + "=" * 65)
    print("  LA FORMULA GENERAL (O CUADRATICA)")
    print("=" * 65)
    print("""
  Para cualquier ecuacion de la forma:

        ax² + bx + c = 0

  existe una formula que calcula directamente las soluciones:

                  -b  ±  √(b² - 4ac)
        x  =  ──────────────────────────
                          2a
""")
    pausa()

    # --- Bloque 2: Por que funciona ---
    print("─" * 65)
    print("  POR QUE FUNCIONA?")
    print("─" * 65)
    print("""
  Se deriva del metodo "completar el cuadrado":
  partimos de  ax² + bx + c = 0  y despejamos x con algebra.
  El resultado siempre es la misma formula, sin importar a, b, c.

  En lugar de repetir ese proceso, la formula ya lo resolvio
  de forma general. Solo sustituimos los valores.
""")
    pausa()

    # --- Bloque 3: a, b, c ---
    print("─" * 65)
    print("  QUE SIGNIFICA CADA PARTE?")
    print("─" * 65)
    print("""
   a  →  Coeficiente de x²  (define el ancho de la parabola)
   b  →  Coeficiente de x   (controla la inclinacion lateral)
   c  →  Termino independiente (donde corta el eje Y)
""")
    pausa("  [ ENTER para ver el Discriminante... ]")

    # --- Bloque 4: Discriminante ---
    print("""
   Δ = b² - 4ac   →   DISCRIMINANTE

       Δ > 0  →  Dos soluciones reales distintas
       Δ = 0  →  Una solucion real  (raiz doble)
       Δ < 0  →  Sin soluciones reales
""")
    pausa("  [ ENTER para ver el signo ± ... ]")

    # --- Bloque 5: Signo +/- ---
    print("""
   ±   →  Nos da DOS caminos: x₁ y x₂
           La parabola puede cruzar el eje X en dos puntos
           simetricos respecto al vertice.

   2a  →  Escala la solucion segun la amplitud de la parabola.
""")
    print("=" * 65)
    pausa("  [ ENTER para comenzar a resolver... ]")


# ─────────────────────────────────────────────────────────────────────────────
#  RESOLVER
# ─────────────────────────────────────────────────────────────────────────────

def resolver_ecuacion():
    mostrar_formula_general()

    print("\n" + "=" * 65)
    print("  TUTOR: ECUACIONES DE 2° GRADO")
    print("=" * 65)
    print("""
  Identifica la estructura de tu ecuacion:

    1)  ax² + bx + c = 0   (Estructura base)
    2)  ax² + bx = c       (Termino independiente separado)
    3)  ax² = bx + c       (Terminos separados)
    4)  ax² = c            (Sin termino lineal)
    5)  a/x² + b/x + c = 0 (Ecuacion racional)
""")

    opcion = input("  Elige la estructura (1-5): ")
    a_final, b_final, c_final = 0.0, 0.0, 0.0
    print("\n" + "─" * 65)

    # ────────────────── Forma 1 ──────────────────
    if opcion == "1":
        print("  FORMA 1  —  Estructura base:  ax² + bx + c = 0\n")
        a_final = obtener_valor("  a (coef. de x²) = ")
        b_final = obtener_valor("  b (coef. de x)  = ")
        c_final = obtener_valor("  c (independ.)   = ")

        pausa()
        print("  Tu ecuacion ya tiene la forma estandar:")
        print(f"      {fmt_eq(a_final, b_final, c_final)}")

    # ────────────────── Forma 2 ──────────────────
    elif opcion == "2":
        print("  FORMA 2  —  ax² + bx = c\n")
        a_final = obtener_valor("  a (coef. de x²) = ")
        b_final = obtener_valor("  b (coef. de x)  = ")
        c_der   = obtener_valor("  c (lado derecho) = ")

        pausa()
        print("  PASO 1 · Inverso aditivo")
        print("  ─────────────────────────────────────────────────────")
        print("  Para usar la formula, un lado debe ser 0.")
        print(f"  Restamos {c_der:g} en ambos lados:\n")
        print(f"      {a_final:g}x² + {b_final:g}x - {c_der:g}  =  {c_der:g} - {c_der:g}")

        c_final = -c_der
        pausa()
        print(f"  Ecuacion normalizada:  {fmt_eq(a_final, b_final, c_final)}")

    # ────────────────── Forma 3 ──────────────────
    elif opcion == "3":
        print("  FORMA 3  —  ax² = bx + c\n")
        a_final = obtener_valor("  a (coef. de x², izquierda) = ")
        b_der   = obtener_valor("  b (coef. de x, derecha)    = ")
        c_der   = obtener_valor("  c (independ., derecha)     = ")

        pausa()
        print("  PASO 1 · Neutralizar el lado derecho")
        print("  ─────────────────────────────────────────────────────")
        print(f"  Restamos {b_der:g}x y {c_der:g} en ambos lados:")
        print(f"\n      {a_final:g}x² - {b_der:g}x - {c_der:g}  =  0")

        b_final = -b_der
        c_final = -c_der
        pausa()
        print(f"  Ecuacion normalizada:  {fmt_eq(a_final, b_final, c_final)}")

    # ────────────────── Forma 4 ──────────────────
    elif opcion == "4":
        print("  FORMA 4  —  ax² = c   (sin termino lineal)\n")
        a_final = obtener_valor("  a (coef. de x²) = ")
        c_der   = obtener_valor("  c (lado derecho) = ")

        pausa()
        print("  PASO 1 · Rellenar huecos")
        print("  ─────────────────────────────────────────────────────")
        print("  Si no aparece el termino 'x', su coeficiente es 0.")
        print(f"  Restamos {c_der:g} en ambos lados para igualar a 0.")

        b_final = 0.0
        c_final = -c_der
        pausa()
        print(f"  Ecuacion normalizada:  {fmt_eq(a_final, b_final, c_final)}")

    # ────────────────── Forma 5 ──────────────────
    elif opcion == "5":
        print("  FORMA 5  —  a/x² + b/x + c = 0\n")
        a_num = obtener_valor("  a (numerador de 1/x²) = ")
        b_num = obtener_valor("  b (numerador de 1/x)  = ")
        c_ind = obtener_valor("  c (termino suelto)    = ")

        pausa()
        print("  PASO 1 · Eliminar denominadores (MCM = x²)")
        print("  ─────────────────────────────────────────────────────")
        print("  Multiplicamos toda la ecuacion por x²:\n")
        print(f"      x² · ({a_num:g}/x²)  →  queda:  {a_num:g}")
        print(f"      x² · ({b_num:g}/x)   →  queda:  {b_num:g}x")
        print(f"      x² · {c_ind:g}       →  queda:  {c_ind:g}x²")

        a_final = c_ind
        b_final = b_num
        c_final = a_num
        pausa()
        print("  Reordenando por exponente:")
        print(f"  {fmt_eq(a_final, b_final, c_final)}")

    else:
        print("  Opcion no reconocida. Vuelve a intentarlo.")
        return

    print("\n" + "─" * 65)

    # ────────────────── Validacion de grado ──────────────────
    if a_final == 0:
        pausa()
        print("  AVISO: el coeficiente de x² es 0.")
        print("  Sin x² la ecuacion desciende a 1° grado.")
        if b_final != 0:
            x_lin = -c_final / b_final
            pausa("  [ ENTER para ver la solucion lineal... ]")
            print(f"  x = {x_lin:.4f}")
        else:
            print("  Inconsistencia: no hay solucion posible.")
        return

    # ────────────────── Paso 2: Discriminante ──────────────────
    pausa("  [ ENTER para calcular el Discriminante Δ... ]")
    print("  PASO 2 · Discriminante")
    print("  ─────────────────────────────────────────────────────")
    print("  Calculamos Δ = b² - 4ac antes de continuar,")
    print("  porque vive dentro de la raiz cuadrada.")
    print("  Si Δ < 0 no hay soluciones reales.\n")
    print(f"      Δ  =  ({b_final:g})²  -  4 · ({a_final:g}) · ({c_final:g})")

    delta = (b_final ** 2) - (4 * a_final * c_final)
    pausa()
    print(f"      Δ  =  {delta:g}")

    if delta < 0:
        pausa()
        print(f"  Δ = {delta:g}  (negativo)")
        print("  La parabola no toca el eje X → sin soluciones reales.")
        return

    if delta == 0:
        pausa()
        print("  Δ = 0  →  raiz doble (una sola solucion).")
    else:
        pausa()
        print(f"  Δ = {delta:g}  (positivo) → hay dos soluciones reales.")

    # ────────────────── Paso 3: Formula general ──────────────────
    pausa("  [ ENTER para aplicar la Formula General... ]")
    print("  PASO 3 · Formula General")
    print("  ─────────────────────────────────────────────────────")
    print("  Sustituimos a, b, c en la formula:")
    print()
    print("                -b  ±  √Δ")
    print("      x  =  ─────────────────")
    print("                   2a")
    print()

    raiz = math.sqrt(delta)
    den  = 2 * a_final

    # Explicar el denominador
    pausa("  [ ENTER para calcular el denominador... ]")
    print(f"  Denominador  →  2a  =  2 × {a_final:g}  =  {den:g}")

    # Explicar la raiz
    pausa("  [ ENTER para calcular la raiz cuadrada... ]")
    print(f"  Raiz cuadrada  →  √Δ  =  √{delta:g}  =  {raiz:.4f}")

    # Mostrar la fraccion con numeros reales
    pausa("  [ ENTER para ver la fraccion con valores reales... ]")
    print(f"\n             -({b_final:g})  ±  {raiz:.4f}")
    print(f"      x  =  ─────────────────────────")
    print(f"                    {den:g}\n")

    x1 = (-b_final + raiz) / den
    x2 = (-b_final - raiz) / den

    neg_b = -b_final

    # Camino 1: suma
    pausa("  [ ENTER para resolver el Camino 1  (+)... ]")
    print("  Camino 1  →  usamos  +")
    print(f"      Numerador  =  {neg_b:g}  +  {raiz:.4f}  =  {neg_b + raiz:.4f}")
    print(f"      x₁  =  {neg_b + raiz:.4f}  /  {den:g}  =  {x1:.4f}")

    # Camino 2: resta
    pausa("  [ ENTER para resolver el Camino 2  (-)... ]")
    print("  Camino 2  →  usamos  -")
    print(f"      Numerador  =  {neg_b:g}  -  {raiz:.4f}  =  {neg_b - raiz:.4f}")
    print(f"      x₂  =  {neg_b - raiz:.4f}  /  {den:g}  =  {x2:.4f}")

    pausa("  [ ENTER para ver el resumen de soluciones... ]")
    print("  SOLUCIONES")
    print("  ─────────────────────────────────────────────────────")
    print(f"      x₁  =  {x1:.4f}")
    print(f"      x₂  =  {x2:.4f}")
    print()


# ─────────────────────────────────────────────────────────────────────────────
#  PUNTO DE ENTRADA
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    while True:
        resolver_ecuacion()
        continuar = input("  Resolver otra ecuacion? (s/n): ").strip().lower()
        if continuar != "s":
            print("  Sigue practicando. La logica hace al maestro.")
            break