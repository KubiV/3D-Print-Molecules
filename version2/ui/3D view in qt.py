import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        self.canvas = FigureCanvas(plt.Figure())
        layout.addWidget(self.canvas)

        self.add_3d_plot()

    def add_3d_plot(self):
        fig = self.canvas.figure
        ax = fig.add_subplot(111, projection='3d')

        # Replace the following lines with your 3D data
        x = np.random.rand(10)
        y = np.random.rand(10)
        z = np.random.rand(10)

        ax.grid(False)
        ax.set_axis_off()

        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.scatter(x, y, z)

        self.canvas.draw()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()