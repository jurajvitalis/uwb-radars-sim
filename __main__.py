import sys

from PyQt5.QtWidgets import QDesktopWidget, QApplication

import widgets
from PyQt5 import QtWidgets


def topleft():
    frameGm = window.frameGeometry()
    topLeftPoint = QApplication.desktop().availableGeometry().topLeft()
    frameGm.moveTopLeft(topLeftPoint)
    window.move(frameGm.topLeft())


if __name__ == "__main__":

    # Create application
    app = QtWidgets.QApplication(sys.argv)

    # Create main window
    window = widgets.MainWindow()
    topleft()
    window.show()

    # Start event loop
    app.exec()
