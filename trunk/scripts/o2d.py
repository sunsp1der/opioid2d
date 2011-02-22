
import sys,os

def _parse(args):
    cmd,args = args[0],args[1:]
    kw = {}
    for a in args[:]:
        if a.startswith("--"):
            k,v = a[2:].split("=",1)
            args.remove(a)
            kw[k] = v

    if cmd == 'makefont':
        makefont(*args, **kw)

def makefont(ttffile, basename=None, size=24, chars=None, padding=0, antialias=1):
    import pygame
    from OpioidTools.text import create_bitmapfont
    pygame.font.init()
    if basename is None:
        basename = os.path.splitext(ttffile)[0]
    size = int(size)
    pad = int(padding)
    antialias = int(antialias)
    print "creating bitmap font:", basename+".o2f"
    create_bitmapfont((ttffile,size), basename, chars, pad, pad, pad, pad, antialias)

if __name__ == '__main__':
    _parse(sys.argv[1:])
