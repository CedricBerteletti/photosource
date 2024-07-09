# -*- coding: utf-8 -*-
"""
@author: Cédric Berteletti
Simple Qt widget for displaying an image
"""


from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel


class SimpleImage(QLabel):
    def __init__(self, image_mipmap):
        super().__init__()
        self.image_mipmap = image_mipmap
        self.init_ui()


    def init_ui(self):
        pixmap = QPixmap(self.image_mipmap.path())        
        self.setPixmap(pixmap)





