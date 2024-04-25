# -*- coding: utf-8 -*-
"""
@author: Cédric Berteletti
Business class for managing image states and intermediate files
"""

from os import makedirs
from os.path import join, dirname, basename, splitext, isfile

from services.mipmaps import MipmapService, MipmapLevels, DEFAULT_IMAGE_FORMAT
from services.processor import PROCESS_DEFAULT_ID
import services.settings as settings


class ImageState():
    def __init__(self, original_image_path, process_id="", preview_id="", mipmap=MipmapLevels.FULL):
        super().__init__()
        self.original_image_path = original_image_path
        self.process_id = process_id
        self.preview_id = preview_id
        self.preview_name = ""
        self.preview_group = ""
        self.mipmap = mipmap
        self.process_editing = ""
        self.process_result = ""
        
        # Load processing script if exists
        script_path = self.result_script_path()
        if isfile(script_path):
            with open(script_path, "r") as file:
                self.process_result = file.read()

    
    def get_original_basename(self):
        filename_without_ext, ext = splitext(basename(self.original_image_path))
        return filename_without_ext
    

    def get_original_extension(self):
        filename_without_ext, ext = splitext(basename(self.original_image_path))
        return ext
    

    def get_original_folder(self):
        return dirname(self.original_image_path)
    

    def is_available(self):
        return isfile(self.mipmap_path())

    
    def mipmap_path(self, extension=DEFAULT_IMAGE_FORMAT):
        "Return the mipmap path"
        if not self.preview_id and self.mipmap == MipmapLevels.FULL:
            # Original image
            directory = self.get_original_folder()
            ext = self.get_original_extension()
        else:
            directory = self.temp_folder()
            ext = extension
        
        suffix = ""
        if self.process_id:
            suffix += f".{self.process_id}"
        if self.preview_id:
            suffix += f".{self.preview_id}"
        if self.mipmap != MipmapLevels.FULL:
            suffix += f".{MipmapService().mipmapLevels[self.mipmap].name}"

        dest_filename = f"{self.get_original_basename()}{suffix}.{ext}"
        return join(directory, dest_filename)


    def temp_folder(self):
        "Return the temp folder for the original image path"
        base_dir = self.get_original_folder()
        sub_dir = settings.get("temp.folder")
        temp_dir = join(base_dir, sub_dir)
        return temp_dir

    
    def scripts_folder(self):
        "Return the process scripts folder the original image path"
        base_dir = self.get_original_folder()
        sub_dir = settings.get("process.folder")
        script_dir = join(base_dir, sub_dir)
        return script_dir

    
    def result_script_path(self):
        "Return the process scripts folder the original image path"
        folder = self.scripts_folder()
        makedirs(folder, exist_ok=True)
        script_name = f"{self.get_original_basename()}.{PROCESS_DEFAULT_ID}.py"
        script_path = join(folder, script_name)
        return script_path