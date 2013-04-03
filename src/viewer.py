'''
Created on Apr 13, 2012

@author: eustas
'''

from PyQt4 import QtCore
from PyQt4 import QtGui


class Viewer(QtGui.QWidget):

  def __init__(self):
    super(Viewer, self).__init__()
    self.init_ui()

  def init_ui(self):
    self.magnify = False

  def paintEvent(self, unused_paint_event):  # Signal handler.
    canvas = QtGui.QPainter()
    canvas.begin(self)
    self.draw_widget(canvas)
    canvas.end()

  def draw_widget(self, canvas):
    size = self.size()
    if self.magnify:
      original_size = self.original_image.size()
      x = self.lens_x - size.width() / 2
      if x + size.width() > original_size.width():
        x = original_size.width() - size.width()
      if x < 0:
        x = 0
      y = self.lens_y - size.height() / 2
      if y + size.height() > original_size.height():
        y = original_size.height() - size.height()
      if y < 0:
        y = 0
      x0 = 0 if original_size.width() > size.width() else (size.width() - original_size.width()) / 2
      y0 = 0 if original_size.height() > size.height() else (size.height() - original_size.height()) / 2
      canvas.drawPixmap(x0, y0, self.original_image, x, y, size.width(), size.height())
    else:
      image_size = self.image.size()
      x = (size.width() - image_size.width()) / 2
      y = (size.height() - image_size.height()) / 2
      canvas.drawPixmap(x, y, self.image)

  def resizeEvent(self, unused_resize_event):  # Signal handler.
    path = 'test.jpg'
    self.original_image = QtGui.QApplication.instance().loader.load_image(path)

    size = self.size()
    original_size = self.original_image.size()
    if (original_size.width() <= size.width()) and (original_size.height() <= size.height()):
        self.image = self.original_image
    else:
        self.image = self.original_image.scaled(size.width(), size.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

  def update_lens(self, x, y):
    size = self.size()
    original_size = self.original_image.size()
    image_size = self.image.size()
    draw_x = (size.width() - image_size.width()) / 2
    draw_y = (size.height() - image_size.height()) / 2
    self.lens_x = ((x - draw_x) * original_size.width()) / image_size.width()
    self.lens_y = ((y - draw_y) * original_size.height()) / image_size.height()
    self.repaint()

  def mousePressEvent(self, mouse_event):  # Signal handler.
    original_size = self.original_image.size()
    size = self.size()
    if (original_size.width() > size.width()) or (original_size.height() > size.height()):
        self.magnify = True
    self.update_lens(mouse_event.x(), mouse_event.y())

  def mouseReleaseEvent(self, unused_mouse_event):  # Signal handler.
    self.magnify = False
    self.repaint()

  def mouseMoveEvent(self, mouse_event):  # Signal handler.
    self.update_lens(mouse_event.x(), mouse_event.y())
