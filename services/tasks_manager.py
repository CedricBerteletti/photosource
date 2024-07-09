# -*- coding: utf-8 -*-
"""
@author: Cédric Berteletti
Service handling batch processing of the images
"""



import cv2 as cv
import numpy as np
from os import makedirs
from os.path import dirname

import logging
from queue import Queue, Empty
import threading
from time import sleep

from processing.common_io import load_image, write_image
from services.singleton import SingletonMeta


class TasksManager(threading.Thread, metaclass=SingletonMeta):

    def __init__(self):
        super().__init__()
        self.actif = False
        self.tasks = Queue()

    def stop(self):
        logging.info("Stopping the tasks manager")
        self.actif = False

    
    # @synchronized(lock)
    def addTask(self, task):
        logging.info(f"Adding the task {task}")
        self.tasks.put(task)


    def run(self):
        self.actif = True
        logging.info("Starting the tasks manager")
     
        while self.actif:
            try:
                while self.actif:
                    task = self.tasks.get(block=False)
                    logging.info(f"Unstacking the task {task}")
                    self.execute_task(task)
            except Empty:
                sleep(0.1)
                logging.debug("No waiting task")


    def execute_task(self, task):
        if not task.image_state.is_available():
            if not task.image_state.process_id and not task.image_state.preview_id:
                # Resizing of the original image
                logging.info(f"Resizing the image {task.image_state.original_image_path} to {task.image_state.mipmap_path()}  {task.size} {task.image_state.format}")
                self.resize_and_convert(task.image_state.original_image_path, task.image_state.mipmap_path(), task.size, task.image_state.format)
            else:
                # Processing the image
                pass

    
    def resize_and_convert(self, source, destination, size, format):
        if cv.haveImageReader(source):
            # Open image with OpenCV
            img = load_image(source)
            image_size = max(img.shape[0], img.shape[1])
            
            base_dir = dirname(destination)
            makedirs(base_dir, exist_ok=True)

            if size > 0:
                factor = size / image_size
                res = cv.resize(img, (0, 0), fx=factor, fy=factor, interpolation = cv.INTER_CUBIC)
            else:
                res = img

            # Writing image with OpenCV
            errors = []
            write_image(res, destination, format, errors)
            if len(errors) > 0:
                logging.warning(f"Unable to write image {destination}")
                return False
            else:
                return True
        else:
            logging.warning(f"{source} isn't a recognized image format")
            return False