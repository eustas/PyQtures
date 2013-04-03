'''
Created on 13.04.2012

@author: eustas
'''

from PyQt4 import QtGui


class Loader(object):

  def __init__(self):
    self.originals = dict()

  def load_image(self, path):
    if path in self.originals:
      return self.originals[path]
    result = QtGui.QPixmap(path)
    self.originals[path] = result
    return result