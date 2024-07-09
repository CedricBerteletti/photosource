# -*- coding: utf-8 -*-
"""
@author: Cédric Berteletti
Service handling mipmaps of images
"""


import services.settings as settings
from services.singleton import SingletonMeta
from services.states.mipmap_level import MipmapLevels, MipmapLevel
from services.states.mipmap_state import MipmapState
from services.tasks_manager import TasksManager
from services.states.task import Task


DEFAULT_IMAGE_FORMAT = "png"


class MipmapService(metaclass=SingletonMeta):

    def __init__(self):
        super().__init__()
        self.mipmapLevels = {}
        self.mipmapLevels[MipmapLevels.VIGNETTE] = MipmapLevel(settings.get("mipmaps.vignette.suffix"), settings.get_int("mipmaps.vignette.size"))
        self.mipmapLevels[MipmapLevels.PREVIEW] = MipmapLevel(settings.get("mipmaps.preview.suffix"), settings.get_int("mipmaps.preview.size"))
        self.mipmapLevels[MipmapLevels.SCREEN] = MipmapLevel(settings.get("mipmaps.screen.suffix"), settings.get_int("mipmaps.screen.size"))

    def mipmap_size(self, mipmap):
        "Return the max pixel dimension of the image for a mipmap level"
        if mipmap == MipmapLevels.FULL:
            return -1
        else:            
            return self.mipmapLevels[mipmap].size

    def image_mipmap(self, image):
        "Return the image mipmap for a specific version of the image (full, preview, vignette, etc.)"        

        mipmap_path = image.mipmap_path()
        if not image.is_available():
            TasksManager().addTask(Task(image, self.mipmap_size(image.mipmap)))
            #self.resize_and_convert(image.original_image_path, mipmap_path, self.mipmapLevels[image.mipmap].size, extension)
            return MipmapState(mipmap_path, loaded=False)
        else:
            return MipmapState(mipmap_path, loaded=True)
    
    
    
