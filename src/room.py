import numpy as np

import constants
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt


class RoomCanvas(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()

        # Data
        self.nOfReceivers = 4

        # Drawing setup
        pixmap = QtGui.QPixmap(constants.CANVAS_WIDTH, constants.CANVAS_HEIGHT)
        self.setPixmap(pixmap)
        self.setFixedSize(QtCore.QSize(constants.CANVAS_WIDTH, constants.CANVAS_HEIGHT))
        self.drawEmptyRoom()
        self.lastX, self.lastY = None, None
        self.penColor = QtGui.QColor('black')

    def drawBackgroud(self):
        """Draws a white rectangle across the whole canvas"""
        painter = QtGui.QPainter(self.pixmap())
        penWhite = QtGui.QPen()
        penWhite.setWidth(2)
        penWhite.setColor(QtGui.QColor('white'))
        painter.setPen(penWhite)
        painter.setBrush(QtGui.QBrush(Qt.white, Qt.SolidPattern))
        painter.drawRect(0, 0, constants.CANVAS_WIDTH, constants.CANVAS_HEIGHT)
        painter.end()

    def drawRoom(self):
        """Draws a black rectangle"""
        painter = QtGui.QPainter(self.pixmap())
        penBlack = QtGui.QPen()
        penBlack.setWidth(2)
        penBlack.setColor(QtGui.QColor('black'))
        painter.setPen(penBlack)
        painter.drawRect(constants.ROOM_OFFSET, constants.ROOM_OFFSET,
                         constants.CANVAS_WIDTH - constants.ROOM_OFFSET * 2,
                         constants.CANVAS_HEIGHT - constants.ROOM_OFFSET * 2)
        painter.end()

    def drawRadars(self):
        """Draws points representing the positions of radars"""
        self.drawTransmitter()
        self.drawReceivers(self.nOfReceivers)
        self.update()

    def drawTransmitter(self):
        """Draws a red point"""
        painter = QtGui.QPainter(self.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(10)
        pen.setColor(QtGui.QColor('red'))
        painter.setPen(pen)
        painter.drawPoint(constants.TX_X_POS_CANVAS, constants.TX_Y_POS_CANVAS)
        painter.end()

    def drawReceivers(self, n):
        """Draws 2 or 4 blue points"""
        painter = QtGui.QPainter(self.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(10)
        pen.setColor(QtGui.QColor('blue'))
        painter.setPen(pen)

        if n >= 2:
            painter.drawPoint(constants.RX1_X_POS_CANVAS, constants.RX1_Y_POS_CANVAS)
            painter.drawPoint(constants.RX2_X_POS_CANVAS, constants.RX2_Y_POS_CANVAS)

        if n == 4:
            painter.drawPoint(constants.RX3_X_POS_CANVAS, constants.RX3_Y_POS_CANVAS)
            painter.drawPoint(constants.RX4_X_POS_CANVAS, constants.RX4_Y_POS_CANVAS)

        painter.end()

    def drawGrid(self):
        painter = QtGui.QPainter(self.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(1)
        pen.setStyle(Qt.DotLine)
        pen.setColor(QtGui.QColor(constants.GRID_COLOR))
        painter.setPen(pen)

        for i in range(1, 9):
            painter.drawLine(constants.WALL_WEST_X, i * 50 + constants.ROOM_OFFSET,
                             constants.WALL_EAST_X, i * 50 + constants.ROOM_OFFSET)
            painter.drawLine(i * 50 + constants.ROOM_OFFSET, constants.WALL_NORTH_Y,
                             i * 50 + constants.ROOM_OFFSET, constants.WALL_SOUTH_Y)

        painter.end()

    def drawEmptyRoom(self):
        self.drawBackgroud()
        self.drawRoom()
        self.drawGrid()
        self.drawRadars()
        self.update()

    def mouseMoveEvent(self, e):
        if constants.ROOM_OFFSET < e.x() <= constants.CANVAS_WIDTH - constants.ROOM_OFFSET:
            if constants.ROOM_OFFSET < e.y() <= constants.CANVAS_HEIGHT - constants.ROOM_OFFSET:

                if self.lastX is None:
                    self.lastX = e.x()
                    self.lastY = e.y()
                    return

                painter = QtGui.QPainter(self.pixmap())
                p = painter.pen()
                p.setWidth(2)
                p.setColor(self.penColor)
                painter.setPen(p)
                painter.drawLine(self.lastX, self.lastY, e.x(), e.y())
                painter.end()

                self.update()
                self.lastX = e.x()
                self.lastY = e.y()

        e.ignore()

    def mouseReleaseEvent(self, e):
        # Catch the end of the movement
        self.lastX = None
        self.lastY = None
        e.ignore()


class Room(RoomCanvas):
    def __init__(self):
        super(Room, self).__init__()

        self.posHistory = [[], []]
        self.posInTime = [[], []]
        self.distances = None

        # Timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerTicked)
        self.tickCounter = 0

    def clearData(self):
        self.posHistory[0].clear()
        self.posHistory[1].clear()
        self.posInTime[0].clear()
        self.posInTime[1].clear()
        np.delete(self.distances, np.s_[::])
        self.tickCounter = 0

        # Start of a new tick
    def timerTicked(self):
        self.tickCounter += 1

        # Debug
        if not self.posHistory[0]:
            print('POS_HISTORY[0] EMPTY')
        if not self.posHistory[1]:
            print('POS_HISTORY[1] EMPTY')

        # Add target position at the current tick
        self.posInTime[0].append(self.posHistory[0][-1])
        self.posInTime[1].append(self.posHistory[1][-1])

    @staticmethod
    def transformCanvasPosToRoomPos(x, y) -> tuple:
        transformedX = (x - 10 - 200) / 50
        transformedY = abs(y - 10 - 400) / 50
        return transformedX, transformedY

    def mouseMoveEvent(self, e):
        super(Room, self).mouseMoveEvent(e)
        if constants.ROOM_OFFSET < e.x() <= constants.CANVAS_WIDTH - constants.ROOM_OFFSET:
            if constants.ROOM_OFFSET < e.y() <= constants.CANVAS_HEIGHT - constants.ROOM_OFFSET:
                transformedX, transformedY = self.transformCanvasPosToRoomPos(e.x(), e.y())
                self.posHistory[0].append(transformedX)
                self.posHistory[1].append(transformedY)

    def mousePressEvent(self, e):
        # Catch the start of movement
        super(Room, self).mousePressEvent(e)
        if constants.ROOM_OFFSET < e.x() <= constants.CANVAS_WIDTH - constants.ROOM_OFFSET:
            if constants.ROOM_OFFSET < e.y() <= constants.CANVAS_HEIGHT - constants.ROOM_OFFSET:
                transformedX, transformedY = self.transformCanvasPosToRoomPos(e.x(), e.y())
                self.posHistory[0].append(transformedX)
                self.posHistory[1].append(transformedY)

                self.timer.start(constants.TICKRATE)

    def mouseReleaseEvent(self, e):
        # Catch the end of the movement
        super(Room, self).mouseReleaseEvent(e)
        if constants.ROOM_OFFSET < e.x() <= constants.CANVAS_WIDTH - constants.ROOM_OFFSET:
            if constants.ROOM_OFFSET < e.y() <= constants.CANVAS_HEIGHT - constants.ROOM_OFFSET:
                transformedX, transformedY = self.transformCanvasPosToRoomPos(e.x(), e.y())
                self.posHistory[0].append(transformedX)
                self.posHistory[1].append(transformedY)

        self.timer.stop()
