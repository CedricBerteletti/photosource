# -*- coding: utf-8 -*-
"""
@author: Cédric Berteletti
Main library of functions for processing an image
"""

import cv2 as cv
from enum import Enum
import numpy as np


OpenCvFormats = Enum("OpenCvFormats", ["RGB32", "HSV32"])

class ImageProcessed():
    def __init__(self, data, format=OpenCvFormats.RGB32):
        super().__init__()
        self.data = data
        self.format = format
        self.current_preview_index = 0

    def next_preview_index(self):
        self.current_preview_index += 1
        return self.current_preview_index

    def rgb32(self):
        if self.format == OpenCvFormats.RGB32:
            pass
        elif self.format == OpenCvFormats.HSV32:
            self.data = cv.cvtColor(self.data, cv.COLOR_HSV2RGB)
            self.format = OpenCvFormats.RGB32
        else:
            raise Exception("Unknown image data format", "")
        return self

    def hsv32(self):
        if self.format == OpenCvFormats.HSV32:
            pass
        elif self.format == OpenCvFormats.RGB32:
            self.data = cv.cvtColor(self.data, cv.COLOR_RGB2HSV)
            self.format = OpenCvFormats.HSV32
        else:
            raise Exception("Unknown image data format", "")
        return self


def write_image(img, filepath, format, errors):
    # Writing image with OpenCV
    if format == "jpg":
        params = [cv.IMWRITE_JPEG_QUALITY, 100]
    elif format == "tif":
        params = []
    else:
        params = []
    if not cv.imwrite(filepath, img.rgb32().data.astype(np.int16), params):
        errors.append(f"Unable to write image {filepath}")
    return errors


def preview(img, name="", group=""):
    # TODO
    pass


def saturation(img, saturation):
    (h, s, v) = cv.split(img.hsv32().data)
    s = s * saturation
    img.data = cv.merge([h,s,v])
    return img