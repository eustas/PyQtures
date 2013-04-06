'''
Created on Apr 13, 2012

@author: eustas
'''

from PyQt4.QtCore import Qt

from PyQt4.QtGui import QPainter
from PyQt4.QtGui import QWidget


class Viewer(QWidget):

  def __init__(self, loader):
    self.loader = loader
    self.path = None
    self.ready = False
    self.magnify = False
    super(Viewer, self).__init__()

  def paintEvent(self, unused_paint_event):  # Signal handler.
    canvas = QPainter()
    canvas.begin(self)
    self.draw_widget(canvas)
    canvas.end()

  def draw_widget(self, canvas):
    if not self.ready:
      return

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
    self.reload()

  def set_path(self, path):
    self.path = path
    self.reload()

  def reload(self):
    self.original_image = self.loader.load_image(self.path)

    size = self.size()
    original_size = self.original_image.size()

    if not original_size.width() or not original_size.height():
      self.ready = False
    else:
      self.ready = True
      if (original_size.width() <= size.width()) and (original_size.height() <= size.height()):
          self.image = self.original_image
      else:
          self.image = self.original_image.scaled(size.width(), size.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

    self.repaint()

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
    if not self.ready:
        return

    original_size = self.original_image.size()
    size = self.size()
    if (original_size.width() > size.width()) or (original_size.height() > size.height()):
      self.magnify = True
      self.update_lens(mouse_event.x(), mouse_event.y())

  def mouseReleaseEvent(self, unused_mouse_event):  # Signal handler.
    self.magnify = False
    self.repaint()

  def mouseMoveEvent(self, mouse_event):  # Signal handler.
    if not self.ready:
      return

    if self.magnify:
      self.update_lens(mouse_event.x(), mouse_event.y())
