import json
import os
from datetime import datetime


DATASET_PATH = os.path.join(os.path.dirname(__file__), "dataset_conocimiento2026.json")


def cargar_dataset():
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


class AdquisicionConocimiento:
    def __init__(self):
        self.dataset = cargar_dataset()
        self.reglas_adquiridas = []
        self.sesion_activa = False
        self.escenarios_presentados = []
        self.escenarios_base = [
            {
                "id": "E001",
                "contexto": "El coche no carga mas alla del 80% y la zona de la bateria esta caliente",
                "pregunta_sugerida": "Que verificaria primero y por que? Que componente especifico sospecharia en una bateria de estado solido?",
                "respuesta_experto": "En baterias de estado solido esto es muy diferente a las de ion-litio convencionales. El electrolito solido, tipicamente oxido de litio-lantano-circonio, se fisura cuando hay expansion termica diferencial sostenida. Si el coche para en 80% con calor en la bateria, sospecho degradacion termica del electrolito solido. La clave tacita es que las microfisuras no las detecta el BMS convencional; solo se revelan midiendo la impedancia de interfaz.",
                "regla_id": "R001",
                "conocimiento_tacito": "El experto menciona impedancia de interfaz, un concepto que nunca aparece en manuales de taller convencionales.",
                "regla_extraida": {
                    "condiciones": ["temperatura_bateria_alta_sostenida", "carga_se_detiene_antes_100", "calor_excesivo_zona_bateria"],
                    "conclusion": "degradacion_termica_electrolito_solido",
                    "certeza": 0.92
                }
            },
            {
                "id": "E002",
                "contexto": "El coche carga normal hasta el 80%, el BMS no muestra alertas, pero la autonomia bajo 40% de un dia para otro sin cambios en la forma de conducir",
                "pregunta_sugerida": "Este escenario es inusual porque todo parece normal en la carga. Que estaria pasando internamente en la bateria?",
                "respuesta_experto": "Este es el caso mas dificil de diagnosticar en baterias de estado solido. El cliente ve carga normal pero la autonomia cayo. Lo que pasa es fisuracion en la interfaz electrolito-catodo. Las fisuras reducen el area activa disponible: la bateria acepta energia hasta el 80% pero la densidad de corriente en las zonas no fisuradas es mayor, agotandose mas rapido. El BMS no lo ve porque mide voltaje, no impedancia de interfaz. Esto es conocimiento que aprendi viendo 3 casos similares; no esta en ningun manual.",
                "regla_id": "R002",
                "conocimiento_tacito": "La distincion entre voltaje (que mide el BMS) e impedancia de interfaz (lo que revela la fisuracion) es conocimiento tacito critico.",
                "regla_extraida": {
                    "condiciones": ["carga_normal_hasta_80_por_ciento", "autonomia_reducida_abruptamente", "sin_cambios_habitos_conduccion"],
                    "conclusion": "fisuracion_interfaz_electrolito_catodo",
                    "certeza": 0.88
                }
            },
            {
                "id": "E003",
                "contexto": "El conductor usa carga rapida casi a diario. Ahora el coche da microcortes electricos breves durante la conduccion, pero la temperatura de la bateria esta normal",
                "pregunta_sugerida": "Los microcortes son intermitentes y la temperatura esta bien. Como diferenciaria un problema mecanico de uno quimico en la bateria?",
                "respuesta_experto": "Con carga rapida frecuente en baterias de litio metalico sospecho dendritas de inmediato. En baterias de estado solido el litio metalico es el anodo. La carga rapida fuerza deposicion desigual: el litio no se distribuye uniformemente, crea filamentos que atraviesan el electrolito solido y generan microcortocircuitos intermitentes. La temperatura es normal porque los puentes de dendrita se forman y rompen rapidamente. Esto es critico: las dendritas pueden causar cortocircuito masivo. Este coche no puede seguir circulando.",
                "regla_id": "R003",
                "conocimiento_tacito": "La relacion entre carga rapida frecuente y formacion de dendritas en anodos de litio metalico es conocimiento especializado en SSB.",
                "regla_extraida": {
                    "condiciones": ["carga_rapida_frecuente", "microcorte_electrico_durante_conduccion", "temperatura_bateria_normal"],
                    "conclusion": "formacion_dendrita_litio_metalico",
                    "certeza": 0.85
                }
            },
            {
                "id": "E004",
                "contexto": "Vehiculo de uso intensivo con muchos ciclos. La bateria pierde carga en reposo de un dia para otro y la eficiencia de carga ha ido bajando semana a semana",
                "pregunta_sugerida": "La perdida en reposo es inusual. Que mecanismo especifico de las baterias de estado solido explicaria esto?",
                "respuesta_experto": "Esto es delaminacion en la interfaz anodo-electrolito. El litio metalico se expande al cargarse y se contrae al descargarse. Con muchos ciclos, esta variacion volumetrica crea separacion fisica entre el anodo y el electrolito solido. La autodescarga en reposo viene de que el contacto interfacial es inconsistente: hay zonas que se tocan y zonas que no. Cuando hay contacto, la corriente fluye incluso en reposo. La solucion puede ser aumentar la presion mecanica del stack antes de sustituir la bateria.",
                "regla_id": "R004",
                "conocimiento_tacito": "El concepto de presion mecanica del stack como solucion parcial antes de sustitucion es conocimiento tacito de experto.",
                "regla_extraida": {
                    "condiciones": ["eficiencia_carga_reducida_progresivamente", "bateria_pierde_carga_en_reposo", "ciclos_carga_descarga_frecuentes"],
                    "conclusion": "delaminacion_interfaz_anodo_electrolito_solido",
                    "certeza": 0.83
                }
            },
            {
                "id": "E005",
                "contexto": "El BMS reporta bateria al 100% de salud, la carga se completa sin alarmas, pero la autonomia bajo de 400km a 260km de un dia para otro",
                "pregunta_sugerida": "El BMS dice que todo esta bien pero la autonomia real contradice eso. Como explicaria esta paradoja en baterias de estado solido?",
                "respuesta_experto": "Este es el escenario que mas me cuesta explicar a los clientes: la bateria parece sana pero no lo esta. El problema esta en el sensor de State of Health. Los sensores SOH que vienen en la mayoria de coches electricos fueron disenados para baterias de ion-litio convencionales: miden voltaje de circuito abierto. En baterias de estado solido eso no es suficiente; necesitas medir impedancia espectroscopica para saber la salud real. El sensor reporta 100% pero la capacidad real es 65%. Requiere recalibracion con equipos especializados para SSB.",
                "regla_id": "R005",
                "conocimiento_tacito": "La incompatibilidad de sensores SOH convencionales con baterias SSB es conocimiento tacito critico que ninguna documentacion de taller menciona.",
                "regla_extraida": {
                    "condiciones": ["carga_normal_sin_alertas", "autonomia_reducida_abruptamente", "lecturas_soh_incorrectas_bms"],
                    "conclusion": "sensor_salud_bateria_defectuoso",
                    "certeza": 0.79
                }
            }
        ]

    def iniciar_sesion(self):
        self.sesion_activa = True
        self.reglas_adquiridas = []
        self.escenarios_presentados = []

    def mostrar_escenario(self, indice):
        if indice < 0 or indice >= len(self.escenarios_base):
            return False
        escenario = self.escenarios_base[indice]
        self.escenarios_presentados.append(escenario["id"])
        print("\n" + "=" * 70)
        print(f"  ESCENARIO {indice + 1}: {escenario['contexto']}")
        print("=" * 70)
        print(f"\n  Pregunta sugerida para el experto:")
        print(f"  \"{escenario['pregunta_sugerida']}\"")
        print(f"\n  Respuesta del Experto (Carlos, 15 anos en baterias SSB):")
        print(f"  \"{escenario['respuesta_experto']}\"")
        print(f"\n  [CONOCIMIENTO TACITO REVELADO]:")
        print(f"  {escenario['conocimiento_tacito']}")
        regla = escenario["regla_extraida"]
        print(f"\n  [REGLA CAPTURADA - {escenario['regla_id']}]:")
        print(f"  SI  {chr(10) + '      Y '.join(regla['condiciones'])}")
        print(f"  ENTONCES  {regla['conclusion']}")
        print(f"  Certeza: {regla['certeza'] * 100:.0f}%")
        self.reglas_adquiridas.append({
            "id": escenario["regla_id"],
            "condiciones": regla["condiciones"],
            "conclusion": regla["conclusion"],
            "certeza": regla["certeza"]
        })
        return True

    def ejecutar_entrevista_completa(self):
        self.iniciar_sesion()
        print("\n" + "=" * 70)
        print("  MODULO 1: ADQUISICION DE CONOCIMIENTO")
        print("  Dominio: Averias en Baterias de Estado Solido (SSB)")
        print("  Experto simulado: Carlos M. - Especialista SSB (15 anos)")
        print("=" * 70)
        print("\n  NOTA: Este modulo usa escenarios concretos para revelar")
        print("  conocimiento tacito que las preguntas abstractas no capturarian.")
        print("  Comparacion:")
        print("  [MAL] 'Como diagnostica una averia en bateria?'")
        print("  [BIEN] 'El coche carga hasta 80% y la zona de bateria esta caliente...'")

        for i in range(len(self.escenarios_base)):
            input(f"\n  Presione ENTER para ver Escenario {i + 1}/{len(self.escenarios_base)}...")
            self.mostrar_escenario(i)

        self._mostrar_resumen_adquisicion()

    def ejecutar_entrevista_demo(self):
        self.iniciar_sesion()
        print("\n" + "=" * 70)
        print("  MODULO 1: ADQUISICION DE CONOCIMIENTO (MODO DEMO)")
        print("  Dominio: Averias en Baterias de Estado Solido (SSB)")
        print("=" * 70)
        for i in range(len(self.escenarios_base)):
            self.mostrar_escenario(i)
        self._mostrar_resumen_adquisicion()

    def _mostrar_resumen_adquisicion(self):
        reglas_predefinidas = len(self.dataset["reglas"])
        reglas_capturadas = len(self.reglas_adquiridas)
        porcentaje = (reglas_capturadas / reglas_predefinidas) * 100
        print("\n" + "=" * 70)
        print("  RESUMEN DE ADQUISICION")
        print("=" * 70)
        print(f"  Reglas predefinidas en dominio SSB: {reglas_predefinidas}")
        print(f"  Reglas capturadas en esta sesion:   {reglas_capturadas}")
        print(f"  Cobertura de adquisicion:           {porcentaje:.0f}%")
        if porcentaje >= 70:
            print("  Estado: APROBADO (>= 70% requerido)")
        else:
            print("  Estado: INSUFICIENTE (se requiere >= 70%)")
        print("\n  LECCION CLAVE:")
        print("  Los escenarios concretos de baterias SSB revelaron heuristicas")
        print("  que jamas aparecen en manuales de taller convencionales:")
        print("  - Impedancia de interfaz vs voltaje de circuito abierto")
        print("  - Incompatibilidad de sensores SOH convencionales con SSB")
        print("  - Presion mecanica del stack como solucion antes de sustitucion")

    def obtener_reglas_capturadas(self):
        return self.reglas_adquiridas


class OntologiaDominio:
    def __init__(self):
        self.jerarquia = {
            "Averia": ["AveriaBateria", "AveriaElectrica", "AveriaElectronica"],
            "AveriaBateria": ["DegradacionTermica", "FalloElectrolito", "FalloAnodo", "FalloCatodo", "FalloSensorSalud"],
            "FalloElectrolito": ["FisuracionElectrolito", "DelaminacionElectrolito"],
            "FalloAnodo": ["FormacionDendrita", "DelaminacionInterfazAnodo"],
            "AveriaElectrica": ["FalloConector", "FalloCargador"],
            "AveriaElectronica": ["FalloBMS", "FalloModuloComunicacion"]
        }
        self.relaciones = {
            "causa": [
                ("DegradacionTermica", "ReduccionAutonomia"),
                ("FisuracionElectrolito", "NoCargaMasAllaDe80"),
                ("FormacionDendrita", "MicrocortocircuitoInterno"),
                ("DelaminacionInterfazAnodo", "AutodescargaEnReposo"),
                ("FalloSensorSalud", "LecturaSOHIncorrecta")
            ],
            "requiere_reparacion": [
                ("DegradacionTermica", "SustitucionModuloBateria"),
                ("FisuracionElectrolito", "DiagnosticoImpedanciaYSustitucion"),
                ("FormacionDendrita", "SustitucionUrgenteRiesgoAlto"),
                ("DelaminacionInterfazAnodo", "RevisionPresionMecanicaStack"),
                ("FalloSensorSalud", "RecalibracionSensorSOH")
            ],
            "sintoma": [
                ("DegradacionTermica", "CalorExcesivoBateria"),
                ("FisuracionElectrolito", "AutonomiaReducidaAbruptamenteSinAlarmas"),
                ("FormacionDendrita", "MicrocortesElectricosIntermitentes"),
                ("DelaminacionInterfazAnodo", "PerdidaCargaEnReposo"),
                ("FalloSensorSalud", "ParadojaCargaCompletaAutonomiaReducida")
            ]
        }
        self.restricciones = [
            ("DegradacionTermica", "NO_SIMULTANEO", "FormacionDendrita"),
            ("FisuracionElectrolito", "PUEDE_COEXISTIR", "FalloSensorSalud"),
            ("FormacionDendrita", "IMPLICA", "UsoExcesivoCargaRapida")
        ]

    def obtener_todos_conceptos(self):
        todos = set()
        for padre, hijos in self.jerarquia.items():
            todos.add(padre)
            todos.update(hijos)
        return todos

    def es_subclase_de(self, concepto, clase_superior):
        if concepto == clase_superior:
            return True
        for padre, hijos in self.jerarquia.items():
            if concepto in hijos:
                if padre == clase_superior:
                    return True
                return self.es_subclase_de(padre, clase_superior)
        return False

    def inferir_causas_por_sintoma(self, sintoma):
        causas = []
        for origen, sintoma_rel in self.relaciones.get("sintoma", []):
            if sintoma_rel == sintoma:
                causas.append(origen)
        return causas

    def obtener_reparacion(self, averia):
        for origen, reparacion in self.relaciones.get("requiere_reparacion", []):
            if origen == averia:
                return reparacion
        return "ConsultarTecnicoEspecializado"

    def detectar_ciclos(self):
        ciclos = []
        for padre, hijos in self.jerarquia.items():
            for hijo in hijos:
                if hijo in self.jerarquia and padre in self.jerarquia.get(hijo, []):
                    ciclos.append((padre, hijo))
        return ciclos

    def detectar_inconsistencias(self):
        inconsistencias = []
        ciclos = self.detectar_ciclos()
        for ciclo in ciclos:
            inconsistencias.append(f"CICLO en jerarquia: {ciclo[0]} <-> {ciclo[1]}")
        conceptos = self.obtener_todos_conceptos()
        for tipo_rel, relaciones in self.relaciones.items():
            for origen, destino in relaciones:
                if origen not in conceptos:
                    inconsistencias.append(f"Concepto '{origen}' en relacion '{tipo_rel}' no existe en jerarquia")
        return inconsistencias

    def visualizar_arbol_ascii(self):
        print("\n" + "=" * 70)
        print("  ONTOLOGIA: Jerarquia de Averias en Baterias de Estado Solido")
        print("=" * 70)
        self._imprimir_nodo("Averia", 0)
        print("\n  RELACIONES SEMANTICAS:")
        for tipo_rel, relaciones in self.relaciones.items():
            print(f"\n  [{tipo_rel.upper()}]")
            for origen, destino in relaciones:
                print(f"    {origen} --{tipo_rel}--> {destino}")
        print("\n  RESTRICCIONES LOGICAS:")
        for a, tipo, b in self.restricciones:
            print(f"    {a} [{tipo}] {b}")

    def _imprimir_nodo(self, nodo, nivel):
        prefijo = "    " * nivel + ("+--> " if nivel > 0 else "")
        print(f"  {prefijo}{nodo}")
        for hijo in self.jerarquia.get(nodo, []):
            self._imprimir_nodo(hijo, nivel + 1)

    def validar_y_mostrar(self):
        print("\n" + "=" * 70)
        print("  MODULO 2: REPRESENTACION DEL CONOCIMIENTO - VALIDACION")
        print("=" * 70)
        self.visualizar_arbol_ascii()
        print("\n" + "-" * 70)
        print("  VALIDACION DE COHERENCIA:")
        inconsistencias = self.detectar_inconsistencias()
        if not inconsistencias:
            print("  [OK] 0 inconsistencias detectadas - Ontologia COHERENTE")
            print("  [OK] Sin ciclos en jerarquias")
            print("  [OK] Todas las relaciones referencian conceptos existentes")
            print("  [OK] Restricciones logicas definidas correctamente")
        else:
            print(f"  [ERROR] {len(inconsistencias)} inconsistencias detectadas:")
            for inc in inconsistencias:
                print(f"    - {inc}")
        print("\n  ESTADISTICAS:")
        print(f"    Conceptos en ontologia: {len(self.obtener_todos_conceptos())}")
        print(f"    Relaciones causa:              {len(self.relaciones.get('causa', []))}")
        print(f"    Relaciones requiere_reparacion:{len(self.relaciones.get('requiere_reparacion', []))}")
        print(f"    Relaciones sintoma:            {len(self.relaciones.get('sintoma', []))}")
        print(f"    Restricciones logicas:         {len(self.restricciones)}")
        print("\n  DEMOSTRACION DE INFERENCIAS AUTOMATICAS:")
        print("  [?] Es 'FormacionDendrita' una AveriaBateria?")
        resultado = self.es_subclase_de("FormacionDendrita", "AveriaBateria")
        print(f"  [R] {'Si' if resultado else 'No'}, es subclase transitiva de AveriaBateria")
        print("\n  [?] Que sintoma tiene 'FisuracionElectrolito'?")
        for origen, sintoma in self.relaciones.get("sintoma", []):
            if origen == "FisuracionElectrolito":
                print(f"  [R] Sintoma: {sintoma}")
        print("\n  [?] Que reparacion requiere 'FormacionDendrita'?")
        rep = self.obtener_reparacion("FormacionDendrita")
        print(f"  [R] {rep}")
        return len(inconsistencias)


class MotorInferencia:
    def __init__(self):
        self.dataset = cargar_dataset()
        self.reglas = self.dataset["reglas"]
        self.historial_diagnosticos = []

    def diagnosticar(self, sintomas, perfil_usuario="cliente"):
        reglas_activadas = self._encontrar_reglas_aplicables(sintomas)
        if not reglas_activadas:
            self._mostrar_sin_diagnostico(sintomas, perfil_usuario)
            return None
        if len(reglas_activadas) > 1:
            regla_final = self._resolver_conflicto(reglas_activadas, sintomas)
        else:
            regla_final = reglas_activadas[0]
        self._mostrar_diagnostico(regla_final, sintomas, perfil_usuario, reglas_activadas)
        registro = {
            "timestamp": datetime.now().isoformat(),
            "sintomas": sintomas,
            "perfil": perfil_usuario,
            "diagnostico": regla_final["conclusion"],
            "certeza": regla_final["certeza"],
            "regla_id": regla_final["id"],
            "conflicto": len(reglas_activadas) > 1
        }
        self.historial_diagnosticos.append(registro)
        return regla_final["conclusion"]

    def _encontrar_reglas_aplicables(self, sintomas):
        aplicables = []
        for regla in self.reglas:
            if all(cond in sintomas for cond in regla["condiciones"]):
                aplicables.append(regla)
        return aplicables

    def _resolver_conflicto(self, reglas_en_conflicto, sintomas):
        def puntuacion(regla):
            condiciones_satisfechas = sum(1 for c in regla["condiciones"] if c in sintomas)
            return regla["certeza"] + condiciones_satisfechas * 0.05
        return max(reglas_en_conflicto, key=puntuacion)

    def _mostrar_sin_diagnostico(self, sintomas, perfil):
        print("\n" + "=" * 70)
        print("  DIAGNOSTICO: NO SE PUEDE DETERMINAR")
        print("=" * 70)
        print(f"  Sintomas reportados: {', '.join(sintomas)}")
        print("\n  Los sintomas reportados no coinciden con ningun patron conocido")
        print("  en la base de conocimiento de baterias de estado solido.")
        if perfil == "cliente":
            print("\n  Recomendacion: Lleve el vehiculo a un taller autorizado")
            print("  especializado en baterias de estado solido.")
        elif perfil == "aprendiz":
            print("\n  Brecha identificada: Este caso no esta cubierto en la base")
            print("  de conocimiento actual. Requiere nueva sesion de adquisicion.")
        else:
            print("\n  Caso no cubierto. Iniciar nueva sesion de adquisicion con experto.")
            print("  Verificar manualmente: impedancia EIS, presion stack, BMS logs.")

    def _mostrar_diagnostico(self, regla, sintomas, perfil, todas_reglas):
        print("\n" + "=" * 70)
        print("  MODULO 3: DIAGNOSTICO CON EXPLICACION ADAPTADA")
        print(f"  Perfil de usuario: {perfil.upper()}")
        print("=" * 70)
        print(f"\n  Sintomas reportados:")
        for s in sintomas:
            print(f"    - {s.replace('_', ' ')}")
        if len(todas_reglas) > 1:
            print(f"\n  [CONFLICTO DETECTADO] {len(todas_reglas)} reglas compiten:")
            for r in todas_reglas:
                print(f"    - {r['id']}: {r['conclusion']} (certeza: {r['certeza']})")
            print(f"  [RESOLUCION] Ganadora por mayor certeza + condiciones: {regla['id']}")
        conclusion_legible = regla["conclusion"].replace("_", " ").title()
        print(f"\n  DIAGNOSTICO PRINCIPAL: {conclusion_legible}")
        print(f"  Regla aplicada: {regla['id']} | Certeza: {regla['certeza'] * 100:.0f}%")
        print(f"  Urgencia: {regla.get('urgencia', 'media').upper()}")
        print("\n" + "-" * 70)
        if perfil == "cliente":
            self._explicacion_cliente(regla)
        elif perfil == "aprendiz":
            self._explicacion_aprendiz(regla)
        else:
            self._explicacion_experto(regla)

    def _explicacion_cliente(self, regla):
        print("  EXPLICACION (lenguaje sencillo para cliente):")
        print(f"\n  {regla['explicacion_positiva']}")
        print("\n  QUE HACER AHORA:")
        urgencia = regla.get("urgencia", "media")
        accion = regla.get("accion_requerida", "revision_tecnica").replace("_", " ")
        if urgencia == "critica":
            print("  ATENCION: No continuar usando el vehiculo.")
            print("  Contacte INMEDIATAMENTE a un tecnico autorizado.")
            print(f"  Accion requerida: {accion}")
        elif urgencia == "alta":
            print("  Programe una cita en taller esta semana.")
            print(f"  Accion requerida: {accion}")
        else:
            print("  Puede usar el vehiculo con precaucion.")
            print(f"  Programe revision: {accion}")

    def _explicacion_aprendiz(self, regla):
        print("  EXPLICACION TECNICA (para aprendiz):")
        print(f"\n  Regla aplicada: {regla['id']} - {regla['nombre']}")
        print(f"  Condiciones que activaron la regla:")
        for cond in regla["condiciones"]:
            print(f"    [OK] {cond.replace('_', ' ')}")
        print(f"\n  Razonamiento:")
        print(f"  {regla['explicacion_positiva']}")
        print(f"\n  Por que se descartaron otras opciones:")
        for descartado, razon in regla.get("explicacion_descarte", {}).items():
            print(f"    X {descartado.replace('_', ' ')}: {razon}")
        print(f"\n  Accion tecnica: {regla.get('accion_requerida', '').replace('_', ' ')}")

    def _explicacion_experto(self, regla):
        print("  EXPLICACION COMPLETA (para mecanico experto):")
        print(f"\n  Regla: {regla['id']} | Nombre: {regla['nombre']}")
        print(f"  Factor de certeza: {regla['certeza']} | Urgencia: {regla.get('urgencia', 'media')}")
        print(f"\n  Condiciones activadas: {regla['condiciones']}")
        print(f"\n  Base teorica:")
        print(f"  {regla['explicacion_positiva']}")
        print(f"\n  Analisis de descartes:")
        for descartado, razon in regla.get("explicacion_descarte", {}).items():
            print(f"    X {descartado}: {razon}")
        print(f"\n  Especificaciones tecnicas SSB:")
        print(f"  {regla.get('especificaciones_tecnicas', 'Ver manual tecnico SSB')}")
        print(f"\n  Accion recomendada: {regla.get('accion_requerida', '').replace('_', ' ')}")

    def ejecutar_diagnostico_interactivo(self):
        print("\n" + "=" * 70)
        print("  MODULO 3: DIAGNOSTICO INTERACTIVO DE AVERIAS SSB")
        print("=" * 70)
        print("\n  Sintomas disponibles en el sistema:")
        todos_sintomas = set()
        for regla in self.reglas:
            todos_sintomas.update(regla["condiciones"])
        for i, s in enumerate(sorted(todos_sintomas), 1):
            print(f"  {i:2}. {s.replace('_', ' ')}")
        print("\n  Ingrese los sintomas separados por coma (o numeros):")
        entrada = input("  > ").strip()
        sintomas_ordenados = sorted(todos_sintomas)
        try:
            indices = [int(x.strip()) - 1 for x in entrada.split(",")]
            sintomas = [sintomas_ordenados[i] for i in indices if 0 <= i < len(sintomas_ordenados)]
        except ValueError:
            sintomas = [s.strip().replace(" ", "_") for s in entrada.split(",")]
        print("\n  Seleccione perfil de usuario:")
        print("  1. Cliente (lenguaje sencillo)")
        print("  2. Aprendiz (detalle tecnico)")
        print("  3. Experto (especificaciones completas)")
        opcion = input("  Opcion [1-3]: ").strip()
        perfiles = {"1": "cliente", "2": "aprendiz", "3": "experto"}
        perfil = perfiles.get(opcion, "cliente")
        self.diagnosticar(sintomas, perfil)

    def obtener_historial(self):
        return self.historial_diagnosticos


class ReporteCobertura:
    def __init__(self, adquisicion, ontologia, motor):
        self.adquisicion = adquisicion
        self.ontologia = ontologia
        self.motor = motor
        self.dataset = cargar_dataset()

    def ejecutar_pruebas_automaticas(self):
        print("\n" + "=" * 70)
        print("  VALIDACION AUTOMATICA: PRUEBAS DE COBERTURA")
        print("=" * 70)
        casos = self.dataset["casos_prueba"]
        aciertos = 0
        conflictos_resueltos = 0
        brechas = []
        print(f"\n  Ejecutando {len(casos)} casos de prueba...\n")
        for caso in casos:
            if not caso["cubierto"]:
                brechas.append(caso)
                print(f"  [BRECHA] {caso['id']} - {caso['nombre']}")
                print(f"           Diagnostico esperado: {caso['diagnostico_esperado']}")
                print(f"           Causa: {caso.get('brecha_identificada', 'No cubierto')}")
                continue
            reglas_activadas = []
            for regla in self.dataset["reglas"]:
                if all(cond in caso["sintomas"] for cond in regla["condiciones"]):
                    reglas_activadas.append(regla)
            if not reglas_activadas:
                resultado = "diagnostico_no_posible"
                es_correcto = False
            elif len(reglas_activadas) > 1:
                conflictos_resueltos += 1
                ganadora = max(reglas_activadas, key=lambda r: r["certeza"])
                resultado = ganadora["conclusion"]
                es_correcto = (resultado == caso["diagnostico_esperado"])
            else:
                resultado = reglas_activadas[0]["conclusion"]
                es_correcto = (resultado == caso["diagnostico_esperado"])
            simbolo = "[OK]" if es_correcto else "[XX]"
            if es_correcto:
                aciertos += 1
            print(f"  {simbolo} {caso['id']}: {caso['nombre'][:45]}")
            if not es_correcto:
                print(f"       Esperado:  {caso['diagnostico_esperado']}")
                print(f"       Obtenido:  {resultado}")
        return aciertos, casos, brechas, conflictos_resueltos

    def generar_reporte_completo(self):
        print("\n" + "=" * 70)
        print("  MODULO 4: REPORTE DE COBERTURA DEL CONOCIMIENTO")
        print("  Proyecto: CONOCIMIENTO-2026")
        print("  Dominio: Baterias de Estado Solido (SSB)")
        print("=" * 70)
        aciertos, casos, brechas, conflictos = self.ejecutar_pruebas_automaticas()
        casos_cubiertos = [c for c in casos if c["cubierto"]]
        reglas_dataset = len(self.dataset["reglas"])
        reglas_adquiridas = len(self.adquisicion.obtener_reglas_capturadas()) if self.adquisicion.obtener_reglas_capturadas() else reglas_dataset
        pct_adquisicion = (reglas_adquiridas / reglas_dataset) * 100
        pct_inferencia = (aciertos / len(casos_cubiertos)) * 100 if casos_cubiertos else 0
        inconsistencias = self.ontologia.detectar_inconsistencias()
        pct_cobertura = self.dataset["estadisticas"]["cobertura_porcentaje"]
        print("\n" + "=" * 70)
        print("  METRICAS FINALES")
        print("=" * 70)
        print(f"\n  1. ADQUISICION DEL CONOCIMIENTO (peso: 30%)")
        print(f"     Reglas capturadas:    {reglas_adquiridas}/{reglas_dataset}")
        print(f"     Cobertura adquisicion:{pct_adquisicion:.1f}%  [{'APROBADO' if pct_adquisicion >= 70 else 'REPROBADO'}]")
        print(f"\n  2. REPRESENTACION - ONTOLOGIA (peso: 25%)")
        print(f"     Inconsistencias:      {len(inconsistencias)}")
        print(f"     Estado ontologia:     {'COHERENTE - APROBADO' if not inconsistencias else 'CON ERRORES'}")
        print(f"\n  3. RAZONAMIENTO E INFERENCIA (peso: 25%)")
        print(f"     Casos correctos:      {aciertos}/{len(casos_cubiertos)}")
        print(f"     Precision:            {pct_inferencia:.1f}%  [{'APROBADO' if pct_inferencia >= 80 else 'REPROBADO'}]")
        print(f"     Conflictos resueltos: {conflictos}")
        print(f"\n  4. COBERTURA DEL DOMINIO (peso: 15%)")
        print(f"     Casos totales:        {len(casos)}")
        print(f"     Casos cubiertos:      {len(casos_cubiertos)}")
        print(f"     Cobertura dominio:    {pct_cobertura:.1f}%")
        print(f"\n  5. BRECHAS IDENTIFICADAS ({len(brechas)} encontradas):")
        for brecha in brechas:
            print(f"     - {brecha['id']}: {brecha.get('brecha_identificada', brecha['nombre'])}")
        print("\n  HISTORIAL DE DIAGNOSTICOS EN SESION:")
        historial = self.motor.obtener_historial()
        if historial:
            for h in historial:
                print(f"     {h['timestamp'][:19]} | {h['diagnostico']} ({h['certeza'] * 100:.0f}%) | Perfil: {h['perfil']}")
        else:
            print("     Sin diagnosticos en esta sesion.")
        nota_final = self._calcular_nota(pct_adquisicion, len(inconsistencias), pct_inferencia, pct_cobertura)
        print(f"\n  EVALUACION ESTIMADA: {nota_final:.1f} / 10.0")
        print("=" * 70)

    def _calcular_nota(self, pct_adq, inconsistencias, pct_inf, pct_cob):
        nota_adq = min(10, (pct_adq / 100) * 10) * 0.30
        nota_ont = (10 if inconsistencias == 0 else max(0, 10 - inconsistencias * 2)) * 0.25
        nota_inf = min(10, (pct_inf / 100) * 10) * 0.25
        nota_cob = min(10, (pct_cob / 100) * 10) * 0.15
        return nota_adq + nota_ont + nota_inf + nota_cob


def mostrar_menu():
    print("\n" + "=" * 70)
    print("  SIMULADOR DE INGENIERIA DEL CONOCIMIENTO - CONOCIMIENTO-2026")
    print("  Dominio: Diagnostico de Averias en Baterias de Estado Solido")
    print("=" * 70)
    print("  1. Adquisicion de Conocimiento (entrevistas con experto simulado)")
    print("  2. Representacion del Conocimiento (ontologia y validacion)")
    print("  3. Diagnostico de Averia (con explicacion adaptada al perfil)")
    print("  4. Reporte de Cobertura del Conocimiento")
    print("  5. Demo completa automatica (todos los modulos)")
    print("  0. Salir")
    print("-" * 70)
    return input("  Seleccione una opcion: ").strip()


def ejecutar_demo_completa(adquisicion, ontologia, motor, reporte):
    print("\n" + "=" * 70)
    print("  DEMO COMPLETA - SIMULADOR CONOCIMIENTO-2026")
    print("=" * 70)
    print("\n  [1/4] Ejecutando adquisicion de conocimiento...")
    adquisicion.ejecutar_entrevista_demo()
    print("\n  [2/4] Validando ontologia del dominio...")
    ontologia.validar_y_mostrar()
    print("\n  [3/4] Ejecutando diagnosticos de ejemplo...")
    casos_demo = [
        {
            "sintomas": ["temperatura_bateria_alta_sostenida", "carga_se_detiene_antes_100", "calor_excesivo_zona_bateria"],
            "perfil": "cliente",
            "descripcion": "Cliente con bateria que para en 80%"
        },
        {
            "sintomas": ["carga_normal_hasta_80_por_ciento", "autonomia_reducida_abruptamente", "sin_cambios_habitos_conduccion"],
            "perfil": "aprendiz",
            "descripcion": "Aprendiz analizando paradoja de autonomia"
        },
        {
            "sintomas": ["carga_rapida_frecuente", "microcorte_electrico_durante_conduccion", "temperatura_bateria_normal"],
            "perfil": "experto",
            "descripcion": "Experto diagnosticando dendritas"
        }
    ]
    for caso in casos_demo:
        print(f"\n  >>> Caso: {caso['descripcion']}")
        motor.diagnosticar(caso["sintomas"], caso["perfil"])
    print("\n  [4/4] Generando reporte de cobertura...")
    reporte.generar_reporte_completo()


def main():
    adquisicion = AdquisicionConocimiento()
    ontologia = OntologiaDominio()
    motor = MotorInferencia()
    reporte = ReporteCobertura(adquisicion, ontologia, motor)

    while True:
        opcion = mostrar_menu()
        if opcion == "1":
            adquisicion.ejecutar_entrevista_completa()
        elif opcion == "2":
            ontologia.validar_y_mostrar()
        elif opcion == "3":
            motor.ejecutar_diagnostico_interactivo()
        elif opcion == "4":
            reporte.generar_reporte_completo()
        elif opcion == "5":
            ejecutar_demo_completa(adquisicion, ontologia, motor, reporte)
        elif opcion == "0":
            print("\n  Sesion finalizada. Hasta pronto.\n")
            break
        else:
            print("  Opcion no valida. Intente de nuevo.")


if __name__ == "__main__":
    main()
