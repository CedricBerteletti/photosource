# -*- coding: utf-8 -*-
"""
@author: Cédric Berteletti
Previews explorer
"""

from PyQt6.QtWidgets import QFrame, QHBoxLayout

from ui.ui_utils import set_default_layout_params


class StatusBar(QFrame):
    def __init__(self):
        super().__init__()
        self.init_ui()


    def init_ui(self):
        self.setLayout(QHBoxLayout(self))
        set_default_layout_params(self.layout())

