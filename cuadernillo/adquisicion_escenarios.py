class SimuladorAdquisicionConocimiento:
    """Simula adquisición de conocimiento mediante entrevistas guiadas por escenarios"""

    def __init__(self):
        self.reglas_adquiridas = []
        self.escenarios_clave = [
            {
                "contexto": "Coche no arranca, pero el tablero se ilumina",
                "pregunta_experto": "¿Qué verificaría primero y por qué?",
                "respuesta_experto": "Revisaría el contacto del motor eléctrico. Si el tablero funciona pero el motor no gira, el problema suele estar en la conexión entre batería y motor, no en la batería misma.",
                "regla_extraida": {
                    "condiciones": ["tablero_funciona", "motor_no_gira"],
                    "conclusion": "fallo_contacto_motor",
                    "certeza": 0.85,
                    "explicacion": "El tablero recibe energía directa de la batería; si funciona, la batería está cargada. El motor no gira porque falla la conexión de alto voltaje."
                }
            },
            {
                "contexto": "Autonomía repentinamente baja (50% menos de lo habitual)",
                "pregunta_experto": "¿Qué causas consideraría y en qué orden?",
                "respuesta_experto": "Primero verificaría sensores de temperatura de batería; un sensor defectuoso puede hacer que el sistema limite la potencia pensando que la batería está sobrecalentada. Si los sensores están bien, revisaría celdas individuales de la batería.",
                "regla_extraida": {
                    "condiciones": ["autonomia_reducida_50pct", "sin_cambios_conduccion"],
                    "conclusion": "sensor_temperatura_defectuoso",
                    "certeza": 0.75,
                    "explicacion": "Reducción abrupta sin cambios en hábitos de conducción sugiere fallo en sistema de gestión, no en batería física."
                }
            },
            {
                "contexto": "Ruido metálico al acelerar, pero solo en frío",
                "pregunta_experto": "¿Cómo diferenciaría entre problema mecánico y eléctrico?",
                "respuesta_experto": "Si el ruido desaparece al calentarse el motor, es probablemente contracción térmica en componentes mecánicos (rodamientos), no un problema eléctrico. Los fallos eléctricos no suelen ser dependientes de la temperatura ambiente.",
                "regla_extraida": {
                    "condiciones": ["ruido_metalico", "solo_en_frio", "desaparece_caliente"],
                    "conclusion": "problema_mecanico_rodamientos",
                    "certeza": 0.90,
                    "explicacion": "Dependencia térmica indica origen mecánico; los componentes eléctricos no varían su comportamiento con temperatura ambiente de forma tan marcada."
                }
            },
            {
                "contexto": "El vehículo carga mucho más lento de lo normal en cargador rápido",
                "pregunta_experto": "Si el cargador externo está bien, ¿qué componente del vehículo suele causar esta degradación de velocidad?",
                "respuesta_experto": "Casi siempre es el sistema de refrigeración del inversor o de la batería. Si el refrigerante está bajo o la bomba falla, el sistema reduce la tasa de carga para evitar daños térmicos, aunque no haya una alerta crítica todavía.",
                "regla_extraida": {
                    "condiciones": ["carga_lenta", "cargador_externo_ok", "sin_alertas_criticas"],
                    "conclusion": "fallo_sistema_refrigeracion",
                    "certeza": 0.80,
                    "explicacion": "La gestión térmica prioriza la integridad de la celda reduciendo el amperaje de entrada ante una disipación de calor ineficiente."
                }
            }
        ]

    def simular_entrevista(self):
        """Simula entrevista estructurada con mecánico experto"""
        print("="*70)
        print(" SIMULACIÓN: Adquisición de conocimiento mediante escenarios reales")
        print("="*70)
        print("\nContexto: Estás entrevistando a Carlos, mecánico especialista en coches eléctricos")
        print("con 15 años de experiencia en Tesla y Nissan Leaf.\n")

        for i, escenario in enumerate(self.escenarios_clave, 1):
            print(f" ESCENARIO {i}: {escenario['contexto']}")
            print(f"\n Tú: \"{escenario['pregunta_experto']}\"")
            print(f"\n Carlos: \"{escenario['respuesta_experto']}\"")

            regla = escenario['regla_extraida']
            print(f"\n Regla capturada:")
            print(f"   SI {' Y '.join(regla['condiciones'])}")
            print(f"   ENTONCES {regla['conclusion']} (certeza: {regla['certeza']})")
            print(f"   Explicación: {regla['explicacion']}")
            self.reglas_adquiridas.append(regla)
            print()

        print("="*70)
        print(" RESULTADO DE LA ADQUISICIÓN")
        print("="*70)
        print(f"Reglas capturadas: {len(self.reglas_adquiridas)}")
        print(f"Cobertura estimada del dominio: 65% (según experto)")
        print("\n LECCIÓN CLAVE:")
        print(" Las preguntas abstractas ('¿cómo diagnostica?') generan respuestas genéricas.")
        print(" Los escenarios concretos activan el conocimiento tácito y revelan heurísticas")
        print(" que el experto aplica sin poder verbalizar en una entrevista tradicional.")
        print("\n Ejemplo: Carlos nunca habría mencionado 'verificar sensores de temperatura'")
        print(" si no se le hubiera presentado el escenario de autonomía reducida abruptamente.")

    def validar_reglas(self):
        """Valida reglas mediante casos de prueba realistas"""
        print("\n" + "="*70)
        print(" VALIDACIÓN: ¿Las reglas capturadas funcionan en casos reales?")
        print("="*70)

        casos_prueba = [
            {
                "sintomas": ["tablero_funciona", "motor_no_gira"],
                "esperado": "fallo_contacto_motor",
                "descripcion": "Caso típico de fallo en contacto de motor"
            },
            {
                "sintomas": ["autonomia_reducida_50pct", "sin_cambios_conduccion"],
                "esperado": "sensor_temperatura_defectuoso",
                "descripcion": "Reducción abrupta de autonomía sin cambios en conducción"
            },
            {
                "sintomas": ["ruido_metalico", "solo_en_frio", "desaparece_caliente"],
                "esperado": "problema_mecanico_rodamientos",
                "descripcion": "Ruido dependiente de temperatura ambiente"
            },
            {
                "sintomas": ["carga_lenta", "cargador_externo_ok", "sin_alertas_criticas"],
                "esperado": "fallo_sistema_refrigeracion",
                "descripcion": "Carga lenta por degradación del sistema térmico"
            },
            {
                "sintomas": ["tablero_no_funciona", "luces_apagadas"],
                "esperado": "bateria_agotada",
                "descripcion": "Caso límite: batería completamente descargada (no cubierto por reglas actuales)"
            }
        ]

        aciertos = 0
        for caso in casos_prueba:
            resultado = self._inferir_simple(caso["sintomas"])
            coincidencia = resultado == caso["esperado"]
            if coincidencia:
                aciertos += 1
                simbolo = "✓"
            else:
                simbolo = "✗"

            print(f"\n{simbolo} {caso['descripcion']}")
            print(f"  Síntomas: {', '.join(caso['sintomas'])}")
            print(f"  Diagnóstico: {resultado} (esperado: {caso['esperado']})")

        print("\n" + "="*70)
        print(f"RESULTADO: {aciertos}/{len(casos_prueba)} casos correctos ({aciertos/len(casos_prueba)*100:.0f}%)")
        print("="*70)
        print("\n BRECHA IDENTIFICADA:")
        print(" El caso 5 (batería agotada) no está cubierto por las reglas actuales.")
        print(" Esto revela un límite de la adquisición inicial: no se exploraron escenarios")
        print(" de descarga completa de batería. ¡Necesitamos otra entrevista enfocada en este caso!")

    def _inferir_simple(self, sintomas):
        """Motor de inferencia minimalista para validación"""
        for regla in self.reglas_adquiridas:
            if all(cond in sintomas for cond in regla["condiciones"]):
                return regla["conclusion"]
        return "diagnostico_no_posible"

# Ejecución del simulador
if __name__ == "__main__":
    simulador = SimuladorAdquisicionConocimiento()
    simulador.simular_entrevista()
    simulador.validar_reglas()
    
    print("\n" + "="*70)
    print(" TU TURNO:")
    print("="*70)
    print("1. Diseña un escenario adicional para capturar conocimiento sobre 'carga lenta'")
    print("2. ¿Qué pregunta harías al experto para revelar heurísticas tácitas?")
    print("3. Implementa una regla para ese escenario y valida con un caso de prueba.")
    print("4. Reflexiona: ¿qué otros casos límite podrían no estar cubiertos por las reglas actuales?")