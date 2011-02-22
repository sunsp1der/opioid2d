
__all__ = [
    "Bitmap",
    ]

import pygame
import Opioid2D.internal.bitmap_transform as t

## TODO: clean up Bitmap API

class Bitmap(object):
    
    def __init__(self, surface):
        size = surface.get_size()
        s = pygame.Surface(size, pygame.SRCALPHA, 32)
        s.fill((0,0,0,0))
        s.blit(surface.convert_alpha(s), (0,0))
        self.surface = s
        self.width,self.height = size
        self.size = size
    
    def copy(self):
        return Bitmap(self.surface.copy())
    
    @classmethod
    def Load(cls, file):
        if isinstance(file, basestring):
            file = open(file, "rb")
        surface = pygame.image.load(file, file.name)
        return Bitmap(surface)
    
#    def GetWidth(self):
#        return self.width
#    
#    def GetHeight(self):
#        return self.height
#    
#    def LockBytes(self):
#        pass
#    
#    def UnlockBytes(self):
#        pass
    
    def get_bytes(self):
        return pygame.image.tostring(self.surface, "RGBA")
    
    def transform(self, func, *arg, **kw):
        return Bitmap(func(self.surface, *arg, **kw))
    
#    def MakeAlphaMultiplied(self):
#        return Bitmap(t.make_alphamultiplied(self.surface))
#     
#    def MakeStencil(self):
#        return Bitmap(t.make_stencil(self.surface))
#    
#    def MakeGrayscale(self):
#        return self
#    
#    def MakeBordered(self, border=1):
#        return Bitmap(t.make_bordered(self.surface, border))
    
    def get_subbitmap(self, srcx, srcy, width, height):
        return Bitmap(self.surface.subsurface((srcx,srcy,width,height)))
    