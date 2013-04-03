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

  def init_ui(self):
    self.viewer = viewer.Viewer()

    h_box = QtGui.QHBoxLayout()
    h_box.addWidget(self.viewer)
    v_box = QtGui.QVBoxLayout()
    v_box.addLayout(h_box)
    v_box.setMargin(0)
    self.setLayout(v_box)

    self.setGeometry(300, 300, 250, 150)
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
