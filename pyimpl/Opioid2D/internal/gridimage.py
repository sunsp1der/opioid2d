
__all__ = [
    "GridImage",
    ]

import cOpioid2D as _c
from math import ceil

from Opioid2D.internal.textures import TextureManager
from Opioid2D.public.Image import ImageInstance
from Opioid2D.internal import bitmap_transform as transform

def _getdim(x):
    return int(ceil(x/500.0))

class GridImage(ImageInstance):
    def __init__(self, bitmap, grid=None, border=0, imgkey=None):
        if grid is None:
            w = _getdim(bitmap.width+border*2)
            h = _getdim(bitmap.height+border*2)
            grid = (w,h)
        self._grid = grid
        self._border = border
        self._images = []
        self._key = imgkey
        self._textures = TextureManager()
        self._cObj = _c.GridImage(*grid)
        self._split(bitmap)

    def _split(self, bitmap):
        gx,gy = self._grid
        bmpw = bitmap.width
        bmph = bitmap.height
        self._size = bmpw,bmph
        self._cObj.SetSize(bmpw, bmph)
        xs,xr = divmod(bmpw, gx)
        ys,yr = divmod(bmph, gy)
        assert xs < 512-self._border*2 and ys < 512-self._border*2
        scry = 0
        for y in range(gy):
            scrx = 0
            height = ys
            if y < yr:
                height += 1
            row = []
            for x in range(gx):
                width = xs
                if x < xr:
                    width += 1
                bmp = bitmap.get_subbitmap(scrx, scry, width, height)
                #bmp.thisown = 1
                if self._border:
                    bmp = bmp.transform(transform.make_bordered, self._border)
                    #bmp.thisown = 1
                img = self._textures.add_image(bmp, border=self._border)
                row.append(img)
                self._cObj.AppendImage(img)
                scrx += width
            scry += height
            self._images.append(row)
                    
