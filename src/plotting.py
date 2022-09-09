import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
import constants

from PyQt5 import QtCore, QtWidgets


class WidgetPlot(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.canvas = MPLCanvas(self)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.canvas)

    def setCleanPlot(self):
        self.canvas.setCleanPlot()

    def updatePlot(self, x, y):
        self.canvas.updatePlot(x, y)

class MPLCanvas(FigureCanvasQTAgg):
    def __init__(self, parent):
        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        super().__init__(self.fig)

        self.setParent(parent)
        self.setFixedSize(QtCore.QSize(constants.PLOT_WIDTH + 50, constants.PLOT_HEIGHT + 50))

        # Matplotlib script
        self.setCleanPlot()

    def setCleanPlot(self):
        self.ax.cla()

        self.ax.grid(linewidth=0.5, linestyle='--')
        tickRange = np.arange(-4, 5, 1).tolist()
        self.ax.set_xlim(-4, 4)
        self.ax.set_ylim(0, 8)
        self.ax.set_xticks(tickRange)
        self.ax.set_xticks(tickRange)

        self.draw()

    def updatePlot(self, x, y):
        self.ax.plot(x, y, 'k')

        # https://stackoverflow.com/questions/7187504/set-data-and-autoscale-view-matplotlib
        self.ax.relim()
        self.ax.autoscale_view(True, True, True)
        self.draw()
