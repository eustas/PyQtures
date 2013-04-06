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
from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QItemSelectionModel
from PyQt4.QtGui import QPalette
from PyQt4.QtGui import QSplitter
from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QTreeView
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QWidget

import loader
import viewer


class Window(QWidget):

  def __init__(self):
    super(Window, self).__init__()
    self.loader = loader.Loader(24)
    palette = self.palette();
    palette.setColor(QPalette.Window, Qt.black);
    self.setAutoFillBackground(True);
    self.setPalette(palette);

    self.current_path = None

    self.file_model = QFileSystemModel()
    self.file_model.setRootPath(QDir.rootPath())

    self.file_selection_model = QItemSelectionModel(self.file_model)
    self.file_selection_model.currentChanged.connect(self._on_current_file_changed)

    self.file_tree = QTreeView(parent=self)
    self.file_tree.collapsed.connect(self._on_tree_expanded_collapsed)
    self.file_tree.expanded.connect(self._on_tree_expanded_collapsed)
    self.file_tree.setModel(self.file_model)
    self.file_tree.setSelectionModel(self.file_selection_model)
    self.file_tree.setColumnHidden(1, True)
    self.file_tree.setColumnHidden(2, True)
    self.file_tree.setColumnHidden(3, True)

    self.viewer = viewer.Viewer(self.loader)

    self.splitter = QSplitter();
    self.splitter.addWidget(self.file_tree)
    self.splitter.addWidget(self.viewer)
    self.splitter.setStretchFactor(0, 0)
    self.splitter.setStretchFactor(1, 1)
    self.splitter.setCollapsible(0, False)

    self.layout = QGridLayout()
    self.layout.addWidget(self.splitter)
    self._switch_to_normal()
    self.setLayout(self.layout)

    self.resize(800, 600)
    self.setWindowTitle('pyQtures')
    self.show()

  def _switch_to_fullscreen(self):
    self.splitter.widget(0).hide()
    self.layout.setMargin(0)
    self.showFullScreen()

  def _switch_to_normal(self):
    self.splitter.widget(0).show()
    self.layout.setMargin(4)
    self.showNormal()

  def keyPressEvent(self, key_event):  # Signal handler.
    key = key_event.key()
    if Qt.Key_Escape == key:
      if self.isFullScreen():
        self._switch_to_normal()
      else:
        QCoreApplication.instance().quit()
    elif Qt.Key_Return == key:
      if self.isFullScreen():
        self._switch_to_normal()
      else:
        self._switch_to_fullscreen()

  def _on_current_file_changed(self, new_current):
    new_path = self.file_model.filePath(new_current)
    if not self.current_path == new_path:
        self.current_path = new_path
        self.viewer.set_path(new_path)

  def _on_tree_expanded_collapsed(self, unused_index):
    QTimer.singleShot(1, lambda: self.file_tree.resizeColumnToContents(0))


def _main():
  app = QApplication(sys.argv)
  app.setWindowIcon(QIcon('icon.png'))

  app.window = Window()
  sys.exit(app.exec_())


if __name__ == '__main__':
    _main()
