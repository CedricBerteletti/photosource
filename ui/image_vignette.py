# -*- coding: utf-8 -*-
"""
@author: Cédric Berteletti
Qt widget for displaying an image vignette
"""


import copy

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QGridLayout

from services.mipmaps import MipmapService, MipmapLevels
from services.states import ImageState
from ui.image_simple import SimpleImage
from ui.ui_utils import set_default_layout_params


class ImageVignette(QWidget):
    clicked = pyqtSignal(ImageState)

    def __init__(self, image):
        super().__init__()
        self.image = copy.copy(image)
        self.image.mipmap = MipmapLevels.VIGNETTE
        self.init_ui()        


    def init_ui(self):        
        layout = QGridLayout(self)        
        set_default_layout_params(layout)
        vignette = SimpleImage(MipmapService().image_mipmap(self.image).path())
        layout.addWidget(vignette, 0, 0, alignment=Qt.AlignmentFlag.AlignHCenter)


    def mouseReleaseEvent(self, e):
        self.clicked.emit(self.image)