# -*- coding: utf-8 -*-
"""
@author: Cédric Berteletti
Service handling processing of the images
"""


import logging
import os
import shutil

from services.singleton import SingletonMeta
from services.states.image_state import DEFAULT_IMAGE_FORMAT


MAIN_SCRIPT_FILEPATH = os.path.join("processing", "main.py")
PROCESS_DEFAULT_ID = "result"
PROCESS_DEFAULT_TEMPLATE_PATH = os.path.join("processing", "templates", "template_process.py")


VERSION_TAG = "####PHOTOSOURCE VERSION"
TEMPLATE_SECTION = "####PHOTOSOURCE ####USER_COMMANDS_TO_REPLACE####"
LINE_SEP = "\n"


class ProcessorService(metaclass=SingletonMeta):

    def __init__(self):
        super().__init__()

    
    def insert_operations(self, script_path, custom_operations):
        "Edit a script with a template section and replace it with the custom pipeline processing of the user"
        # Read in the file
        filedata = None
        with open(script_path, "r") as file:
            filedata = file.read()

        # Replace the target string - quick and dirty
        operations = custom_operations.split(LINE_SEP)
        lines = filedata.split(LINE_SEP)
        newdata = ""
        for line in lines:
            if TEMPLATE_SECTION not in line:
                newdata = newdata + line + LINE_SEP
            else:
                indentation = line.split(TEMPLATE_SECTION)[0]
                for operation in operations:
                    newdata = newdata + indentation + operation + LINE_SEP

        # Write the file out again
        with open(script_path, "w") as file:
            file.write(newdata)        


    def process(self, source_image_path, temp_folder, dest_folder_path, dest_image_name, process_operations, process_id=PROCESS_DEFAULT_ID, format=DEFAULT_IMAGE_FORMAT):
        logging.info(f"Processing image {source_image_path}")
        
        # Copying the templated processing script to the temp folder
        os.makedirs(temp_folder, exist_ok=True)
        script_name = f"{PROCESS_DEFAULT_ID}.py"
        process_script_path = os.path.join(temp_folder, script_name)
        shutil.copyfile(PROCESS_DEFAULT_TEMPLATE_PATH, process_script_path)

        # Customizing the script
        self.insert_operations(process_script_path, process_operations)

        # Running the script
        command = f"python \"{MAIN_SCRIPT_FILEPATH}\" --source_image_path \"{source_image_path}\" --dest_folder_path \"{dest_folder_path}\" --dest_image_name \"{dest_image_name}\""
        command += f" --format \"{format}\" --process_id \"{process_id}\" --process_script_path \"{process_script_path}\""
        os.system(command)