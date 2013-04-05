#!/usr/bin/python
'''
Created on Apr 13, 2012

@author: eustas
'''

import sys

from PyQt4.QtCore import QCoreApplication
from PyQt4.QtCore import QDir
from PyQt4.QtCore import Qt

from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QFileSystemModel
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QItemSelectionModel
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QSplitter
from PyQt4.QtGui import QTreeView
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QWidget

import loader
import viewer


class MainWindow(QWidget):

  def __init__(self):
    super(MainWindow, self).__init__()
    self.init_ui()

  def on_current_file_changed(self, current):
    self.viewer.set_path(self.file_model.filePath(current))

  def init_ui(self):
    self.file_model = QFileSystemModel()
    self.file_selection_model = QItemSelectionModel(self.file_model)
    self.file_model.setRootPath(QDir.rootPath())
    self.file_tree = QTreeView(parent=self);
    self.file_tree.setModel(self.file_model)
    self.file_tree.setSelectionModel(self.file_selection_model)
    self.file_tree.setColumnHidden(1, True)
    self.file_tree.setColumnHidden(2, True)
    self.file_tree.setColumnHidden(3, True)

    self.file_selection_model.currentChanged.connect(self.on_current_file_changed)

    self.viewer = viewer.Viewer()

    self.splitter = QSplitter();
    self.splitter.addWidget(self.file_tree)
    self.splitter.addWidget(self.viewer)
    self.splitter.setStretchFactor(0, 0)
    self.splitter.setStretchFactor(1, 1)

    h_box = QHBoxLayout()
    h_box.addWidget(self.splitter)
    v_box = QVBoxLayout()
    v_box.addLayout(h_box)
    v_box.setMargin(0)
    self.setLayout(v_box)

    self.resize(800, 600)
    self.setWindowTitle('pyQtures')
    self.setWindowIcon(QIcon('icon.png'))
    self.show()

  def keyPressEvent(self, key_event):  # Signal handler.
    key = key_event.key()
    if Qt.Key_Escape == key:
      if self.isFullScreen():
        self.showNormal()
      else:
        QCoreApplication.instance().quit()
    elif Qt.Key_Return == key:
      if self.isFullScreen():
        self.showNormal()
      else:
        self.showFullScreen()


class App(QApplication):

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
