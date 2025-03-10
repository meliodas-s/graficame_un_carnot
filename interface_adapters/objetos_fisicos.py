import matplotlib.path as mpath
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap as lsc


class Embolo:
    """
    Clase que me permite crear un embolo dado sus medidas
    """

    def __init__(self, r, ct_cil_y, h_e, a_e, r_e, color='black') -> None:
        """
        r: radio del cilindro interior, donde va el embolo
        ct_cil_y: centro de cilindro en y
        h_e: altura del embolo, que tan grueso sera el piston
        a_e: altura del eje, que tan largo sera el eje
        r_e: radido del eje, permite definir el grosor del eje
        """
        path_data = [
            (mpath.Path.MOVETO, (-r, ct_cil_y)),
            (mpath.Path.LINETO, (r, ct_cil_y)),
            (mpath.Path.LINETO, (r, ct_cil_y + h_e)),
            (mpath.Path.LINETO, (r_e, ct_cil_y + h_e)),
            (mpath.Path.LINETO, (r_e, ct_cil_y + h_e + a_e)),
            (mpath.Path.LINETO, (-r_e, ct_cil_y + h_e + a_e)),
            (mpath.Path.LINETO, (-r_e, ct_cil_y + h_e)),
            (mpath.Path.LINETO, (-r, ct_cil_y + h_e)),
            (mpath.Path.CLOSEPOLY, (-r, ct_cil_y)),
        ]

        self.codes, self.verts = zip(*path_data)
        path = mpath.Path(self.verts, self.codes)
        self.parche = mpatches.PathPatch(path, color=color)

    def cambiar_pocision(self, mover_y) -> None:
        """
        mover_y: cuanta distancia se movera en el eje y
        """
        moved_verts = [(x, y + mover_y) for (x, y) in self.verts]
        moved_path = mpath.Path(moved_verts, self.codes)
        self.verts = moved_verts
        self.parche.set_path(moved_path)


class Gas:
    """
    Clase que crea un gas y me permite manipularlo
    """

    def __init__(self, radio, cord_y, paleta: lsc, altura) -> None:
        self.parche = {
            mpatches.Rectangle(
                (-radio, cord_y), radio*2, altura, color=paleta(0), alpha=0.6
            )
        }

    def calentar_gas(self, porcentaje):
        """
        Dado un porcentaje, incrementa el color caliente en ese porcentaje

        Parámetros:
        -----------

        porcentaje: float
            Un numero dentro de [0,1]

        Retorno:
        --------
        None
            Esta funcion no retorna valor, cambia el color del parche
        """
        self.parche.set_color(self.paleta(porcentaje))

    def enfriar_gas(self, porcentaje):
        """
        Dado un porcentaje, decrementa el color caliente en ese porcentaje

        Parámetros:
        -----------

        porcentaje: float
            Un numero dentro de [0,1]

        Retorno:
        --------
        None
            Esta funcion no retorna valor, cambia el color del parche
        """
        self.parche.set_color(self.paleta(1-porcentaje))


class Cilindro:
    """
    Objeto encargado de crear el cilidro y sus bordes.

    Atributos:
    ----------
    cilindro_int: Rectangle
        Es el parche que representa el cilindro interior

    cilindro_ext: Rectangle
        Es el parche que representa el cilindro exterior
    """

    def __init__(self, radio, cord_y, altura, grosor) -> None:
        """
        Inicializa una instancia de Cilindro.

        Parametros:
        -----------
        radio: float
            El radio interior del cilindro.

        cord_y: float
            La coordenada en y que tendra la esquina inf. izq. del cilindro.

        altura: float
            La altura que tendra el cilindro interior desde la base.

        grosor: float
            El grosor de los bordes del cilindro exterior.
        """
        # Parametros
        diam_int = radio*2
        diam_ext = radio*2 + grosor*2
        radio_ext = radio + grosor
        cord_y_ext = cord_y - grosor
        self.datos = [diam_int, diam_ext, radio_ext, cord_y_ext]

        # Cilindros
        self.cilindro_int = {
            mpatches.Rectangle(
                (-radio, cord_y), diam_int, altura, color='gray')}
        self.cilindro_ext = {
            mpatches.Rectangle(
                (-radio_ext, cord_y_ext), diam_ext, altura+grosor, color='b')}

    def datos(self) -> dict:
        """
        Devuelve los datos necesarios para crear un cilindro.

        Returns:
        --------
        dict
            Diccionario con los datos para poder crear barras.
        """
        datos = self.datos
        datos_r = {
            'd_int': datos[0], 'd_ext': datos[1],
            'r_ext': datos[2], 'cord_y_ext': datos[3]}
        return datos_r


class Barra:
    """
    Objeto encargado de crear mis barras que son mis fuentes de calor o frio.

    Atributos:
    ----------
    temperatura : float
        Temperatura a la que se encuentra mi fuente.

    cord_x : float
        Coordenada en el eje x de la esq. inf. izquierda.

    cord_y : float
        Coordenada en el eje y de el esq. inf. izquierda.

    parche : Rectangle
        Patch que representa mi barra o fuente de energia.
    """

    def __init__(self, temperatura, cord_x, cord_y, altura, diam_ext) -> None:
        self.temperatura = temperatura
        self.cord_x = cord_x
        self.cord_y = cord_y
        # self.
        self.parche = mpatches.Rectangle(
            (cord_x, cord_y), diam_ext, altura, color='r')


class Particula:
    """
    Objeto encargado de crear una particula la cual se movera por un x camino.

    Atributos
    ---------
    cord_x : float
        Coordeanada en x actual.

    cord_y : float
        Coordenada en y actual.
    """

    def __init__(self, cord_x, cord_y) -> None:
        self.cord_x = cord_x
        self.cord_y = cord_y

    def desplazarse(self):
        """
        Dada una funcion y una cantidad, se desplaza la particula.
        """


# # Figuras
# dmtr = r * 2                                    # Diametro.
# ct_cil_y = -alturas['h_2']/2                    # Centro cilindro en y.
# bd_cil_e = 0.05                                 # Borde cilindro exterio.
# long_cil_e = dmtr+2*bd_cil_e                    # Long cilindro exterior.
# mrgn_cil = 1                                    # Espacio sin gas.
# altu_bar = 0.5                                  # Altura barras de tmemp.
# h_e = 0.1                                       # Altura del embolo.
# r_e = 0.1                                       # Radio de eje.
# a_e = 0.3                                       # Altura de eje.
# y_all = ct_cil_y - bd_cil_e - altu_bar          # Cord en y para barrs.
# x_h = -r-bd_cil_e                               # Cord en x para barra h.
# x_a = x_h + long_cil_e                          # Cord en x para barra a.
# x_l = x_a + long_cil_e                          # Cord en x para barra l.
# cilindro_int = mpatches.Rectangle(
#     (-r, ct_cil_y), dmtr, alturas['h_2'] + mrgn_cil, color='gray')
# cilindro_ext = mpatches.Rectangle(
#     (-r-bd_cil_e, ct_cil_y-bd_cil_e), long_cil_e, alturas['h_2']+bd_cil_e + mrgn_cil, color='b')
# bara_h = mpatches.Rectangle((x_h, y_all), long_cil_e, altu_bar, color='r')
# bara_adi = mpatches.Rectangle((x_a, y_all), long_cil_e, altu_bar, color='b')
# bara_l = mpatches.Rectangle(
#     (x_l, y_all), long_cil_e, altu_bar, color='lightblue')
# gas = mpatches.Rectangle((-r, ct_cil_y), dmtr,
#                          alturas['h_1'], color=color_h, alpha=0.6)
