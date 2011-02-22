
import pygame
_DEBUG = False
try:
    import Numeric as N#@UnresolvedImport
    if _DEBUG: print 'using Numeric'
except:
    import sys
    import numpy.oldnumeric as N
    sys.modules['Numeric'] = N 
    if _DEBUG: print 'using numpy'

__all__ = [
    "make_stencil",
    "make_bordered",
    "make_alphamultiplied",
    "make_grayscale",
    ]

def get_arrays(surf):
    a = pygame.surfarray.array3d(surf)
    aa = pygame.surfarray.array_alpha(surf)
    return a,aa

def get_pixels(surf):
    a = pygame.surfarray.pixels3d(surf)
    aa = pygame.surfarray.pixels_alpha(surf)
    return a,aa

def make_surface(a,aa):
    s = pygame.surfarray.make_surface(a)
    s2 = pygame.Surface(s.get_size(), pygame.SRCALPHA, 32)
    s2.blit(s,(0,0))
    a = pygame.surfarray.pixels_alpha(s2)
    a[...] = aa
    return s2

def make_stencil(surf, r=255,g=255,b=255):
    a,aa = get_arrays(surf)
    a[...,0] = r
    a[...,1] = g
    a[...,2] = b
    return make_surface(a, aa)

def make_bordered(surf, border=1):
    x,y = surf.get_size()
    s = pygame.Surface((x+border*2,y+border*2), 0, surf)
    s.fill((0,0,0,0))
    a,aa = get_pixels(s)
    src,srca = get_pixels(surf)
    a[border:x+border, border:y+border, ...] = src
    aa[border:x+border, border:y+border] = srca
    for i in range(border):
        a[border:x+border, i, ...] = src[:,0,...]
        a[border:x+border, -i-1, ...] = src[:,-1,...]
        aa[border:x+border, i, ...] = srca[:,0,...]
        aa[border:x+border, -i-1, ...] = srca[:,-1,...]
    for i in range(border):
        a[i,...] = a[border, ...]
        a[-i-1,...] = a[-border-1, ...]
        aa[i,...] = aa[border, ...]
        aa[-i-1,...] = aa[-border-1, ...]
    return s

def make_alphamultiplied(surf):
    a,aa = get_arrays(surf)
    a[...,0] = (a[...,0] * (aa / 255.0)).astype(N.UnsignedInt8)
    a[...,1] = (a[...,1] * (aa / 255.0)).astype(N.UnsignedInt8)
    a[...,2] = (a[...,2] * (aa / 255.0)).astype(N.UnsignedInt8)
    s = make_surface(a,aa)
    return s

def make_grayscale(surf):
    a,aa = get_arrays(surf)
    mean = (a[...,0].astype(N.Int) + a[...,1].astype(N.Int) + a[...,2].astype(N.Int)) / 3.0
    mean = mean.astype(N.UnsignedInt8)
    a[...,0] = mean
    a[...,1] = mean
    a[...,2] = mean
    s = make_surface(a,aa)
    return s

make_greyscale = make_grayscale