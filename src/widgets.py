from PyQt5 import QtWidgets, QtGui

import room
import plotting
import calculations


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('UWB radar sim')

        # Create canvas for path input
        self.room = room.Room()

        # Storing all method values
        self.locMethods = calculations.LocalizationMethods()

        # Create clear button
        self.clearBtn = QtWidgets.QPushButton()
        self.clearBtn.setFixedWidth(100)
        self.clearBtn.setFixedHeight(50)
        self.clearBtn.setText('CLEAR')
        self.clearBtn.setObjectName('clearBtn')
        self.clearBtn.clicked.connect(self.clearBtnClicked)

        # Create SAVE button
        self.saveBtn = QtWidgets.QPushButton()
        self.saveBtn.setFixedWidth(100)
        self.saveBtn.setFixedHeight(50)
        self.saveBtn.setText('SAVE')
        self.saveBtn.setObjectName('saveBtn')
        self.saveBtn.clicked.connect(self.plotBtnClicked)

        # Create menu layout
        self.menuLayout = QtWidgets.QVBoxLayout()
        self.menuLayout.addWidget(self.saveBtn)
        self.menuLayout.addWidget(self.clearBtn)

        # Create layout of tab1
        layoutTab1 = QtWidgets.QHBoxLayout()
        layoutTab1.addLayout(self.menuLayout)
        layoutTab1.addWidget(self.room)
        stubWidgetTab1 = QtWidgets.QWidget()
        stubWidgetTab1.setLayout(layoutTab1)

        # Create layout of DCM
        dmLabel = QtWidgets.QLabel('Direct calculation method')
        dmLabel.setFont(QtGui.QFont("Times", weight=QtGui.QFont.Bold))
        self.dmTime = QtWidgets.QLabel(str(self.locMethods.dmTime) + 'sec')
        self.dmPlot = plotting.WidgetPlot(self)
        dmLayout = QtWidgets.QVBoxLayout()
        dmLayout.addWidget(dmLabel)
        dmLayout.addWidget(self.dmTime)
        dmLayout.addWidget(self.dmPlot)

        # Create layout of LSM
        lsmLabel = QtWidgets.QLabel('Least-squares method')
        lsmLabel.setFont(QtGui.QFont("Times", weight=QtGui.QFont.Bold))
        self.lsmTime = QtWidgets.QLabel(str(self.locMethods.lsmTime) + 'sec')
        self.lsmPlot = plotting.WidgetPlot(self)
        lsmLayout = QtWidgets.QVBoxLayout()
        lsmLayout.addWidget(lsmLabel)
        lsmLayout.addWidget(self.lsmTime)
        lsmLayout.addWidget(self.lsmPlot)

        # Create layout of TSM
        tsmLabel = QtWidgets.QLabel('Taylor series method')
        tsmLabel.setFont(QtGui.QFont("Times", weight=QtGui.QFont.Bold))
        self.tsmTime = QtWidgets.QLabel(str(self.locMethods.tsmTime) + 'sec')
        self.tsmPlot = plotting.WidgetPlot(self)
        tsmLayout = QtWidgets.QVBoxLayout()
        tsmLayout.addWidget(tsmLabel)
        tsmLayout.addWidget(self.tsmTime)
        tsmLayout.addWidget(self.tsmPlot)

        # Create layout of tab2
        layoutTab2 = QtWidgets.QHBoxLayout()
        layoutTab2.addLayout(dmLayout)
        layoutTab2.addLayout(lsmLayout)
        layoutTab2.addLayout(tsmLayout)
        stubWidgetTab2 = QtWidgets.QWidget()
        stubWidgetTab2.setLayout(layoutTab2)

        # Create tabs
        tabs = QtWidgets.QTabWidget()
        tabs.setTabPosition(QtWidgets.QTabWidget.North)
        tabs.setDocumentMode(True)
        tabs.addTab(stubWidgetTab1, 'input')
        tabs.addTab(stubWidgetTab2, 'output')

        self.setCentralWidget(tabs)

    def plotBtnClicked(self):
        self.room.distances = calculations.rawDist2Dist(self.room.posInTime)
        self.locMethods.directMethod(self.room.distances)
        self.locMethods.lsMethod(self.room.distances)
        self.locMethods.tsMethod(self.room.distances)
        self.dmPlot.updatePlot(self.locMethods.dmResult[0], self.locMethods.dmResult[1])
        self.lsmPlot.updatePlot(self.locMethods.lsmResult[0], self.locMethods.lsmResult[1])
        self.tsmPlot.updatePlot(self.locMethods.tsmResult[0], self.locMethods.tsmResult[1])
        self.dmTime.setText(str(round(self.locMethods.dmTime, 7)) + ' sec')
        self.lsmTime.setText(str(round(self.locMethods.lsmTime, 7)) + ' sec')
        self.tsmTime.setText(str(round(self.locMethods.tsmTime, 7)) + ' sec')

    def clearBtnClicked(self):
        self.clearData()
        self.dmPlot.setCleanPlot()
        self.lsmPlot.setCleanPlot()
        self.tsmPlot.setCleanPlot()
        self.room.drawEmptyRoom()
        self.dmTime.setText(str(round(self.locMethods.dmTime, 7)) + ' sec')
        self.lsmTime.setText(str(round(self.locMethods.lsmTime, 7)) + ' sec')
        self.tsmTime.setText(str(round(self.locMethods.tsmTime, 7)) + ' sec')

    def clearData(self):
        self.room.clearData()
        self.locMethods.clearData()
