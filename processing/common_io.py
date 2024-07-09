# -*- coding: utf-8 -*-
"""
@author: Cédric Berteletti
Main library of functions for loading and saving an image
"""


import cv2 as cv
import numpy as np


def load_image(filepath):
    return cv.imread(filepath).astype(np.float32)

def write_image(img, filepath, format, errors):
    # Writing image with OpenCV
    if format == "jpg":
        params = [cv.IMWRITE_JPEG_QUALITY, 100]
    elif format == "tif":
        params = []
    else:
        params = []
    if not cv.imwrite(filepath, img.astype(np.int16), params):
        errors.append(f"Unable to write image {filepath}")
    return errors