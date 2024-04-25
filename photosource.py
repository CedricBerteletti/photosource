# -*- coding: utf-8 -*-
"""
@author: Cédric Berteletti
A source based image manipulation program
"""

import ctypes
from datetime import datetime
import logging
import platform
import sys

from PyQt6.QtGui import QPalette, QColor, QColorConstants
from PyQt6.QtWidgets import QApplication

import services.internationalization as int
import services.settings as settings
from ui.main_window import MainWindow


def make_dpi_aware():
    "Allow correct display of pyqtgraph graphs on high res screens"
    # if int(platform.release()) >= 8:
    #     ctypes.windll.shcore.SetProcessDpiAwareness(True)
    pass


def main(argv):

    # QT - Interface graphique
    make_dpi_aware()

    # You need one (and only one) QApplication instance per application.
    # Pass in sys.argv to allow command line arguments for your app.
    # If you know you won't use command line arguments QApplication([]) works too.
    app = QApplication(argv)

    # Force the style to be the same on all OS
    app.setStyle(settings.get("theme.main"))
    # Now use a palette to switch to dark colors:
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.WindowText, QColorConstants.White)
    palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColorConstants.Black)
    palette.setColor(QPalette.ColorRole.ToolTipText, QColorConstants.White)
    palette.setColor(QPalette.ColorRole.Text, QColorConstants.White)
    palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ButtonText, QColorConstants.White)
    palette.setColor(QPalette.ColorRole.BrightText, QColorConstants.Red)
    palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColorConstants.Black)
    app.setPalette(palette)
    # Custom styling
    with open("ui/style.qss","r") as style_file:
        app.setStyleSheet(style_file.read())

    # Create a Qt widget, which will be our window.
    window = MainWindow()
    window.showMaximized()  # IMPORTANT!!!!! Windows are hidden by default.

    # Start the event loop.
    app.exec()


settings.init()
int.init(settings.get("language"))
logging.basicConfig(format="%(asctime)s %(levelname)s - %(filename)s:%(lineno)d - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.getLevelName(settings.get("logging.level")))
logging.info(f"{int.l("msg.photosource.name")} {settings.get("photosource.version")}")
if __name__ == "__main__":
    start_time = datetime.now()
    main(sys.argv)
    elapsed_time = datetime.now() - start_time
    logging.info("Elapsed time (hh:mm:ss.ms) {}".format(elapsed_time))