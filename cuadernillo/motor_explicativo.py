class MotorInferenciaExplicativo:
    """
    Motor de inferencia que genera explicaciones comprensibles
    para cada diagnóstico, mostrando qué reglas se aplicaron y por qué.
    """

    def __init__(self):
        self.reglas = [
            {
                "id": "R1",
                "condiciones": ["tablero_funciona", "motor_no_gira"],
                "conclusion": "fallo_contacto_motor",
                "certeza": 0.85,
                "explicacion_positiva": (
                    "El tablero funciona, lo que indica que la batería está cargada. "
                    "Pero el motor no gira, lo que sugiere un fallo en la conexión "
                    "de alto voltaje entre batería y motor."
                ),
                "explicacion_descarte": {
                    "bateria_agotada": "Descartado porque el tablero funciona, lo que requiere energía de la batería.",
                    "fallo_motor": "Menos probable porque el fallo sería total (ni tablero ni motor); aquí el tablero funciona."
                }
            },
            {
                "id": "R2",
                "condiciones": ["autonomia_reducida_50pct", "sin_cambios_conduccion"],
                "conclusion": "sensor_temperatura_defectuoso",
                "certeza": 0.75,
                "explicacion_positiva": (
                    "La autonomía se redujo abruptamente sin cambios en hábitos de conducción. "
                    "Esto es típico de un sensor de temperatura defectuoso que hace que el sistema "
                    "limite la potencia pensando que la batería está sobrecalentada."
                ),
                "explicacion_descarte": {
                    "bateria_danada": "Menos probable porque una batería dañada mostraría degradación gradual, no abrupta.",
                    "conduccion_agresiva": "Descartado porque el usuario confirmó que sus hábitos de conducción no cambiaron."
                }
            },
            {
                "id": "R3",
                "condiciones": ["ruido_metalico", "solo_en_frio", "desaparece_caliente"],
                "conclusion": "problema_mecanico_rodamientos",
                "certeza": 0.90,
                "explicacion_positiva": (
                    "El ruido metálico aparece solo cuando el coche está frío y desaparece al calentarse. "
                    "Esta dependencia térmica es característica de problemas mecánicos en rodamientos, "
                    "donde la contracción térmica genera holguras que desaparecen al expandirse los metales."
                ),
                "explicacion_descarte": {
                    "fallo_electronico": "Descartado porque los fallos electrónicos no suelen ser dependientes de la temperatura ambiente.",
                    "problema_motor": "Menos probable porque un problema en el motor eléctrico no mostraría esta dependencia térmica tan marcada."
                }
            },
            {
                "id": "R4",
                "condiciones": ["carga_lenta", "cargador_externo_ok"],
                "conclusion": "degradacion_gestion_termica",
                "certeza": 0.80,
                "explicacion_positiva": (
                    "La velocidad de carga es baja a pesar de que el cargador externo funciona correctamente. "
                    "Esto indica que el sistema de gestión térmica del vehículo está limitando la entrada de corriente "
                    "para proteger las celdas de un posible sobrecalentamiento o debido a una alta resistencia interna."
                ),
                "explicacion_descarte": {
                    "fallo_cargador": "Descartado porque se confirmó que el cargador externo está en parámetros óptimos.",
                    "bateria_fria": "Menos probable si el síntoma persiste tras varios minutos de conexión activa."
                }
            }
        ]

    def diagnosticar(self, sintomas, perfil_usuario="experto"):
        """
        Genera diagnóstico con explicación adaptada al perfil del usuario.
        Perfiles: 'experto', 'estudiante', 'cliente'
        """
        print("="*70)
        print(" DIAGNÓSTICO DE AVERÍAS EN COCHE ELÉCTRICO")
        print("="*70)
        print(f"\nSíntomas reportados: {', '.join(sintomas)}")

        # Buscar regla que coincida
        regla_aplicable = None
        for regla in self.reglas:
            if all(cond in sintomas for cond in regla["condiciones"]):
                regla_aplicable = regla
                break

        if not regla_aplicable:
            print("\n NO SE PUEDE REALIZAR UN DIAGNÓSTICO CONFIABLE")
            print(" Los síntomas reportados no coinciden con patrones conocidos.")
            print(" Recomendación: Visitar taller especializado para diagnóstico manual.")
            return

        # Generar explicación según perfil
        print(f"\n DIAGNÓSTICO: {regla_aplicable['conclusion'].replace('_', ' ').title()}")
        print(f" Certeza: {regla_aplicable['certeza']*100:.0f}%")

        if perfil_usuario == "cliente":
            print("\n EXPLICACIÓN PARA USUARIO FINAL:")
            print(f" {regla_aplicable['explicacion_positiva']}")
            print("\n ¿Qué hacer ahora?")
            if regla_aplicable['conclusion'] == "fallo_contacto_motor":
                print(" → Contactar a servicio técnico autorizado para revisión del sistema de alto voltaje.")
                print(" → No intentar reparar por cuenta propia: riesgo de descarga eléctrica.")
            elif regla_aplicable['conclusion'] == "sensor_temperatura_defectuoso":
                print(" → Programar cita en taller para reemplazo del sensor de temperatura de batería.")
                print(" → El coche es seguro para conducir, pero la autonomía seguirá reducida hasta la reparación.")
            elif regla_aplicable['conclusion'] == "problema_mecanico_rodamientos":
                print(" → Visitar taller mecánico para inspección de rodamientos del motor.")
                print(" → Conducir con precaución: el ruido debería desaparecer al calentarse el motor.")
            elif regla_aplicable['conclusion'] == "degradacion_gestion_termica":
                print(" → Realizar un ciclo de equilibrado de celdas mediante carga lenta AC.")
                print(" → Si el problema persiste, revisar bomba de refrigerante.")

        elif perfil_usuario == "estudiante":
            print("\n EXPLICACIÓN PARA ESTUDIANTE (detalle técnico):")
            print(f" Regla aplicada: {regla_aplicable['id']}")
            print(f" Condiciones satisfechas: {', '.join(regla_aplicable['condiciones'])}")
            print(f" Conclusión: {regla_aplicable['conclusion']}")
            print(f"\n Razonamiento:")
            print(f" {regla_aplicable['explicacion_positiva']}")
            print(f"\n ¿Por qué se descartaron otras opciones?")
            for descartado, razon in regla_aplicable['explicacion_descarte'].items():
                print(f" • {descartado.replace('_', ' ').title()}: {razon}")

        elif perfil_usuario == "ingeniero":
            print("\n EXPLICACIÓN PARA INGENIERO (Telemetría y Sensores):")
            print(f" Regla: {regla_aplicable['id']} | Certeza: {regla_aplicable['certeza']}")
            print(f" Condiciones activadas: {regla_aplicable['condiciones']}")
            print(f"\n Base teórica: {regla_aplicable['explicacion_positiva']}")
            print(f"\n Análisis de descartes:")
            for descartado, razon in regla_aplicable['explicacion_descarte'].items():
                print(f" ✗ {descartado}: {razon}")
            print(f"\n Recomendación técnica: {self._recomendacion_tecnica(regla_aplicable['conclusion'])}")

        else: # experto
            print("\n EXPLICACIÓN PARA EXPERTO (máximo detalle):")
            print(f" Regla: {regla_aplicable['id']} | Certeza: {regla_aplicable['certeza']}")
            print(f" Condiciones activadas: {regla_aplicable['condiciones']}")
            print(f"\n Base teórica: {regla_aplicable['explicacion_positiva']}")
            print(f"\n Análisis de descartes:")
            for descartado, razon in regla_aplicable['explicacion_descarte'].items():
                print(f" ✗ {descartado}: {razon}")
            print(f"\n Recomendación técnica: {self._recomendacion_tecnica(regla_aplicable['conclusion'])}")

    def _recomendacion_tecnica(self, averia):
        """Genera recomendación técnica específica para cada avería"""
        if averia == "fallo_contacto_motor":
            return "Inspeccionar conectores de alto voltaje; verificar corrosión y torque de conexiones."
        elif averia == "sensor_temperatura_defectuoso":
            return "Reemplazar sensor NTC en módulo de batería; calibrar sistema BMS tras reemplazo."
        elif averia == "problema_mecanico_rodamientos":
            return "Desmontar motor para inspección de rodamientos; verificar holguras según especificaciones."
        elif averia == "degradacion_gestion_termica":
            return "Verificar flujo de refrigerante en intercambiador de calor; monitorizar gradiente de temperatura entre celdas."
        return "Requiere diagnóstico manual por técnico especializado."

# Demostración interactiva
if __name__ == "__main__":
    motor = MotorInferenciaExplicativo()

    print("\n" + "="*70)
    print(" DEMOSTRACIÓN: Explicaciones adaptadas a distintos perfiles de usuario")
    print("="*70)

    print("\n[1] DIAGNÓSTICO CARGA LENTA PARA INGENIERO (perfil: ingeniero)")
    motor.diagnosticar(
        sintomas=["carga_lenta", "cargador_externo_ok"],
        perfil_usuario="ingeniero"
    )

    print("\n\n[2] DIAGNÓSTICO CON CONFLICTO (perfil: experto)")
    motor.reglas.append({
        "id": "R_COMPETENCIA",
        "condiciones": ["ruido_metalico", "solo_en_frio"],
        "conclusion": "desgaste_engranajes_reductora",
        "certeza": 0.50,
        "explicacion_positiva": "Posible desgaste en la etapa de reducción.",
        "explicacion_descarte": {"otros": "N/A"}
    })
    motor.diagnosticar(
        sintomas=["ruido_metalico", "solo_en_frio", "desaparece_caliente"],
        perfil_usuario="experto"
    )

    print("\n" + "="*70)
    print(" LECCIÓN FUNDAMENTAL:")
    print("="*70)
    print(" La explicabilidad está integrada en el diseño del motor de inferencia.")
    print(" Cada regla incluye explicación positiva, de descartes y adaptación al perfil.")

    print("\n TU TURNO:")
    print(" 1. Agrega una nueva regla para 'carga_lenta' con explicaciones completas.")
    print(" 2. Implementa un perfil 'ingeniero' con detalles de sensores y voltajes.")
    print(" 3. Diseña un caso donde dos reglas compiten.")
    print(" 4. Reflexiona: ¿Qué pasaría si el sistema no explicara los descartes?")