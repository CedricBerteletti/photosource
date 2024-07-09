# -*- coding: utf-8 -*-
"""
@author: Cédric Berteletti
Image explorer
"""

import copy

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QScrollArea, QVBoxLayout

from services.mipmaps import MipmapService, MipmapLevels
from services.states.image_state import DEFAULT_IMAGE_FORMAT
from ui.image_simple import SimpleImage
from ui.ui_utils import set_default_layout_params


class ImageExplorer(QFrame):
    def __init__(self):
        super().__init__()
        self.image = None
        self.scrollContent = None
        self.init_ui()


    def set_image(self, image):
        self.image = copy.copy(image)
        self.image.mipmap = MipmapLevels.SCREEN
        self.image.format = DEFAULT_IMAGE_FORMAT
        self.init_image()


    def init_ui(self):
        self.setLayout(QVBoxLayout(self))
        set_default_layout_params(self.layout())

        # Image scroll area
        self.scroll = QScrollArea(self)
        self.layout().addWidget(self.scroll)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll.setWidgetResizable(True)


    def init_image(self):
        if self.image is not None:
            self.scrollContent = QFrame(self.scroll)
            self.scroll.setWidget(self.scrollContent)
            layout = QVBoxLayout(self.scrollContent)
            set_default_layout_params(layout)

            image = SimpleImage(MipmapService().image_mipmap(self.image))
            layout.addWidget(image, alignment=Qt.AlignmentFlag.AlignCenter)

