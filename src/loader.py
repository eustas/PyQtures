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
    self.limit = limit
    self.empty_image = QPixmap()
    self.count = 0
    self.head = _Node(None, None)
    self.tail = _Node(None, None)
    self.head.next = self.tail
    self.tail.prev = self.head

    self.cache = dict()

  def load_image(self, path):
    if not path:
      return self.empty_image

    if not path.endsWith('.jpg', cs=Qt.CaseInsensitive):
      return self.empty_image

    if path in self.cache:
      node = self.cache[path]
      self._pull(node)
      print 'from cache [%s]' % path
      return node.image
    image = QPixmap(path)
    print 'loaded     [%s]' % path
    node = _Node(path, image)
    self.cache[path] = node
    cast_off = self._push(node)
    if cast_off:
      del self.cache[cast_off.path]
      print 'discarded  [%s]' % cast_off.path
    return image

  def _pull(self, node):
    node.prev.next = node.next
    node.next.prev = node.prev
    self.count -= 1
    self._push(node)

  def _push(self, node):
    cast_off = None
    if self.count == self.limit:
      cast_off = self.head.next
      self.head.next = cast_off.next
      cast_off.next.prev = self.head
      cast_off.next = None
      cast_off.prev = None
      self.count -= 1

    node.prev = self.tail.prev
    node.prev.next = node
    self.tail.prev = node
    node.next = self.tail
    self.count += 1

    return cast_off
