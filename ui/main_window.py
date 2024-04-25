# -*- coding: utf-8 -*-
"""
@author: Cédric Berteletti
Main window
"""


from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QDockWidget

import services.settings as settings
from services.internationalization import l
from ui.folder_explorer import FolderExplorer
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
        self.folderExplorerWidget = QDockWidget(l("msg.folder_explorer"), self)
        self.folderExplorerWidget.setWidget(FolderExplorer())
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.folderExplorerWidget)

        # Preview images explorer
        self.previewsExplorerWidget = QDockWidget(l("msg.previews_explorer"), self)
        self.previewsExplorerWidget.setWidget(PreviewsExplorer())
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.previewsExplorerWidget)
        
        # Process editor
        self.processEditorWidget = QDockWidget(l("msg.process_editor"), self)
        self.processEditorWidget.setWidget(ProcessEditor())
        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, self.processEditorWidget)

        # Status bar
        self.statusBarWidget = QDockWidget(None, self)
        self.statusBarWidget.setWidget(StatusBar())
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.statusBarWidget)

        # Main image explorer
        self.main_widget = ImageExplorer()
        self.setCentralWidget(self.main_widget)

        # Signals
        # Selecting a vignette
        self.folderExplorerWidget.widget().imageSelected.connect(self.processEditorWidget.widget().set_image)
        self.folderExplorerWidget.widget().imageSelected.connect(self.previewsExplorerWidget.widget().set_image)
        self.folderExplorerWidget.widget().imageSelected.connect(self.main_widget.set_image)

        # Selecting a preview
        # TODO










