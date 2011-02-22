
__all__ = [
    "create_bitmapfont",
    ]

import pickle
import pygame
from Opioid2D.internal.text import BitmapFontData


def create_bitmapfont(font, basename, chars=None, padleft=0, padright=0, padtop=0, padbottom=0, antialias=True):
    """Create a bitmap font template

    font - a pygame Font object or a (name,size) tuple
    chars - a string of characters that will be rendered (defaults to characters with ascii code 32-128)
    padleft, padright, padtop, padbottom - add padding to the characters if you intend to add borders/shadows
    """
    if isinstance(font, tuple):
        fontname, size = font
        try:
            f = pygame.font.Font(fontname, size)
        except IOError:
            f = pygame.font.SysFont(fontname, size)
        font = f
    import Image
    if chars is None:
        chars = map(chr, range(32,128))
    else:
        while 1:
            i = chars.find("..")
            if i == -1:
                break
            c1 = chars[i-1]
            c2 = chars[i+2]
            chars = chars[:i-1] + "".join(map(chr, range(ord(c1),ord(c2)))) + chars[i+2:]
    datfile = basename+".o2f"
    pngfile = basename+".png"
    surfs = []
    maxheight = 0
    width = 0
    for c in chars:
        surf = font.render(c, antialias, (255,255,255,255))
        w,h = surf.get_size()
        maxheight = max(maxheight, h)
        width += w + padright + padleft
        surfs.append(surf)
    height = maxheight + padtop + padbottom
    surf = pygame.Surface((width,height),pygame.SRCALPHA,32)
    surf.fill((0,0,0,0))
    x = 0
    rects = {}
    for c,s in zip(chars,surfs):
        w,h = s.get_size()
        w += padleft + padright
        h += padtop + padbottom
        surf.blit(s, (x+padleft,padtop))
        rects[c] = (x,0,w,h)
        x += w
    dat = pygame.image.tostring(surf,"RGBA")
    img = Image.fromstring("RGBA", surf.get_size(), dat)
    img.save(pngfile, optimize=True)
    dat = BitmapFontData()
    dat.char_rects = rects
    dat.linesize = font.get_linesize() + padtop + padbottom
    dat.padding = (padleft,padright,padtop,padbottom)
    f = open(datfile, "wb")
    pickle.dump(dat, f, 2)
    f.close()
