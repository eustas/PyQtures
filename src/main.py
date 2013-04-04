#!/usr/bin/python
'''
Created on Apr 13, 2012

@author: eustas
'''

import sys

from PyQt4 import QtCore
from PyQt4 import QtGui

import loader
import viewer


class MainWindow(QtGui.QWidget):

  def __init__(self):
    super(MainWindow, self).__init__()
    self.init_ui()

  def on_current_file_changed(self, current):
    self.viewer.set_path(self.file_model.filePath(current))

  def init_ui(self):
    self.file_model = QtGui.QFileSystemModel()
    self.file_selection_model = QtGui.QItemSelectionModel(self.file_model)
    self.file_model.setRootPath(QtCore.QDir.rootPath())
    self.file_tree = QtGui.QTreeView(parent=self);
    self.file_tree.setModel(self.file_model)
    self.file_tree.setSelectionModel(self.file_selection_model)
    self.file_tree.setColumnHidden(1, True)
    self.file_tree.setColumnHidden(2, True)
    self.file_tree.setColumnHidden(3, True)

    self.file_selection_model.currentChanged.connect(self.on_current_file_changed)

    self.viewer = viewer.Viewer()

    self.splitter = QtGui.QSplitter();
    self.splitter.addWidget(self.file_tree)
    self.splitter.addWidget(self.viewer)
    self.splitter.setStretchFactor(0, 0)
    self.splitter.setStretchFactor(1, 1)

    h_box = QtGui.QHBoxLayout()
    h_box.addWidget(self.splitter)
    v_box = QtGui.QVBoxLayout()
    v_box.addLayout(h_box)
    v_box.setMargin(0)
    self.setLayout(v_box)

    self.resize(800, 600)
    self.setWindowTitle('pyQtures')
    self.setWindowIcon(QtGui.QIcon('icon.png'))
    self.show()

  def keyPressEvent(self, key_event):  # Signal handler.
    key = key_event.key()
    if QtCore.Qt.Key_Escape == key:
      if self.isFullScreen():
        self.showNormal()
      else:
        QtCore.QCoreApplication.instance().quit()
    elif QtCore.Qt.Key_Return == key:
      if self.isFullScreen():
        self.showNormal()
      else:
        self.showFullScreen()


class App(QtGui.QApplication):

  def __init__(self, argv):
    super(App, self).__init__(argv)
    self.init()

  def init(self):
    self.loader = loader.Loader()
    self.main_window = MainWindow()


def main():
  sys.exit(App(sys.argv).exec_())


if __name__ == '__main__':
    main()
