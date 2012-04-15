'''
Created on Apr 13, 2012

@author: eustas
'''

import sys

from PyQt4 import QtCore
from PyQt4 import QtGui

from ImageLoader import ImageLoader

class MainWindow(QtGui.QWidget):

  def __init__(self):
    super(MainWindow, self).__init__()
    self.initUI()

  def initUI(self):
    self.picViewer = PicViewer()

    hbox = QtGui.QHBoxLayout()
    hbox.addWidget(self.picViewer)
    vbox = QtGui.QVBoxLayout()
    vbox.addLayout(hbox)
    vbox.setMargin(0)
    self.setLayout(vbox)

    self.setGeometry(300, 300, 250, 150)
    self.setWindowTitle('pyQtures')
    self.setWindowIcon(QtGui.QIcon('favico.png'))
    self.show()

  def keyPressEvent(self, keyEvent):
    key = keyEvent.key()
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

class PyQtures(QtGui.QApplication):

  def __init__(self, argv):
    super(PyQtures, self).__init__(argv)
    self.initApp()

  def initApp(self):
    self.imageLoader = ImageLoader()
    self.mainWindow = MainWindow()

def main():
  sys.exit(PyQtures(sys.argv).exec_())

if __name__ == '__main__':
    main()
