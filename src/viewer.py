'''
Created on Apr 13, 2012

@author: eustas
'''

from PyQt4.QtCore import Qt

from PyQt4.QtGui import QColor
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QPainter
from PyQt4.QtGui import QPen
from PyQt4.QtGui import QStaticText
from PyQt4.QtGui import QWidget


class Viewer(QWidget):

  def __init__(self, loader):
    self._loader = loader
    self._path = None
    self._exif = None
    self._ready = False
    self._magnify = False
    self._label = QStaticText()
    self._font = QFont("Verdana", 9)
    self._font.setBold(True)
    self._pen = QPen(QColor(0x00FF00))
    super(Viewer, self).__init__()

  def paintEvent(self, unused_paint_event):  # Signal handler.
    canvas = QPainter()
    canvas.begin(self)
    self._draw_widget(canvas)
    canvas.end()

  def _draw_widget(self, canvas):
    if not self._ready:
      return

    size = self.size()

    if self._magnify:
      image_size = self._image.size()
      x = self._lens_x - size.width() / 2
      if x + size.width() > image_size.width():
        x = image_size.width() - size.width()
      if x < 0:
        x = 0
      y = self._lens_y - size.height() / 2
      if y + size.height() > image_size.height():
        y = image_size.height() - size.height()
      if y < 0:
        y = 0
      x0 = 0 if image_size.width() > size.width() else (size.width() - image_size.width()) / 2
      y0 = 0 if image_size.height() > size.height() else (size.height() - image_size.height()) / 2
      canvas.drawPixmap(x0, y0, self._image, x, y, size.width(), size.height())
    else:
      scaled_image_size = self._scaled_image.size()
      x = (size.width() - scaled_image_size.width()) / 2
      y = (size.height() - scaled_image_size.height()) / 2
      canvas.drawPixmap(x, y, self._scaled_image)

    canvas.setFont(self._font)
    canvas.setPen(self._pen)
    canvas.drawStaticText(2, 2, self._label)

  def resizeEvent(self, unused_resize_event):  # Signal handler.
    self._create_scaled_image()
    self.repaint()

  def reset_path(self):
    self._path = None
    self._reload()

  def set_path(self, path):
    self._path = path
    self._reload()

  def _reload(self):
    self._image = self._loader.load_image(self._path)
    image_size = self._image.size()
    self._ready = image_size.width() or image_size.height()
    if self._ready:
      self._label.setText("%s [%dx%d]" % (self._path, image_size.width(), image_size.height()))
    self._create_scaled_image()
    self.repaint()

  def _create_scaled_image(self):
    self._scaled_image = None
    if not self._ready:
        return

    image_size = self._image.size()
    size = self.size()
    if (image_size.width() <= size.width()) and (image_size.height() <= size.height()):
      self._scaled_image = self._image
    else:
      self._scaled_image = self._image.scaled(size.width(), size.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

  def _update_lens(self, x, y):
    size = self.size()
    image_size = self._image.size()
    scaled_image_size = self._scaled_image.size()
    draw_x = (size.width() - scaled_image_size.width()) / 2
    draw_y = (size.height() - scaled_image_size.height()) / 2
    self._lens_x = ((x - draw_x) * image_size.width()) / scaled_image_size.width()
    self._lens_y = ((y - draw_y) * image_size.height()) / scaled_image_size.height()
    self.repaint()

  def mousePressEvent(self, mouse_event):  # Signal handler.
    if not self._ready:
        return

    image_size = self._image.size()
    size = self.size()
    if (image_size.width() > size.width()) or (image_size.height() > size.height()):
      self._magnify = True
      self._update_lens(mouse_event.x(), mouse_event.y())

  def mouseReleaseEvent(self, unused_mouse_event):  # Signal handler.
    self._magnify = False
    self.repaint()

  def mouseMoveEvent(self, mouse_event):  # Signal handler.
    if not self._ready:
      return

    if self._magnify:
      self._update_lens(mouse_event.x(), mouse_event.y())
