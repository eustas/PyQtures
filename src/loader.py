'''
Created on 13.04.2012

@author: eustas
'''

from PyQt4.QtCore import Qt

from PyQt4.QtGui import QPixmap

# TODO(eustas): May be use QPixmapCache?

class _Node(object):
  def __init__(self, path, image):
    self.prev = None
    self.next = None
    self.path = path
    self.image = image


class Loader(object):

  def __init__(self, limit):
    self._limit = limit
    self._empty_image = QPixmap()
    self._count = 0
    self._head = _Node(None, None)
    self._tail = _Node(None, None)
    self._head.next = self._tail
    self._tail.prev = self._head

    self._cache = dict()

  def load_image(self, path):
    if not path:
      return self._empty_image

    if not Loader.is_image(path):
      return self._empty_image

    if path in self._cache:
      node = self._cache[path]
      self._pull(node)
      return node.image
    image = QPixmap(path)
    node = _Node(path, image)
    self._cache[path] = node
    cast_off = self._push(node)
    if cast_off:
      del self._cache[cast_off.path]
      print 'discarded  [%s]' % cast_off.path
    return image

  def _pull(self, node):
    node.prev.next = node.next
    node.next.prev = node.prev
    self._count -= 1
    self._push(node)

  def _push(self, node):
    cast_off = None
    if self._count == self._limit:
      cast_off = self._head.next
      self._head.next = cast_off.next
      cast_off.next.prev = self._head
      cast_off.next = None
      cast_off.prev = None
      self._count -= 1

    node.prev = self._tail.prev
    node.prev.next = node
    self._tail.prev = node
    node.next = self._tail
    self._count += 1

    return cast_off

  @staticmethod
  def is_image(path):
    return path.endsWith('.jpg', cs=Qt.CaseInsensitive) or path.endsWith('.png', cs=Qt.CaseInsensitive)
