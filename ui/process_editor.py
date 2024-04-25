# -*- coding: utf-8 -*-
"""
@author: Cédric Berteletti
Source code editor for the processing of the image
"""

import logging

from PyQt6.QtWidgets import QFrame, QPushButton, QTextEdit, QHBoxLayout, QVBoxLayout, QStyle

from services.processor import ProcessorService, PROCESS_DEFAULT_ID, PROCESS_DEFAULT_TEMPLATE_PATH
from ui.ui_utils import set_default_layout_params


class ProcessEditor(QFrame):
    def __init__(self):
        super().__init__()
        self.image = None
        self.init_ui()        


    def init_ui(self):
        self.setLayout(QVBoxLayout(self))
        set_default_layout_params(self.layout())

        # Toolbar - BEGIN
        self.toolbar = QFrame(self)
        self.toolbar.setLayout(QHBoxLayout(self.toolbar))
        set_default_layout_params(self.toolbar.layout())
        self.layout().addWidget(self.toolbar)
        
        self.toolbar.layout().addStretch()

        # Launch processing preview of the current image
        pixmapi = QStyle.StandardPixmap.SP_MediaPlay
        icon = self.style().standardIcon(pixmapi)
        generate_button = QPushButton(icon, "")
        self.toolbar.layout().addWidget(generate_button)
        generate_button.clicked.connect(self.generate_preview)

        # Launch processing preview for all image of the folder
        pixmapi = QStyle.StandardPixmap.SP_MediaSkipForward
        icon = self.style().standardIcon(pixmapi)
        generate_all_button = QPushButton(icon, "")
        self.toolbar.layout().addWidget(generate_all_button)
        generate_all_button.clicked.connect(self.generate_all_previews)

        self.toolbar.layout().addStretch()

        # Export
        pixmapi = QStyle.StandardPixmap.SP_ArrowUp
        icon = self.style().standardIcon(pixmapi)
        export_button = QPushButton(icon, "")
        self.toolbar.layout().addWidget(export_button)
        export_button.clicked.connect(self.export)

        # Toolbar - END

        self.textedit = QTextEdit()
        self.textedit.textChanged.connect(self.text_changed)
        self.layout().addWidget(self.textedit)


    def set_image(self, image):
        self.image = image
        self.textedit.setPlainText(self.image.process_result)


    def text_changed(self):
        self.image.process_result = self.textedit.toPlainText()
        with open(self.image.result_script_path(), "w") as file:
            file.write(self.image.process_result)


    def generate_preview(self):
        if self.image is not None:
            logging.info(f"Processing the previews for the image")
            ProcessorService().process(self.image.original_image_path, self.image.temp_folder(), self.image.temp_folder(), self.image.get_original_basename(), self.image.process_result, process_id=PROCESS_DEFAULT_ID)


    def generate_all_previews(self):
        logging.info(f"Processing the previews for all images")

        # TODO


    def export(self):
        if self.image is not None:
            logging.info(f"Exporting the image")

            # TODO


