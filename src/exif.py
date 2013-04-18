'''
Created on 14.04.2013

@author: eustas
'''

from PyQt4.QtCore import Qt


class Exif(object):
  def __init__(self, path):
    self._path = path
    self.orientation = 0
    if path.endsWith('.jpg', cs=Qt.CaseInsensitive):
      self._read_jpeg()

  def _read_jpeg(self):
    with open(self._path, 'rb') as f:
      segments = []
      offset = 0
      soi = f.read(2)
      offset += 2
      if soi != '\xFF\xD8':
        print 'JPEG: SOI marker missing.'
        return
      while True:
        segment_offset = offset
        segment_id = f.read(2)
        offset += 2
        if segment_id[0] != '\xFF':
          print 'JPEG: marker missing @ %d' % (segment_offset)
          break
        segment_id = ord(segment_id[1])
        if segment_id == 0xDA:  # Start-of-scan
          # print 'SOS'
          break
        if segment_id == 0xD9:  # End-of-image
          # print 'EOI'
          break
        segment_length = f.read(2)
        segment_length = (ord(segment_length[0]) << 8) + ord(segment_length[1])
        offset += segment_length
        segment_head = f.read(6)
        segments.append((segment_id, segment_offset, segment_length, segment_head))
        f.seek(segment_length)
      for (segment_id, segment_offset, segment_length, segment_head) in segments:
        # print 'Id: %d | Head: %s' % (segment_id, segment_head)
        if segment_id == 0xE1 and segment_head == 'Exif\0\0':
          self._read_exif(f, segment_offset, segment_length)

  def _read_int(self, string):
    result = 0
    for byte in string:
      result = 256 * result + ord(byte)
    return result

  def _read_exif(self, src, segment_offset, unused_length):
    offset = segment_offset + 2 + 2 + 6;
    src.seek(offset)
    order = src.read(2)
    fix_order = lambda string: string
    if order == 'MM':
      pass
    elif order == 'II':
      fix_order = lambda string: string[::-1]
    else:
      print 'Unknown endianess marker: %s' % order
      return
    tiffMarker = self._read_int(fix_order(src.read(2)))
    if tiffMarker != 0x002A:
      print 'Unknown tiffMarker: %s' % tiffMarker
      return

    ifdOffset = offset + self._read_int(fix_order(src.read(4)))
    src.seek(ifdOffset)
    tag_count = self._read_int(fix_order(src.read(2)))
    for unused in range(tag_count):
      tag_id = self._read_int(fix_order(src.read(2)))
      tag_type = self._read_int(fix_order(src.read(2)))
      tag_length = self._read_int(fix_order(src.read(4)))
      tag_value = src.read(4)
      # print '%d: %d %d %d' % (i, tag_id, tag_type, tag_length)
      if tag_id == 274 and tag_type == 3 and tag_length == 1:
        orientation_id = self._read_int(fix_order(tag_value[0:2]))
        if orientation_id == 3:
          self.orientation = 180
        elif orientation_id == 6:
          self.orientation = 270
        elif orientation_id == 8:
          self.orientation = 90
