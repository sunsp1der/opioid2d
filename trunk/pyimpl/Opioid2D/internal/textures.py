
__all__ = [
    "TextureManager",
    ]

import cOpioid2D as _c

class TextureSheet(object):
    TEXSIZE = 512

    def __init__(self):
        self._tex = _c.Texture(self.TEXSIZE)

        self.y = 0
        self.next_y = 0
        self.x = 0

    def insert_image(self, w, h, data, border=0):
        if self.x + w <= 512:
            if  self.y + h > 512:
                return None
            x = self.x
            y = self.y
        else:
            if self.next_y + h <= self.TEXSIZE:
                x = 0
                y = self.next_y
            else:
                return None
        if y != self.y:
            self.y = y
        self.x = x + w
        if self.y + h > self.next_y:
            self.next_y = self.y + h
        self._tex.WriteBytes(x,y,w,h,data)
        ts = float(self.TEXSIZE)
        return _c.Image(self._tex, w-border*2, h-border*2, (x+border)/ts, (y+border)/ts, (x+w-border)/ts, (y+h-border)/ts)
                

class TextureManager(object):
    def __init__(self):
        self.sheets = []

    def add_image(self, bmp, border=0):
        if not self.sheets:
            self.sheets.append(TextureSheet())
        xs = bmp.width
        ys = bmp.height
        bytes = bmp.get_bytes()
        for s in self.sheets:
            img = s.insert_image(xs,ys,bytes,border)
            if img is not None:
                return img
        if img is None:
            sheet = TextureSheet()
            self.sheets.append(sheet)
            img = sheet.insert_image(xs,ys,bytes,border)
            assert img is not None
            return img
