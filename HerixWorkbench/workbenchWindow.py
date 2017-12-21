#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""
# ---------------------------------------------------------------------------------------------------------------------#
from __future__ import unicode_literals

import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from spec2nexus.spec import SpecDataFile
from specguiutils.scanbrowser import ScanBrowser
from specguiutils.scantypeselector import ScanTypeSelector, SCAN_TYPES



class HerixWorkbenchWindow(QMainWindow):
    """Main window class"""
    def __init__(self, parent=None):
        super(HerixWorkbenchWindow, self).__init__(parent)
        self.setGeometry(50, 50, 1500, 800)
        self.setWindowTitle("Herix Workbench")
        self.setMinimumSize(1000, 650)
        self.windowSplitter = QSplitter()

        self.CreateSpecDataSplitter()
        self.createMenuBar()
        self.windowSplitter.addWidget(self.specSplitter)
        self.setCentralWidget(self.windowSplitter)

    def CreateSpecDataSplitter(self):
        self.specSplitter = QSplitter()
        self.specSplitter.setOrientation(Qt.Vertical)
        self.specSplitter.setFixedWidth(300)

        self.scanBrowser = ScanBrowser()
        self.scanTypeSelector = ScanTypeSelector()

        self.specSplitter.addWidget(self.scanTypeSelector)
        self.specSplitter.addWidget(self.scanBrowser)

    def createMenuBar(self):
        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)
        fileMenu = menuBar.addMenu("File")

        openAction = QAction("Open", self)
        openAction.triggered.connect(self.openSpecFile)

        exitAction = QAction("Exit", self)
        exitAction.triggered.connect(self.close)

        fileMenu.addAction(openAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

    @pyqtSlot()
    def openSpecFile(self):
        fileName, specFilterName = QFileDialog.getOpenFileName(self, "Open spec file", None, "*.spec")
        self.specFile = None

        if fileName != "":
            try:
                self.specFile = SpecDataFile(fileName)
                self.scans = self.specFile.scans
                self.loadScans()
            except Exception as ex:
                QMessageBox.warning(self, "Loading error",
                                    "There was an error loading the spec file. \n\nException: " + str(ex))

    def loadScans(self):
        self.scanBrowser.loadScans(self.scans)
        scanTypes = self.getScanTypes()
        self.scanTypeSelector.loadScans(scanTypes)
        self.scanTypeSelector.scanTypeChanged.connect(self.filterScansByType)

    def getScanTypes(self):
        scanTypes = set()
        for scan in self.scans:
            scanTypes.add(self.specFile.scans[scan].scanCmd.split()[0])
        scanTypes = list(scanTypes)
        print(scanTypes)
        scanTypes.sort(key=str.lower)
        print(scanTypes)
        return scanTypes

    def filterScansByType(self):
        if self.scanTypeSelector.getCurrentType() == 'All':
            self.loadAllScans()
        else:
            self.scanBrowser.filterByScanTypes(self.scans, self.scanTypeSelector.getCurrentType())

    def loadAllScans(self):
        self.scanBrowser.loadScans(self.scans)


def main():
    """Main method.
    """
    app = QApplication(sys.argv)
    herixWindow = HerixWorkbenchWindow()
    herixWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()