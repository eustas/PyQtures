'''
Created on Apr 13, 2012

@author: eustas
'''

from PyQt4 import QtGui

class PicViewer(QtGui.QWidget):

  def __init__(self):
    super(PicViewer, self).__init__()
    self.initUI()

  def initUI(self):
    self.magnify = False

  def paintEvent(self, e):
    qp = QtGui.QPainter()
    qp.begin(self)
    self.drawWidget(qp)
    qp.end()

  def drawWidget(self, qp):
    size = self.size()
    if self.magnify:
      originalSize = self.originalImage.size()
      x = self.eyeX - size.width() / 2
      if x + size.width() > originalSize.width():
        x = originalSize.width() - size.width()
      if x < 0:
        x = 0
      y = self.eyeY - size.height() / 2
      if y + size.height() > originalSize.height():
        y = originalSize.height() - size.height()
      if y < 0:
        y = 0
      x0 = 0 if originalSize.width() > size.width() else (size.width() - originalSize.width()) / 2
      y0 = 0 if originalSize.height() > size.height() else (size.height() - originalSize.height()) / 2
      qp.drawPixmap(x0, y0, self.originalImage, x, y, size.width(), size.height())
    else:
      imgSize = self.image.size()
      x = (size.width() - imgSize.width()) / 2
      y = (size.height() - imgSize.height()) / 2
      qp.drawPixmap(x, y, self.image)

  def resizeEvent(self, resizeEvent):
    size = self.size()
    w = size.width()
    h = size.height()
    path = 'test.jpg'
    self.originalImage = QtGui.QApplication.instance().imageLoader.getImage(path)
    self.image = QtGui.QApplication.instance().imageLoader.getScaledImage(path, w, h)

  def updateLens(self, mouseEvent):
    size = self.size()
    originalSize = self.originalImage.size()
    imgSize = self.image.size()
    drawX = (size.width() - imgSize.width()) / 2
    drawY = (size.height() - imgSize.height()) / 2
    x = mouseEvent.x()
    y = mouseEvent.y()
    self.eyeX = ((x - drawX) * originalSize.width()) / imgSize.width()
    self.eyeY = ((y - drawY) * originalSize.height()) / imgSize.height()
    self.repaint()

  def mousePressEvent(self, mouseEvent):
    originalSize = self.originalImage.size()
    size = self.size()
    if (originalSize.width() > size.width()) or (originalSize.height() > size.height()):
        self.magnify = True
    self.updateLens(mouseEvent)

  def mouseReleaseEvent(self, mouseEvent):
    self.magnify = False
    self.updateLens(mouseEvent)

  def mouseMoveEvent(self, mouseEvent):
    self.updateLens(mouseEvent)
