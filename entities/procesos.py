import sympy as sp


class Proceso:
    def __init__(
            self,
            proceso: tuple,
            moles=1,
            R=0.082,
            gamma=2,
            **kwargs
    ) -> None:
        self.R = R
        self.moles = moles
        self.proceos = proceso
        self.variables = {key: self._process_argument(
            key, value) for key, value in kwargs.items()}

        # Nombre de variables en el diccionrio
        Pinicial = f'P{proceso[0]}'
        Pfinal = f'P{proceso[1]}'
        Vinicial = f'V{proceso[0]}'
        Vfinal = f'V{proceso[1]}'
        Tinicial = f'T{proceso[0]}'
        Tfinal = f'T{proceso[1]}'

        # Ecuaciones de gases ideal (Necesarias para todo los procesos)
        self.ecuacion_gas_inicial = (
            self.variables[Pinicial]*self.variables[Vinicial] -
            self.moles*self.R*self.variables[Tinicial]
        )
        self.ecuacion_gas_final = (
            self.variables[Pfinal]*self.variables[Vfinal] -
            self.moles*self.R*self.variables[Tfinal]
        )

    @staticmethod
    def _process_argument(key, arg):
        """
        Procesa un argumento:
        - Si es texto, retorna un valor predeterminado.
        - Si no, retorna el argumento original.
        """
        if isinstance(arg, str):
            return sp.symbols(key)
        return arg


class ProcesoAdiabatio(Proceso):
    def __init__(
        self, proceso: tuple, moles,  R=0.082, gamma=2, **kwargs
    ) -> None:
        super().__init__(proceso, moles, R, gamma, **kwargs)
        self.gamma = gamma

        # Nombre de variables en el diccionrio
        Pinicial = f'P{proceso[0]}'
        Pfinal = f'P{proceso[1]}'
        Vinicial = f'V{proceso[0]}'
        Vfinal = f'V{proceso[1]}'

        # P*V**gamma = constante
        ecuacion_estado1 = (
            self.variables[Pinicial]*self.variables[Vinicial]**gamma
        )
        ecuacion_estado2 = (
            self.variables[Pfinal]*self.variables[Vfinal]**gamma
        )

        # Ecuacion1 = Ecuacion2
        self.ecuacion_proceso = ecuacion_estado1 - ecuacion_estado2


class ProcesoIsotermico(Proceso):
    def __init__(
        self, proceso: tuple, moles=1, R=0.082, gamma=2, **kwargs
    ) -> None:
        super().__init__(proceso, moles, R, gamma, **kwargs)

        # Nombre de variables en el diccionrio
        Tinicial = f'T{proceso[0]}'
        Tfinal = f'T{proceso[1]}'

        # T = constante
        ecuacion_estado1 = (
            self.variables[Tinicial]
        )
        ecuacion_estado2 = (
            self.variables[Tfinal]
        )

        # Ecuacion1 = Ecuacion2
        self.ecuacion_proceso = ecuacion_estado1 - ecuacion_estado2


class ProcesoIsobarico(Proceso):
    def __init__(
        self, proceso: tuple, moles=1, R=0.082, gamma=2, **kwargs
    ) -> None:
        super().__init__(proceso, moles, R, gamma, **kwargs)

        # Nombre de variables en el diccionrio
        Pinicial = f'P{proceso[0]}'
        Pfinal = f'P{proceso[1]}'

        # P = constante
        ecuacion_estado1 = (
            self.variables[Pinicial]
        )
        ecuacion_estado2 = (
            self.variables[Pfinal]
        )

        # Ecuacion1 = Ecuacion2
        self.ecuacion_proceso = ecuacion_estado1 - ecuacion_estado2


class ProcesoIsocorico(Proceso):
    def __init__(
        self, proceso: tuple, moles=1, R=0.082, gamma=2, **kwargs
    ) -> None:
        super().__init__(proceso, moles, R, gamma, **kwargs)

        # Nombre de variables en el diccionrio
        Vinicial = f'V{proceso[0]}'
        Vfinal = f'V{proceso[1]}'

        # V = constante
        ecuacion_estado1 = (
            self.variables[Vinicial]
        )
        ecuacion_estado2 = (
            self.variables[Vfinal]
        )

        # Ecuacion1 = Ecuacion2
        self.ecuacion_proceso = ecuacion_estado1 - ecuacion_estado2


class ProcesosAgrupados:
    procesos_id = list(range(1, 5, 1))
    cantidad_procesos = 4

    # Creacion de diccionario con variables {str:str}
    variables = []
    for i in range(4):
        variables.append(f'T{i+1}')
        variables.append(f'P{i+1}')
        variables.append(f'V{i+1}')
    variables = {f'{item}': f'{item}' for item in variables}

    def __init__(
        self, procesos_seleccionado: list[int],
        constantes: dict[float],
        datos_conocidos: dict[str:float]
    ) -> None:

        # Encontrando las incognitas y guardo variables para sis de ecuaciones
        self.datos_conocidos = datos_conocidos
        nombres_datos_conocidos = self.datos_conocidos.keys()

        self.incognitas = list()
        for variable in self.variables.keys():
            if variable in nombres_datos_conocidos:
                self.variables[variable] = self.datos_conocidos[variable]
            else:
                self.incognitas.append(self.variables[variable])

        # Todos las clases de procesos para su seleccion
        self.procesos_disponibles = [
            ProcesoIsotermico, ProcesoAdiabatio,
            ProcesoIsocorico, ProcesoIsobarico
        ]

        # Seleecion de los procesos (lista con procesos seleecionados)
        self.seleccion_usuario = [
            self.procesos_disponibles[i] for i in procesos_seleccionado
        ]

        # Organizador de procesos
        self.procesos_instanciados = []

        # Separar datos para cada uno de los 4 procesos
        for i in range(self.cantidad_procesos):

            # Ids del Estado inicial y el final
            procesos_ids = (self.procesos_id[-i-1], self.procesos_id[-i])

            # Variables del Estado inicial y el final
            variables_proceso_i = {
                f'P{procesos_ids[0]}': self.variables[f'P{procesos_ids[0]}'],
                f'P{procesos_ids[1]}': self.variables[f'P{procesos_ids[1]}'],
                f'V{procesos_ids[0]}': self.variables[f'V{procesos_ids[0]}'],
                f'V{procesos_ids[1]}': self.variables[f'V{procesos_ids[1]}'],
                f'T{procesos_ids[0]}': self.variables[f'T{procesos_ids[0]}'],
                f'T{procesos_ids[1]}': self.variables[f'T{procesos_ids[1]}'],
            }

            # Argumentos para la creacion del proceso
            argumentos_proceso_i = [procesos_ids, variables_proceso_i]

            # Crear instanciad de los 4 procesos
            instancia_proceso_i = self.seleccion_usuario[i](
                argumentos_proceso_i[0],
                moles=constantes['moles'],
                R=constantes['R'],
                gamma=constantes['gamma'],
                ** argumentos_proceso_i[1]
            )
            self.procesos_instanciados.append(instancia_proceso_i)

# Seccion de prueba
if __name__ == "__main__":
    # Datos conocidos para la prueba de las variables que no estan
    data = dict()
    data['P4'] = 4.13416
    data['T3'] = 275
    data['P2'] = 4.80
    data['V2'] = 6.141
    data['T1'] = 360

    procesos_seleccionados = [0, 1, 0, 1]
    constantes = {
        'moles': 1,
        'R': 0.082,
        'gamma': 2
    }
    proceos_agrupados = ProcesosAgrupados(
        procesos_seleccionados, constantes, data)

    # Mi log
    print()
    print(f"* {'Proceso 0 instanciado':-<50}{proceos_agrupados.procesos_instanciados[0]}")
    print(f"* {'Variables que estan y no estan':-<50}{proceos_agrupados.procesos_instanciados[0].variables}")
    print(f"* {'Incognitas':-<50}{proceos_agrupados.incognitas}")
