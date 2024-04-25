# -*- coding: utf-8 -*-
"""
@author: Cédric Berteletti
Simple Qt widget for displaying an image
"""


from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel


class SimpleImage(QLabel):
    def __init__(self, imagepath):
        super().__init__()
        self.imagepath = imagepath
        self.init_ui()


    def init_ui(self):
        pixmap = QPixmap(self.imagepath)        
        self.setPixmap(pixmap)





