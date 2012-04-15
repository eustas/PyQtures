'''
Created on 13.04.2012

@author: eustas
'''

from PyQt4 import QtCore
from PyQt4 import QtGui

class ImageLoader(object):

  def __init__(self):
    self.originals = dict()

  def getImage(self, path):
    if path in self.originals:
      return self.originals[path]
    result = QtGui.QPixmap(path)
    self.originals[path] = result
    return result

  def getScaledImage(self, path, maxWidth, maxHeight):
    raw = self.getImage(path)
    #TODO: Cache
    return raw.scaled(maxWidth, maxHeight, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)