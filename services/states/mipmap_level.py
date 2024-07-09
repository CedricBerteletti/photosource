# -*- coding: utf-8 -*-
"""
@author: Cédric Berteletti
"""


from enum import Enum


MipmapLevels = Enum("MipmapLevels", ["FULL", "VIGNETTE", "PREVIEW", "SCREEN"])

class MipmapLevel():
    def __init__(self, name, size):
        self.name = name
        self.size = size