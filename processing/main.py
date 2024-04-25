# -*- coding: utf-8 -*-
"""
@author: Cédric Berteletti
Main script for processing the images
"""

import cv2 as cv
from datetime import datetime
import getopt
from importlib import import_module
import numpy as np
import os
import sys

from common_lib import ImageProcessed, write_image


def main(argv):
    errors = []

    # Command line arguments
    opts, args = getopt.getopt(argv[1:],"s:d:i:f:p:", ["source_image_path=", "dest_folder_path=", "dest_image_name=", "format=", "process_id=", "process_script_path=", ])
    print(argv, opts, args)
    for opt, arg in opts:
        if opt in ("-s", "--source_image_path"):
            source_image_path = arg
        elif opt in ("-d", "--dest_folder_path"):
            dest_folder_path = arg
        elif opt in ("-i", "--dest_image_name"):
            dest_image_name = arg
        elif opt in ("-f", "--format"):
            format = arg
        elif opt in ("-p", "--process_id"):
            process_id = arg
        elif opt in ("--process_script_path"):
            process_script_path = arg

    if cv.haveImageReader(source_image_path):
        # Open image with OpenCV
        img = ImageProcessed(cv.imread(source_image_path).astype(np.float32))
        
        source_filename = os.path.basename(source_image_path)
        source_filename_without_ext, source_ext = os.path.splitext(source_filename)
        if not format:
            format = source_ext
        os.makedirs(dest_folder_path, exist_ok=True)
        dest_filename = f"{dest_image_name}.{process_id}.{format}"

        # Calling the proccessing pipeline of the user
        script_folder_path = os.path.dirname(process_script_path)
        script_filename = os.path.basename(process_script_path)
        module_name, script_ext = os.path.splitext(script_filename)
        sys.path.insert(0, script_folder_path)
        custom_module = import_module(module_name)
        process = getattr(custom_module, "process")
        res = process(img)

        return write_image(res, os.path.join(dest_folder_path, dest_filename), format, errors)
    else:
        errors.append(f"{source_image_path} isn't a recognized image format")
        return errors


if __name__ == "__main__":
    start_time = datetime.now()
    errors = main(sys.argv)
    if errors:
        for error in errors:
            print(error)
    elapsed_time = datetime.now() - start_time
