# -*- coding: utf-8 -*-
"""
@author: Cédric Berteletti
Folder explorer
"""

import logging
from os import listdir
from os.path import isfile, join

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import  QStyle, QFileDialog, QFrame, QScrollArea, QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout

from services.internationalization import l
from services.mipmaps import MipmapLevels, MipmapService
import services.settings as settings
from services.states.image_state import ImageState
from ui.image_vignette import ImageVignette
from ui.ui_utils import set_default_layout_params



class SourceImagesExplorer(QFrame):
    "Displays the image present in a folder"

    imageSelected = pyqtSignal(ImageState)

    def __init__(self):
        super().__init__()
        self.imagespath = ""
        self.images = []
        self.scrollContent = None
        self.init_ui()



    def init_ui(self):
        self.setLayout(QVBoxLayout(self))
        set_default_layout_params(self.layout())

        # Toolbar - BEGIN
        self.toolbar = QFrame(self)
        self.toolbar.setLayout(QHBoxLayout(self.toolbar))
        set_default_layout_params(self.toolbar.layout())
        self.layout().addWidget(self.toolbar)

        # Home folder button
        pixmapi = QStyle.StandardPixmap.SP_DirHomeIcon
        icon = self.style().standardIcon(pixmapi)
        home_button = QPushButton(icon, "")
        self.toolbar.layout().addWidget(home_button)
        home_button.clicked.connect(self.select_path)

        # Toolbar - END
        self.toolbar.layout().addStretch()

        # Images scroll area
        self.scroll = QScrollArea(self)
        self.layout().addWidget(self.scroll)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setMinimumWidth(MipmapService().mipmap_size(MipmapLevels.VIGNETTE)+10)


    def resizeEvent(self, event):
        if self.scrollContent:
            new_nb_columns = self.nb_columns_possible()
            if new_nb_columns != self.nb_columns:
                self.init_scroll_content()
        return super(SourceImagesExplorer, self).resizeEvent(event)


    def select_path(self):
        self.imagespath = QFileDialog.getExistingDirectory(self, l("msg.select_images"))
        self.init_images()
        self.init_scroll_content()


    def init_images(self):        
        if self.imagespath:
            self.images = []
            logging.info(f"New source folder : {self.imagespath}")
            files = [f for f in listdir(self.imagespath) if isfile(join(self.imagespath, f))]

            for f in files:
                image_path = join(self.imagespath, f)
                image = ImageState(image_path)
                self.images.append(image)


    def init_scroll_content(self):
        self.scrollContent = QFrame(self.scroll)
        self.scroll.setWidget(self.scrollContent)
        layout = QGridLayout(self.scrollContent)
        set_default_layout_params(layout)

        self.nb_columns = self.nb_columns_possible()

        index_row = 0
        index_col = 0
        for image in self.images:
                vignette = ImageVignette(image)
                vignette.clicked.connect(self.image_selected)

                layout.addWidget(vignette, index_row, index_col)
                index_col += 1
                if index_col == self.nb_columns:
                    index_col = 0
                    index_row += 1

        layout.setRowStretch(layout.rowCount(), 1)


    def nb_columns_possible(self):
        return self.geometry().width() // MipmapService().mipmap_size(MipmapLevels.VIGNETTE)

    
    def image_selected(self, image):        
        logging.debug(f"New image selected for process/display : {image.original_image_path}")
        self.imageSelected.emit(image)

                
