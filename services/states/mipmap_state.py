# -*- coding: utf-8 -*-
"""
@author: Cédric Berteletti
"""


import os
from os.path import isfile


LOADING_IMAGE_FILEPATH = os.path.join("images", "rounded_blocks.gif")
#LOADING_IMAGE_FILEPATH = os.path.join("images", "flowing_gradient.gif")


class MipmapState():
    def __init__(self, mipmap_path, loaded=False):
        super().__init__()
        self.mipmap_path = mipmap_path
        self.loaded = loaded

    
    def is_available(self):
        self.loaded = isfile(self.mipmap_path)
        return self.loaded


    def path(self):
        if self.is_available():
            return self.mipmap_path
        else:
            return LOADING_IMAGE_FILEPATH