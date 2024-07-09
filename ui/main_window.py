# -*- coding: utf-8 -*-
"""
@author: Cédric Berteletti
Main window
"""


from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QDockWidget

import services.settings as settings
from services.internationalization import l
from ui.source_images_explorer import SourceImagesExplorer
from ui.previews_explorer import PreviewsExplorer
from ui.process_editor import ProcessEditor
from ui.image_explorer import ImageExplorer
from ui.status_bar import StatusBar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"{l("msg.photosource.name")} {settings.get("photosource.version")}")

        self.setCorner(Qt.Corner.TopLeftCorner, Qt.DockWidgetArea.LeftDockWidgetArea)
        self.setCorner(Qt.Corner.TopRightCorner, Qt.DockWidgetArea.RightDockWidgetArea)
        #self.setCorner(Qt.Corner.BottomLeftCorner, Qt.DockWidgetArea.LeftDockWidgetArea)
        #self.setCorner(Qt.Corner.BottomRightCorner, Qt.DockWidgetArea.RightDockWidgetArea)

        # Source folder images explorer
        self.sourceImagesExplorerWidget = self.create_dock_widget(l("msg.folder_explorer"), SourceImagesExplorer())
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.sourceImagesExplorerWidget)

        # Preview images explorer
        self.previewsExplorerWidget = self.create_dock_widget(l("msg.previews_explorer"), PreviewsExplorer())
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.previewsExplorerWidget)
        
        # Process editor
        self.processEditorWidget = self.create_dock_widget(l("msg.process_editor"), ProcessEditor())
        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, self.processEditorWidget)

        # Status bar
        self.statusBarWidget = self.create_dock_widget(None, StatusBar())
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.statusBarWidget)

        # Main image explorer
        self.main_widget = ImageExplorer()
        self.setCentralWidget(self.main_widget)

        # Signals
        # Selecting a vignette
        self.sourceImagesExplorerWidget.widget().imageSelected.connect(self.processEditorWidget.widget().set_image)
        self.sourceImagesExplorerWidget.widget().imageSelected.connect(self.previewsExplorerWidget.widget().set_image)
        self.sourceImagesExplorerWidget.widget().imageSelected.connect(self.main_widget.set_image)

        # Selecting a preview
        # TODO

    def create_dock_widget(self, title, insideWidget):
        dw = QDockWidget(title, self)
        dw.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetFloatable |
                       QDockWidget.DockWidgetFeature.DockWidgetMovable)
        dw.setWidget(insideWidget)
        return dw










