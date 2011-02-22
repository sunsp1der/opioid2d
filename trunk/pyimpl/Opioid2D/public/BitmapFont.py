
__all__ = [
    "BitmapFont", 
    ]

import pygame
from os.path import splitext
import cPickle as pickle

from Opioid2D.internal.textures import TextureManager
from Opioid2D.public.Node import Node
from Opioid2D.public.Sprite import Sprite
from Opioid2D.public.Bitmap import Bitmap
from Opioid2D.public.Image import ImageInstance
from Opioid2D.public.ResourceManager import ResourceManager
    
class BitmapFont(object):

    def __init__(self, fontfile, pngfile=None, spacing=0, linespacing=0):
        """Open a previously created bitmap font"""
        if pngfile is None:
            pngfile = splitext(fontfile)[0]+".png"
        f = open(fontfile, "rb")
        data = f.read()
        f.close()
        data = pickle.loads(data)
        f.close()
        self.chardict = {}
        self.bmpdict = {}
        self.texmgr = TextureManager()
        s = Bitmap.Load(open(pngfile,"rb"))
        for k, (x, y, w, h) in data.char_rects.iteritems():
            bmp = s.get_subbitmap(x, y, w, h)
            img = self.texmgr.add_image(bmp)
            img.hotspot.set(0, 1)
            self.chardict[k] = ImageInstance(img)
            self.bmpdict[k] = bmp
        self.linesize = data.linesize
        self.padding = data.padding
        self.spacing = spacing
        self.linespacing = linespacing
        
    def create(self, s, single=False):
        if single:
            return self.create_single(s)
        n = Sprite()
        xpos = 0
        ypos = 0
        xmax = 0
        nx = 0
        ny = 0
        height = self.linesize
        padleft, padright, padtop, padbottom = self.padding
        nx -= padleft
        ny += height-padtop
        n.letters = []
        n.font = self
        for c in s:
            if c == '\n':
                xmax = max(xpos, xmax)
                ypos += height + self.linespacing
                nx -= xpos
                ny += height + self.linespacing
                xpos = 0
            img = self.chardict.get(c, None)
            if img is None:
                continue
            s = Sprite(img)
            img = img._cObj
            s.attach_to(n)
            s.position = nx, ny
            n.letters.append(s)
            nx += img.w - padleft - padright + self.spacing
            xpos += img.w - padleft - padright + self.spacing
        #n.rect = (0, 0, xmax, ypos+height)
        return n
    
    def create_surface(self, s):
        xpos = 0
        ypos = 0
        xmax = 0
        ymax = 0
        nx = 0
        ny = 0
        height = self.linesize
        padleft, padright, padtop, padbottom = self.padding
        xpos += padleft
        #ny += height-padtop
        blits = []
        for c in s:
            if c == '\n':
                xmax = max(xpos, xmax)
                ymax = 0
                ypos += height + self.linespacing
                nx -= xpos
                ny += height + self.linespacing
                xpos = 0
            bmp = self.bmpdict.get(c, None)
            if bmp is None:
                continue
            blits.append((bmp,nx,ny))
            ymax = max(ymax, bmp.height)
            nx += bmp.width - padleft - padright + self.spacing
            xpos += bmp.width - padleft - padright + self.spacing
        xmax = max(xmax,xpos)
        size = xmax,ypos+ymax
        s = pygame.Surface(size, pygame.SRCALPHA, 32)
        #s.fill((255,255,255,255))
        s.fill((0,0,0,0))
        for bmp,x,y in blits:
            s.blit(bmp.surface, (x, y))
        return s
            
    def create_single(self, s):
        surf = self.create_surface(s)
        img = ResourceManager._create_image(Bitmap(surf))
        return Sprite(img)


