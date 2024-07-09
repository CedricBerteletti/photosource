# -*- coding: utf-8 -*-
"""
@author: Cédric Berteletti
"""


class Task():
    def __init__(self, image_state, size):
        super().__init__()
        self.image_state = image_state
        self.size = size
        self.completed = False
