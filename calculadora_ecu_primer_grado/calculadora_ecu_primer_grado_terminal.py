def resolver():
    print("================================================")
    print("   SISTEMA DE RESOLUCIÓN PASO A PASO (v2.0)    ")
    print("================================================")
    
    # Mostrar primero las capacidades del software
    print("\nOPERACIONES SOPORTADAS:")
    print("Este algoritmo resuelve ecuaciones de primer grado donde")
    print("'M' es cualquier operador (+, -, *, /) y X es la incógnita.")
    print("Estructuras:")
    print("  1) A M (B * X) = C")
    print("  2) (A * X) M B = C")
    print("  3) (A / X) M B = C")
    print("  4) A M (B / X) = C")
    print("  5) (X / A) M B = C")
    print("------------------------------------------------\n")

    try:
        # 1. Recolección de datos
        a = float(input("Valor de A: "))
        op = input("Operador M (+, -, *, /): ")
        b = float(input("Valor de B: "))
        c = float(input("Valor de C: "))
        opcion = input("\nElige el número de estructura (1-5): ")
        
        print("\n--- INICIANDO RESOLUCIÓN PASO A PASO ---")
        x = None

        # Función auxiliar para explicar el despeje de la operación M
        def explicar_m(val_a, res_c, operador):
            if operador == '+':
                print(f"Paso 1: Restamos {val_a} a ambos lados.")
                return res_c - val_a
            if operador == '-':
                print(f"Paso 1: El término {val_a} es positivo, al moverlo queda: {val_a} - {res_c}")
                return val_a - res_c
            if operador == '*':
                print(f"Paso 1: Dividimos ambos lados por {val_a}.")
                return res_c / val_a
            if operador == '/':
                print(f"Paso 1: Despejamos el divisor. El nuevo valor es {val_a} / {res_c}")
                return val_a / res_c

        # Función auxiliar para despejes simples (cuando X no está atrapado por A)
        def explicar_simple(res_c, val_b, operador):
            if operador == '+': return res_c - val_b, f"Restamos {val_b}"
            if operador == '-': return res_c + val_b, f"Sumamos {val_b}"
            if operador == '*': return res_c / val_b, f"Dividimos por {val_b}"
            if operador == '/': return res_c * val_b, f"Multiplicamos por {val_b}"

        # Lógica de resolución con explicaciones
        if opcion == "1":
            print(f"Ecuación: {a} {op} ({b} * X) = {c}")
            bx = explicar_m(a, c, op)
            print(f"-> Resultado intermedio: ({b} * X) = {bx}")
            print(f"Paso 2: Dividimos por {b} para aislar X.")
            x = bx / b

        elif opcion == "2":
            print(f"Ecuación: ( {a} * X ) {op} {b} = {c}")
            ax, msg = explicar_simple(c, b, op)
            print(f"Paso 1: {msg} en ambos lados.")
            print(f"-> Resultado intermedio: ({a} * X) = {ax}")
            print(f"Paso 2: Dividimos por {a} para aislar X.")
            x = ax / a

        elif opcion == "3":
            print(f"Ecuación: ( {a} / X ) {op} {b} = {c}")
            a_x, msg = explicar_simple(c, b, op)
            print(f"Paso 1: {msg} en ambos lados.")
            print(f"-> Resultado intermedio: ({a} / X) = {a_x}")
            print(f"Paso 2: Intercambiamos X con el resultado: X = {a} / {a_x}")
            x = a / a_x

        elif opcion == "4":
            print(f"Ecuación: {a} {op} ({b} / X) = {c}")
            b_x = explicar_m(a, c, op)
            print(f"-> Resultado intermedio: ({b} / X) = {b_x}")
            print(f"Paso 2: Intercambiamos X con el resultado: X = {b} / {b_x}")
            x = b / b_x

        elif opcion == "5":
            print(f"Ecuación: ( X / {a} ) {op} {b} = {c}")
            x_a, msg = explicar_simple(c, b, op)
            print(f"Paso 1: {msg} en ambos lados.")
            print(f"-> Resultado intermedio: (X / {a}) = {x_a}")
            print(f"Paso 2: Multiplicamos por {a} para aislar X.")
            x = x_a * a

        # Resultado final
        if x is not None:
            print(f"\n>>> FINALIZADO: X = {x}")
        else:
            print("\nOpción no válida seleccionada.")

    except ZeroDivisionError:
        print("\n[!] Error: Se produjo una división por cero. La ecuación puede no tener solución.")
    except Exception as e:
        print(f"\n[!] Error inesperado: {e}")

if __name__ == "__main__":
    resolver()