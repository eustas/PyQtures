#!/usr/bin/python
'''
Created on Apr 13, 2012

@author: eustas
'''

import sys

from PyQt4.QtCore import QCoreApplication
from PyQt4.QtCore import QDir
from PyQt4.QtCore import QFileInfo
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QEvent
from PyQt4.QtCore import QTimer

from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QFileSystemModel
from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QItemSelectionModel
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QSplitter
from PyQt4.QtGui import QTreeView
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QWidget

from loader import Loader
from viewer import Viewer


class Window(QMainWindow):

  def __init__(self):
    super(Window, self).__init__()

    central_widget = QWidget()

    self._current_path = None
    self._use_suffix = False

    self._file_model = QFileSystemModel()
    self._file_model.setNameFilters(['*.jpg', '*.png'])
    self._file_model.setNameFilterDisables(False)
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
    central_widget.setLayout(self._layout)

    self._file_tree.installEventFilter(self);

    self.resize(800, 600)
    self.setWindowTitle('pyQtures')
    self.setCentralWidget(central_widget)
    self.show()

  def eventFilter(self, widget, event):
    if event.type() == QEvent.KeyPress:
      if event.key() == Qt.Key_Tab:
        self._toggle_path_suffix()
        return True
    return QMainWindow.eventFilter(self, widget, event)

  def _toggle_path_suffix(self):
    self._use_suffix = not self._use_suffix
    self._update_path()

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
    elif Qt.Key_Up == key:
      self._go_to_sibling_image(-1)
    elif Qt.Key_Down == key:
      self._go_to_sibling_image(1)
    elif Qt.Key_Tab == key:
      self._toggle_path_suffix()

  def _go_to_sibling_image(self, offset):
    current = self._file_selection_model.currentIndex()
    nxt = current.sibling(current.row() + offset, current.column())
    if (nxt.parent() != current.parent()):
      return
    # TODO(eustas): Iterate through dirs?
    self._file_selection_model.setCurrentIndex(nxt, QItemSelectionModel.SelectCurrent)

  def _normal_key_handler(self, key):
    if Qt.Key_Escape == key:
      QCoreApplication.instance().quit()
    elif Qt.Key_Return == key:
      self._switch_to_fullscreen()

  def _on_current_file_changed(self, new_current):
    new_path = self._file_model.filePath(new_current)
    if not self._current_path == new_path:
        self._current_path = new_path
        self._update_path()

  def _update_path(self):
    if not self._use_suffix:
      self._viewer.set_path(self._current_path)
      return

    self._viewer.reset_path()
    if not self._current_path:
      return

    selected_file = QFileInfo(self._current_path)
    if not selected_file.exists():
      return

    selected_dir = selected_file.absoluteDir()
    file_name = selected_file.fileName()
    if not selected_dir.exists():
      return

    if not selected_dir.cd('converted'):
      return

    suffixed_path = selected_dir.absoluteFilePath(file_name)
    self._viewer.set_path(suffixed_path)

  def _on_tree_expanded_collapsed(self, unused_index):
    QTimer.singleShot(1, lambda: self._file_tree.resizeColumnToContents(0))


class Application(QApplication):

  def __init__(self):
    super(Application, self).__init__(sys.argv)
    self.setStyleSheet('''
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
''')
    self.setWindowIcon(QIcon('icon.png'))
    self.window = Window()


def _main():
  sys.exit(Application().exec_())


if __name__ == '__main__':
    _main()
