"""ResourceManager
"""

__all__ = [
    "ResourceManager",
    ]

import os, zipfile, re
from glob import glob
import StringIO as StringIO

from Opioid2D.internal.textures import TextureManager
from Opioid2D.internal.gridimage import GridImage
from Opioid2D.public.Image import Image, ImageMeta, ImageInstance
from Opioid2D.public.Bitmap import Bitmap
import Opioid2D.internal.bitmap_transform as transform

import cOpioid2D as _c

def _globre(g):
    g = re.escape(g)
    g = g.replace(r"\?", ".")
    g = g.replace(r"\*", ".*?")
    return re.compile(g+"$")

class ResourceManager(object):
    """ResourceManager singleton
    """
    def __init__(self):
        self.images = {}
        self.patterns = {}
        self._texmgr = TextureManager()
        self.path = None
        
    def set_source(self, path):
        """Set the source path for resource loading (defaults to current dir)"""
        self.path = path
        
    def open_resource(self, name):
        if self.path is not None:
            if zipfile.is_zipfile(self.path):
                z = zipfile.ZipFile(self.path)
                s = z.read(name.replace("\\", "/"))
                z.close()
                sio = StringIO.StringIO(s)
                sio.name = name
                return sio
            return open(os.path.join(self.path, name), "rb")
        return open(name, "rb")

    def find_resources(self, pattern):
        if self.path is not None:
            if zipfile.is_zipfile(self.path):
                z = zipfile.ZipFile(self.path)
                names = z.namelist()
                r = _globre(pattern)
                return [name for name in names if r.match(name)]
            return glob(os.path.join(self.path, pattern))
        return glob(pattern)

    def preload_images(self, pattern):
        files = self.find_resources(pattern)
        for fn in files:
            fn = fn.replace(os.path.sep, "/")
            for img in ImageMeta.subclasses:
                if img.filename == fn:
                    self.get_image(img)
                    break
            else:
                self.get_image(fn)
                
    def clear_cache(self):
        """Removes everything from cache"""
        self.images = {}
        self.patterns = {}

    def get_image(self, image, hotspot=None, mode=None, border=None):
        """Load an image from the given path
        
        The image is cached and the same Image instance is returned on
        subsequent calls.
        """
        if isinstance(image, type) and issubclass(image, Image):
            image = image()
        elif not isinstance(image, Image):
            filename = image
            image = Image()
            image.filename = filename
        if mode or hotspot or border:
            image = image.copy()
            if hotspot is not None:
                image.hotspot = hotspot        
            if mode is not None:
                image.mode = mode
            if border is not None:
                image.border = border
        if isinstance(image.mode, basestring):
            image.mode = [image.mode]
        try:
            return self.images[image]
        except KeyError:
            if not image.filename:
                raise ValueError("no filename specified in Image definition for %s" % image.__class__.__name__)
            bmp = self._load_bitmap(image.filename)            
            for mod in image.mode:
                try:
                    func = getattr(transform, "make_"+mod)
                except AttributeError:
                    raise ValueError("invalid Image mode: %r" % mod)
                bmp = bmp.transform(func)
            img = self._set_image(image, bmp, hotspot=image.hotspot, border=image.border)
            img._cObj.hotspot.set(*image.hotspot)
            for c in image.collision:
                img.add_collision_node(*c)            
            return img
        
    def get_strip(self, image, width):
        """Load an image strip and return a list of images
        """
        pass
    
    def get_grid(self, image, width, height, hotspot=None):
        """Load an image grid and return a list of images
        """
        bmp = self._load_bitmap(image)
        cols = bmp.width // width
        rows = bmp.height // height
        result = []
        for r in range(rows):
            for c in range(cols):
                sb = bmp.get_subbitmap(c*width,r*height,width,height)
                result.append(self._create_image(sb,hotspot))
        return result
    
    def get_pattern(self, pattern=None, hotspot=None, mode=None, border=None):
        """Load images using a glob pattern"""
        if pattern in self.patterns:
            return self.patterns[pattern]
        files = self.find_resources(pattern)
        files.sort()
        images = []
        for fn in files:
            images.append(self.get_image(fn, hotspot=hotspot, mode=mode, border=border))
        self.patterns[pattern] = images
        return images


    def _set_image(self, key, bmp, hotspot=None, border=1):
        img = self._create_image(bmp, hotspot, border)
        img._key = key
        self.images[key] = img
        return img
    
    def _create_image(self, bmp, hotspot=None, border=1):
        if bmp.width+border*2 > 512 or bmp.height+border*2 > 512:
            img = GridImage(bmp, border=border)
        else:
            if border:
                bmp = bmp.transform(transform.make_bordered, border)
            img = self._texmgr.add_image(bmp, border)
            img = ImageInstance(img)
        if hotspot:
            img._cObj.hotspot.set(*hotspot)
        return img

    def _load_bitmap(self, src):
        if not hasattr(src, "read"):
            src = self.open_resource(src)
        # read from file-like object
        bmp = Bitmap.Load(src)
        return bmp

ResourceManager = ResourceManager()
