# -*- coding: utf-8 -*-
"""
@author: Cédric Berteletti
Previews explorer
"""


import copy

from PyQt6.QtWidgets import QFrame, QVBoxLayout

from ui.ui_utils import set_default_layout_params


class PreviewsExplorer(QFrame):
    def __init__(self):
        super().__init__()
        self.image = None
        self.scrollContent = None
        self.init_ui()


    def set_image(self, image):
        self.image = copy.copy(image)
        self.init_previews()


    def init_ui(self):
        self.setLayout(QVBoxLayout(self))
        set_default_layout_params(self.layout())
        
        # TODO


    def init_previews(self):
        if self.image is not None:
            # TODO
            pass
            


    #     self.init_ui()


    # def init_ui(self):
    #     self.setLayout(QGridLayout(self))
    #     set_default_layout_params(self.layout())

    #     pixmapi = QStyle.StandardPixmap.SP_DirHomeIcon
    #     icon = self.style().standardIcon(pixmapi)        
    #     self.layout().addWidget(QPushButton(icon, "Name"))


