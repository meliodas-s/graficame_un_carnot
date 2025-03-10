import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class MultiAnimator:
    def __init__(self) -> None:

        self.fig, (self.ax_graf, self.ax_embo) = plt.subplots(
            1, 2, figsize=(12, 6))
        self.animator_graf = AnimatorGraf(self.ax_graf)
        self.animator_embo = AnimatorEmbo(self.ax_embo)
        print(type(self.ax_embo))
        pass

    def run(self, data_graf, data_embo):
        ani_graf = FuncAnimation(
            self.fig, self.animator_graf.animate, frames=len(data_graf),
            init_func=self.animator_graf.init_animate, fargs=(data_graf,),
            blit=True, repeat=False
        )
        ani_embo = FuncAnimation(
            self.fig, self.animator_embo.animate, frames=len(data_embo),
            init_func=self.animator_embo.init_animate, fargs=(data_embo,),
            blit=True, repeat=False
        )
        plt.show()


class AnimatorGraf:
    def __init__(self, ax) -> None:
        self.ax = ax
        self.line, = self.ax.plot([], [], 'o', lw=0.1)

    def init_animate(self):
        self.ax.set_xlim(0, 20)
        self.ax.set_ylim(0, 20)
        self.line.set_data([], [])
        return self.line,

    def animate(self, frame, data):
        x = [point[0] for point in data[:frame]]
        y = [point[1] for point in data[:frame]]
        self.line.set_data(x, y)
        return self.line,


class AnimatorEmbo:
    def __init__(self, ax) -> None:
        self.ax = ax
        self.line, = self.ax.plot([], [], 'o', lw=0.1)

    def init_animate(self):
        self.ax.set_xlim(0, 20)
        self.ax.set_ylim(0, 20)
        self.line.set_data([], [])
        return self.line,

    def animate(self, frame, data):
        x = [point[0] for point in data[:frame]]
        y = [point[1] for point in data[:frame]]
        self.line.set_data(x, y)
        return self.line,


class Plotter():
    def __init__(self, ax, data:list[list]) -> None:
        self.procesos = list()
        print(data)
        proceso = ax.plot(data[0][0], data[0][1])
        self.procesos.append(proceso)