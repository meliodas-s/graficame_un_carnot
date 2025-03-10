import numpy as np
import sympy as sp


class Solutions:
    def __init__(self, procesos_agrupados) -> None:
        self.procesos_agrupados = procesos_agrupados

        # Constantes
        gamma = 2
        n = 1
        R = 0.082

        # Todas las ecuaciones del sistema de ecuaciones
        self.ecuaciones = list()
        for proceso in self.procesos_agrupados.procesos_instanciados:
            self.ecuaciones.append(proceso.ecuacion_proceso)
            self.ecuaciones.append(proceso.ecuacion_gas_inicial)
        print(tuple(self.ecuaciones))
        print(procesos_agrupados.incognitas)
        

        # Resolviendo sistema con sympy
        self.solucion = sp.nsolve(
            tuple(self.ecuaciones),
            self.procesos_agrupados.incognitas,
            [5]*7,
            verify=False,
            dict=True
        )

        # Intersecciones
        # for item in solucion[0].items():
        #     data[f'{item[0]}'] = float(item[1])

        # # Grafica de puntos
        # v_cords = list()
        # p_cords = list()
        # t_cords = list()
        # for i in range(1, 5):
        #     v_cords.append(data[f'V_{i}'])
        #     p_cords.append(data[f'P_{i}'])
        #     t_cords.append(f'{i}')

        # return data, dict(v_cords=v_cords, p_cords=p_cords, t_cords=t_cords)


def graficar_adiabatica(pres: float, v_ini: float, v_fin: float, cant_putos: int):
    """
    Toma los datos necesario para graficar una funcion adiabatica y
    devuelve un diccionario con los valores para matploltib.

    Parameters:
        temp (float): Temperatura en el estado.
        v_fin (float): Volumen final.
        v_ini (float): Volumen inicial.
        cant_puntos (int): Cantidad de puntos a graficar.

    Returns:
        dict: El diccionario con parametros para matplotlib.
    """
    gamma = 2
    n = 1
    R = 0.082

    v = np.linspace(v_ini, v_fin, cant_putos)
    p = pres*v_ini**gamma/(v**gamma)
    return {'X': v, 'Y': p, 'args': {'color': 'black', 'label': 'Adiabatica'}}


def graficar_isotermica(temp: float, v_ini: float, v_fin: float, cant_putos: int):
    """
    Toma los datos necesario para graficar una funcion isotermica y
    devuelve un diccionario con los valores para matploltib.

    Parameters:
        temp (float): Temperatura en el estado.
        v_fin (float): Volumen final.
        v_ini (float): Volumen inicial.
        cant_puntos (int): Cantidad de puntos a graficar.

    Returns:
        dict: El diccionario con parametros para matplotlib.
    """
    gamma = 2
    n = 1
    R = 0.082

    v = np.linspace(v_fin, v_ini, cant_putos)
    p = n*R*temp/v

    return {'X': v, 'Y': p, 'args': {'color': 'black', 'label': 'Isotermica'}}


def solucion_h(r: float, v1: float, v2: float):
    h1, h2 = sp.symbols('h_1 h_2')
    r = 1

    # Soluciones
    sol = sp.solve(
        [
            sp.pi*r**2*h1-v1,
            sp.pi*r**2*h2-v2
        ],
        [
            h1,
            h2
        ],
    )
    sol = [h for h in sol.values()]

    return {'h_1': sol[0], 'h_2': sol[1]}
