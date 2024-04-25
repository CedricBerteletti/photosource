# -*- coding: utf-8 -*-
"""
@author: Cédric Berteletti
Service handling mipmaps of images
"""


import cv2 as cv
from enum import Enum
import logging
import numpy as np
from os import makedirs
from os.path import dirname, isfile

import services.settings as settings
from services.singleton import SingletonMeta


DEFAULT_IMAGE_FORMAT = "png"

MipmapLevels = Enum("MipmapLevels", ["FULL", "VIGNETTE", "PREVIEW", "SCREEN"])

class MipmapLevel():
    def __init__(self, name, size):
        self.name = name
        self.size = size


class MipmapState():
    def __init__(self, mipmap_path, loaded=False):
        super().__init__()
        self.mipmap_path = mipmap_path
        self.loaded = loaded

    
    def is_available(self):
        return isfile(self.mipmap_path)


    def path(self):
        # TODO
        return self.mipmap_path
    

class MipmapService(metaclass=SingletonMeta):

    def __init__(self):
        super().__init__()
        self.mipmapLevels = {}
        self.mipmapLevels[MipmapLevels.VIGNETTE] = MipmapLevel(settings.get("mipmaps.vignette.suffix"), settings.get_int("mipmaps.vignette.size"))
        self.mipmapLevels[MipmapLevels.PREVIEW] = MipmapLevel(settings.get("mipmaps.preview.suffix"), settings.get_int("mipmaps.preview.size"))
        self.mipmapLevels[MipmapLevels.SCREEN] = MipmapLevel(settings.get("mipmaps.screen.suffix"), settings.get_int("mipmaps.screen.size"))

    def mipmap_size(self, mipmap):
        "Return the max pixel dimension of the image for a mipmap level"
        if mipmap == MipmapLevels.FULL:
            return -1
        else:            
            return self.mipmapLevels[mipmap].size

    def image_mipmap(self, image, extension=DEFAULT_IMAGE_FORMAT):
        "Return the image mipmap for a specific version of the image (full, preview, vignette, etc.)"        

        mipmap_path = image.mipmap_path(extension)
        if not image.is_available():
            self.resize_and_convert(image.original_image_path, mipmap_path, self.mipmapLevels[image.mipmap].size, extension)

        return MipmapState(mipmap_path, loaded=True)
    
    
    def resize_and_convert(self, source, destination, size, format):
        if cv.haveImageReader(source):
            # Open image with OpenCV
            img = cv.imread(source).astype(np.float32)
            image_size = max(img.shape[0], img.shape[1])
            
            base_dir = dirname(destination)
            makedirs(base_dir, exist_ok=True)

            if size > 0:
                factor = size / image_size
                res = cv.resize(img, (0, 0), fx=factor, fy=factor, interpolation = cv.INTER_CUBIC)
            else:
                res = img

            # Writing image with OpenCV
            if format == "jpg":
                params = [cv.IMWRITE_JPEG_QUALITY, 100]
            elif format == "tif":
                params = []
            else:
                params = []
            if not cv.imwrite(destination, res.astype(np.int16), params):
                logging.warning(f"Unable to write image {destination}")
                return False
            return True
        else:
            logging.warning(f"{source} isn't a recognized image format")
            return False
