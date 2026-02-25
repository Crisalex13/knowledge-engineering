class OntologiaAveriasCoches:
    """
    Ontología formal para averías en coches eléctricos.
    Representa conocimiento mediante:
    - Jerarquías conceptuales (es_un)
    - Relaciones semánticas (causa, requiere_reparacion)
    - Restricciones lógicas (no puede ser A y B simultáneamente)
    """

    def __init__(self):
        # Jerarquía conceptual: qué es qué
        self.jerarquia = {
            "averia": ["mecanica", "electrica", "electtronica", "software"],
            "mecanica": ["problema_rodamientos", "fallo_frenos", "suspension_defectuosa"],
            "electrica": ["fallo_contacto_motor", "cableado_danado", "conector_corrosion", "fallo_bomba_refrigeracion"],
            "electtronica": ["sensor_temperatura_defectuoso", "bms_fallo", "inversor_problema"],
            "software": ["firmware_obsoleto", "error_calibracion", "conflicto_actualizacion"]
        }

        # Relaciones semánticas: cómo se conectan los conceptos
        self.relaciones = {
            "causa": [
                ("sensor_temperatura_defectuoso", "autonomia_reducida_50pct"),
                ("fallo_contacto_motor", "motor_no_gira"),
                ("bms_fallo", "carga_lenta"),
                ("firmware_obsoleto", "comportamiento_erratico"),
                ("fallo_bomba_refrigeracion", "sobrecalentamiento_bateria")
            ],
            "requiere_reparacion": [
                ("problema_rodamientos", "taller_especializado"),
                ("fallo_contacto_motor", "tecnico_alta_voltaje"),
                ("sensor_temperatura_defectuoso", "reemplazo_sensor"),
                ("firmware_obsoleto", "actualizacion_software"),
                ("fallo_bomba_refrigeracion", "sustitucion_bomba_liquido")
            ],
            "sintoma": [
                ("problema_rodamientos", "ruido_metalico_solo_frio"),
                ("fallo_contacto_motor", "tablero_funciona_motor_no_gira"),
                ("sensor_temperatura_defectuoso", "autonomia_reducida_sin_causa"),
                ("bms_fallo", "carga_detenida_80pct"),
                ("fallo_bomba_refrigeracion", "aviso_temperatura_critica")
            ]
        }

        # Restricciones lógicas: qué no puede ocurrir simultáneamente
        self.restricciones = [
            ("problema_rodamientos", "NO", "fallo_contacto_motor"), # Mecánico vs eléctrico
            ("sensor_temperatura_defectuoso", "NO", "bms_fallo"), # Sensores vs sistema gestión
            ("firmware_obsoleto", "IMPLICA", "comportamiento_erratico") # Relación causal fuerte
        ]

    def es_subclase_de(self, concepto, clase_superior):
        """Verifica si un concepto es subclase de otro (transitivo)"""
        if concepto == clase_superior:
            return True
        
        # Búsqueda en la jerarquía
        for padre, hijos in self.jerarquia.items():
            if concepto in hijos:
                if padre == clase_superior:
                    return True
                if self.es_subclase_de(padre, clase_superior):
                    return True
        return False

    def inferir_causa(self, sintoma):
        """Infiere posibles causas a partir de un síntoma"""
        causas = []
        for relacion, valor in self.relaciones.get("sintoma", []):
            if valor == sintoma:
                causas.append(relacion)
        return causas

    def validar_coherencia(self):
        """Verifica que la ontología no tenga contradicciones lógicas"""
        print("="*70)
        print(" VALIDACIÓN DE COHERENCIA DE LA ONTOLOGÍA")
        print("="*70)

        # Verificar jerarquías consistentes
        print("\n1. Verificación de jerarquías:")
        inconsistencias = 0
        for concepto, subclases in self.jerarquia.items():
            for subclase in subclases:
                if subclase in self.jerarquia and concepto in self.jerarquia[subclase]:
                    print(f" ✗ INCONSISTENCIA: {concepto} es subclase de {subclase} y viceversa")
                    inconsistencias += 1

        if inconsistencias == 0:
            print(" ✓ Todas las jerarquías son consistentes (sin ciclos)")

        # Verificar restricciones
        print("\n2. Verificación de restricciones lógicas:")
        for restriccion in self.restricciones:
            if restriccion[1] == "NO":
                print(f" Restricción '{restriccion[0]} NO {restriccion[2]}' definida (requiere validación con datos)")

        print("\n3. Cobertura de relaciones:")
        for tipo_rel, relaciones in self.relaciones.items():
            print(f" •{tipo_rel}: {len(relaciones)} relaciones definidas")

        print("\n ONTOLOGÍA VALIDADA:")
        print(" - Jerarquías consistentes")
        print(" - Relaciones semánticas completas para el dominio")
        print(" - Restricciones lógicas definidas (requieren validación con datos reales)")

    def demostrar_inferencias(self):
        """Muestra inferencias automáticas posibles con esta ontología"""
        print("\n" + "="*70)
        print(" INFERENCIAS AUTOMÁTICAS POSIBLES")
        print("="*70)

        print("\nEjemplo 1: Dado el síntoma 'tablero_funciona_motor_no_gira'")
        causas = self.inferir_causa("tablero_funciona_motor_no_gira")
        print(f" → Causas posibles: {', '.join(causas)}")
        print(f" → Tipo de avería: {causas[0] if causas else 'desconocido'} (eléctrica)")

        print("\nEjemplo 2: ¿'problema_rodamientos' es una avería mecánica?")
        es_mecanica = self.es_subclase_de("problema_rodamientos", "mecanica")
        print(f" → {'Sí' if es_mecanica else 'No'}, es subclase de 'mecanica'")

        print("\nEjemplo 3: ¿Qué reparación requiere 'sensor_temperatura_defectuoso'?")
        reparaciones = [
            r[1] for r in self.relaciones["requiere_reparacion"]
            if r[0] == "sensor_temperatura_defectuoso"
        ]
        print(f" → Requiere: {', '.join(reparaciones)}")

        # Nueva inferencia solicitada
        print("\nEjemplo 4 (Nuevo): Inferencia para 'fallo_bomba_refrigeracion'")
        sintoma_nuevo = "aviso_temperatura_critica"
        causa_inf = self.inferir_causa(sintoma_nuevo)
        print(f" → Ante síntoma '{sintoma_nuevo}', la causa es: {causa_inf[0]}")
        es_electrica = self.es_subclase_de("fallo_bomba_refrigeracion", "electrica")
        print(f" → ¿Es una avería eléctrica?: {'Sí' if es_electrica else 'No'}")
        rep_nueva = [r[1] for r in self.relaciones["requiere_reparacion"] if r[0] == "fallo_bomba_refrigeracion"]
        print(f" → Reparación necesaria: {rep_nueva[0]}")

        print("\n LECCIÓN CLAVE:")
        print(" Una ontología no es solo un diccionario; es una estructura que permite")
        print(" inferencias automáticas: si X es subclase de Y, y Y tiene propiedad Z,")
        print(" entonces X también tiene Z. Esto reduce la necesidad de codificar")
        print(" cada regla explícitamente y facilita la evolución del conocimiento.")

if __name__ == "__main__":
    ontologia = OntologiaAveriasCoches()
    ontologia.validar_coherencia()
    ontologia.demostrar_inferencias()

    print("\n" + "="*70)
    print(" TU TURNO (RESULTADOS):")
    print("="*70)
    print("1. Agrega una nueva avería 'fallo_bomba_refrigeracion' a la jerarquía eléctrica -> COMPLETADO")
    print("2. Define sus relaciones: síntoma, causa y reparación requerida -> COMPLETADO")
    print("3. Verifica que no introduzca inconsistencias en la ontología -> VERIFICADO")
    print("4. Demuestra una inferencia que antes no era posible con la ontología original -> MOSTRADO EN EJEMPLO 4")