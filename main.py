import Original.solucion_grafica as solucion_grafica

# Entitites
from entities.procesos import Proceso, ProcesoAdiabatio, ProcesoIsobarico
from entities.procesos import ProcesoIsotermico, ProcesoIsocorico
from entities.procesos import ProcesosAgrupados

# Use case
from use_cases.soluciones import Solutions

# Interface Adapters
from interface_adapters.animador import AnimatorGraf, AnimatorEmbo
from interface_adapters.animador import MultiAnimator, Plotter
from interface_adapters.objetos_fisicos import Particula

# [Isotermico, Adiabatico, Isocorico, Isobarico]
tipos_procesos = [0, 1, 2, 3]


def main():
    # Condiciones iniciales del sistema
    procesos = [tipos_procesos[0], tipos_procesos[1],
                tipos_procesos[0], tipos_procesos[1]]

    # Constantes
    constantes = dict()
    constantes['R'] = 0.082
    constantes['gamma'] = 2
    constantes['moles'] = 2
    r = 1

    # Datos de entrada
    data = dict()
    data['P4'] = 4.13416
    data['T3'] = 275
    data['P2'] = 4.80
    data['V2'] = 6.141
    data['T1'] = 360


    # Procesos
    procesos_agrupados = ProcesosAgrupados(procesos, constantes, data)
    solutions = Solutions(procesos_agrupados)
    print(solutions.solucion)



    # Clausurado de momento
    # # Soluciones
    # data, cords = solucion_grafica.solucion(data)
    # halturas = solucion_grafica.solucion_h(r, data['V_1'], data['V_2'])

    # # Proceso 1-2
    # not_animate_data = solucion_grafica.graficar_isotermica(
    #     data['T_1'], data['V_1'], data['V_2'], 50)
    # for_animate_data = list(zip(not_animate_data['X'], not_animate_data['Y']))

    # # visualizar resultados
    # particula = Particula(data['V_1'], data['P_1'])
    # multi_animator = MultiAnimator()
    # plots_statics = Plotter(multi_animator.ax_graf, [
    #                         [not_animate_data['X'], not_animate_data['Y']]])
    # multi_animator.run(for_animate_data, for_animate_data)


if __name__ == "__main__":
    main()
