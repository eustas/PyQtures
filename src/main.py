#!/usr/bin/python
'''
Created on Apr 13, 2012

@author: eustas
'''

import sys

from PyQt4.QtCore import QCoreApplication
from PyQt4.QtCore import QDir
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QTimer

from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QFileSystemModel
from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QItemSelectionModel
from PyQt4.QtGui import QSplitter
from PyQt4.QtGui import QTreeView
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QWidget

from loader import Loader
from viewer import Viewer


class Window(QWidget):

  def __init__(self):
    super(Window, self).__init__()

    self._current_path = None

    self._file_model = QFileSystemModel()
    self._file_model.setRootPath(QDir.rootPath())

    self._file_selection_model = QItemSelectionModel(self._file_model)
    self._file_selection_model.currentChanged.connect(self._on_current_file_changed)

    self._file_tree = QTreeView(parent=self)
    self._file_tree.collapsed.connect(self._on_tree_expanded_collapsed)
    self._file_tree.expanded.connect(self._on_tree_expanded_collapsed)
    self._file_tree.setModel(self._file_model)
    self._file_tree.setSelectionModel(self._file_selection_model)
    self._file_tree.setColumnHidden(1, True)
    self._file_tree.setColumnHidden(2, True)
    self._file_tree.setColumnHidden(3, True)
    self._file_tree.header().hide()

    self._viewer = Viewer(Loader(24))

    self._splitter = QSplitter();
    self._splitter.addWidget(self._file_tree)
    self._splitter.addWidget(self._viewer)
    self._splitter.setStretchFactor(0, 0)
    self._splitter.setStretchFactor(1, 1)
    self._splitter.setCollapsible(0, False)

    self._layout = QGridLayout()
    self._layout.addWidget(self._splitter)
    self._switch_to_normal()
    self.setLayout(self._layout)

    self.resize(800, 600)
    self.setWindowTitle('pyQtures')
    self.show()

  def _switch_to_fullscreen(self):
    self._splitter.widget(0).hide()
    self._layout.setMargin(0)
    self.showFullScreen()

  def _switch_to_normal(self):
    self._splitter.widget(0).show()
    self._layout.setMargin(4)
    self.showNormal()

  def keyPressEvent(self, key_event):  # Signal handler.
    key = key_event.key()
    if self.isFullScreen():
      self._full_screen_key_handler(key)
    else:
      self._normal_key_handler(key)

  def _full_screen_key_handler(self, key):
    if Qt.Key_Escape == key:
      self._switch_to_normal()
    elif Qt.Key_Return == key:
      self._switch_to_normal()

  def _normal_key_handler(self, key):
    if Qt.Key_Escape == key:
      QCoreApplication.instance().quit()
    elif Qt.Key_Return == key:
      self._switch_to_fullscreen()

  def _on_current_file_changed(self, new_current):
    new_path = self._file_model.filePath(new_current)
    if not self._current_path == new_path:
        self._current_path = new_path
        self._viewer.set_path(new_path)

  def _on_tree_expanded_collapsed(self, unused_index):
    QTimer.singleShot(1, lambda: self._file_tree.resizeColumnToContents(0))


def _main():
  qss = '''
* {
  background-color: #000000;
  color: #FFFFFF;
  border: none;
}
QWidget:focus {
  border: 1px solid #808080;
}
QScrollBar {
  border: 1px solid #808080;
  margin: 0;
}
QScrollBar:horizontal {
  height: 12px;
}
QScrollBar::handle {
  margin: 2px;
  background: #808080;
  border-radius: 3px;
}
QScrollBar:vertical {
  width: 12px;
}
QScrollBar::add-line, QScrollBar::sub-line {
  width: 0;
  height: 0;
}
QScrollBar::add-page, QScrollBar::sub-page {
  background: none;
}
'''

  app = QApplication(sys.argv)
  app.setStyleSheet(qss)
  app.setWindowIcon(QIcon('icon.png'))

  app.window = Window()
  sys.exit(app.exec_())


if __name__ == '__main__':
    _main()
