
# -*- coding: utf-8 -*-
"""
@author: Cédric Berteletti
Script for :
- increase saturation and brightness of a photo
"""

import cv2 as cv
from datetime import datetime 
import getopt
import numpy as np
import os
import shutil
import sys
from wand.image import Image

PHOTOSOURCE_LOCAL_TEMP_DIRECTORY = ".photosource"
PHOTOSOURCE_FORMAT_SUFFIX_EXR = ""
PHOTOSOURCE_FORMAT_SUFFIX_SRGB = ".srgb"
PHOTOSOURCE_FORMAT_SUFFIX_LINEAR_RGB = ".rgb"


verbose = False

nbSelected = 0
nbProcessed = 0
nbWarnings = 0
nbErrors = 0


def print_help():
    print(f"Invalid arguments")
    sys.exit()

def warning(str):
    global nbWarnings
    print("WARNING: " + str)
    nbWarnings += 1

def error(str):
    global nbErrors
    print("ERROR: " + str)
    nbErrors += 1

def main(argv):
    global nbSelected
    global verbose
    source_path = ""
    destination_path = ""

    # Command line arguments
    opts, args = getopt.getopt(argv,"hvs:d:",["help", "verbose", "source_path=", "destination_path="])
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_help()
        elif opt in ("-v", "--verbose"):
            verbose = True

        elif opt in ("-s", "--source_path"):
            source_path = arg
        elif opt in ("-d", "--destination_path"):
            destination_path = arg


    if not source_path or not destination_path:
        print_help()
    
    if verbose:
        print(f"Source path: {source_path}")
        print(f"Destination path: {destination_path}")

    if os.path.isdir(source_path):
        if os.path.isdir(destination_path):
            process_files_in_path(source_path, destination_path)
        elif os.path.isfile(destination_path):
            print_help()
        else:
            print_help()
    elif os.path.isfile(source_path):
        if os.path.isdir(destination_path):            
            source_filename = os.path.basename(source_path)
            destination_file_path = os.path.join(destination_path, source_filename)
            nbSelected += 1
            process_file(source_path, destination_file_path)
        else:
            nbSelected += 1
            process_file(source_path, destination_path)
    else:
        print_help()


def process_files_in_path(source_path, destination_path):
    global nbSelected
    for path, subdirs, files in os.walk(source_path):
        for filename in files:
            nbSelected += 1
            source_file_path = os.path.join(path, filename)
            relative_path = os.path.relpath(path, source_path)
            destination_file_path = os.path.join(destination_path, relative_path, filename)
            os.makedirs(os.path.join(destination_path, relative_path), exist_ok=True)
            process_file(source_file_path, destination_file_path)


def filepath_temp_suffix(file_path, temp_dir="", suffix="", extension=""):
    filename = os.path.basename(file_path)
    filename_without_ext, ext = os.path.splitext(filename)
    base_dir = os.path.dirname(file_path)
    
    dest_dir = os.path.join(base_dir, temp_dir)
    os.makedirs(dest_dir, exist_ok=True)
    if extension:
        ext = extension
    dest_filename = filename_without_ext
    dest_filename += f".{suffix}"
    dest_filename += f".{ext}"

    return os.path.join(dest_dir, dest_filename)

def process_file(source_file_path, destination_file_path):
    process_file_opencv(source_file_path, destination_file_path)


def process_file_opencv(source_file_path, destination_file_path):
    global nbProcessed
    if cv.haveImageReader(source_file_path):
        if verbose:
            print(f"Converting image {source_file_path} to {destination_file_path}")

        # Ouverture image avec OpenCV
        cv_rgb = cv.imread(source_file_path).astype(np.float32)
        image_size = max(cv_rgb.shape[0], cv_rgb.shape[1])

        cv_hsv = cv_rgb_to_hsv(cv_rgb)
        cv_hsv = filter_opencv(cv_hsv)
        res = cv_hsv_to_rgb(cv_hsv)

        # Enregistrment image avec OpenCV
        if not cv.imwrite(destination_file_path, res, [cv.IMWRITE_JPEG_QUALITY, 100]):
            error(f"Unable to write image {destination_file_path}")
            return False
        nbProcessed += 1
    else:
        warning(f"{source_file_path} isn't a recognized image format : copying the raw file without conversion")
        shutil.copy2(source_file_path, destination_file_path)
        return False
    return True


def cv_rgb_to_hsv(cv_rgb):
    return cv.cvtColor(cv_rgb, cv.COLOR_RGB2HSV) #.astype(np.float32)

def cv_hsv_to_rgb(cv_hsv):
    return cv.cvtColor(cv_hsv, cv.COLOR_HSV2RGB) #.astype(np.float32)

def filter_opencv(cv_hsv):
    (h, s, v) = cv.split(cv_hsv)
    s = s * 1.2
    # s = np.clip(s, 0, 255)
    res = cv.merge([h,s,v])
    return res




if __name__ == "__main__":
    start_time = datetime.now()
    main(sys.argv[1:])
    elapsed_time = datetime.now() - start_time
    print('Elapsed time (hh:mm:ss.ms) {}'.format(elapsed_time))
    print(f"Nb files selected: {nbSelected}")
    print(f"Nb files processed: {nbProcessed}")
    print(f"Nb warnings: {nbWarnings}")
    print(f"Nb errors: {nbErrors}")






## Archives
    


def process_file_wand(source_file_path, destination_file_path):
    global nbProcessed
    if cv.haveImageReader(source_file_path):
        if verbose:
            print(f"Converting image {source_file_path} to {destination_file_path}")

        # Ouverture image avec OpenCV
        # img = cv.imread(source_file_path).astype(np.float32)
        # image_size = max(img.shape[0], img.shape[1])

        # Ouverture image avec ImageMagick
        with Image(filename=source_file_path) as img:
            if verbose:
                print(f"Type: {img.type}")
                print(f"Color space: {img.colorspace}")
                print(f"Format: {img.format}")

            # TODO
            #img_cv = filter_opencv(img_cv)
                
            write_file_formats(source_file_path)
            
            res = img
            #write_linear_exr(img, f"{destination_file_path}.exr")
                
            
            #img_cv = wand_to_cv_hsv(img)
            #img_cv = filter_opencv(img_cv)
            #res = cv_hsv_to_wand(img_cv)

            # Enregistrment image avec ImageMagick
            res.save(filename=destination_file_path)

            nbProcessed += 1

            

        # Enregistrment image avec OpenCV
        # if not cv.imwrite(destination_file_path, img, [cv.IMWRITE_JPEG_QUALITY, 100]):
        #     error(f"Unable to write image {destination_file_path}")
        #     return False
    else:
        warning(f"{source_file_path} isn't a recognized image format : copying the raw file without conversion")
        shutil.copy2(source_file_path, destination_file_path)
        return False
    return True

def write_file_formats(source_file_path):
    os.system(f"magick \"{source_file_path}\" -colorspace sRGB -define quantum:format=floating-point \"{filepath_temp_suffix(source_file_path, PHOTOSOURCE_LOCAL_TEMP_DIRECTORY, "srgb", "tif")}\" ")
    os.system(f"magick \"{source_file_path}\" -colorspace RGB -define quantum:format=floating-point \"{filepath_temp_suffix(source_file_path, PHOTOSOURCE_LOCAL_TEMP_DIRECTORY, "rgb", "tif")}\" ")
    #os.system(f"magick \"{source_file_path}\" -colorspace sRGB -profile \"%MAGICK_HOME%\\sRGB.icc\" -define quantum:format=floating-point \"{filepath_temp_suffix(source_file_path, PHOTOSOURCE_LOCAL_TEMP_DIRECTORY, "srgb", "tif")}\" ")
    #os.system(f"magick \"{source_file_path}\" -profile \"%MAGICK_HOME%\\sRGB.icc\" -colorspace RGB -colorspace sRGB -define quantum:format=floating-point \"{filepath_temp_suffix(source_file_path, PHOTOSOURCE_LOCAL_TEMP_DIRECTORY, "rgb", "tif")}\" ")
    # os.system(f"magick \"{source_file_path}\" -colorspace sRGB \"{filepath_temp_suffix(source_file_path, PHOTOSOURCE_LOCAL_TEMP_DIRECTORY, "srgb", "jpg")}\" ")
    # os.system(f"magick \"{source_file_path}\" -colorspace RGB -colorspace sRGB \"{filepath_temp_suffix(source_file_path, PHOTOSOURCE_LOCAL_TEMP_DIRECTORY, "rgb", "jpg")}\" ")
    # os.system(f"magick \"{source_file_path}\" -colorspace sRGB \"{filepath_temp_suffix(source_file_path, PHOTOSOURCE_LOCAL_TEMP_DIRECTORY, "srgb", "exr")}\" ")
    # os.system(f"magick \"{source_file_path}\" -colorspace RGB -colorspace sRGB \"{filepath_temp_suffix(source_file_path, PHOTOSOURCE_LOCAL_TEMP_DIRECTORY, "rgb", "exr")}\" ")

def clear_file_formats(source_file_path):

    pass

def write_linear_exr(img_wand, destpath):
    conv = img_wand.clone()
    conv = conv.convert("exr")
    conv.transform_colorspace("rgb")
    conv.save(filename=destpath)


def wand_to_cv_hsv(img_wand):
    conv = img_wand.convert("tif")
    conv.alpha_channel = False # was not required for me, including it for completion
    img_array = np.asarray(bytearray(conv.make_blob())) # , dtype=np.uint8 #float32
    print(img_array.size)
    print(conv.size[0])
    print(conv.size[1])
    #n_channels = img_array.size / img_wand.size[0] / img_wand.size[1]
    #img_array = img_array.reshape(img_wand.size[0], img_wand.size[1], int(n_channels))
    #img_array = img_array.reshape(img.size[0], img.size[1])

    if img_array is not None:
        img_cv_rgb = cv.imdecode(img_array, cv.IMREAD_UNCHANGED).astype(np.float32)
    print(img_cv_rgb.size)
    # cv.imshow("Color image", img_cv_rgb)
    # cv.waitKey(0)

    return cv.cvtColor(img_cv_rgb, cv.COLOR_BGR2HSV)

def cv_hsv_to_wand(img_cv_hsv):
    img_cv_rgb = cv.cvtColor(img_cv_hsv, cv.COLOR_HSV2RGB).astype(np.uint8)
    img_wand = Image.from_array(img_cv_rgb)
    return img_wand