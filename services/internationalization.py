# -*- coding: utf-8 -*-
"""
@author: Cédric Berteletti
Service handling internationalization of the application
"""

import configparser

def init(language):
    global internationalization
    internationalization = configparser.ConfigParser(inline_comment_prefixes="#")
    internationalization.read(f"labels.{language}.ini")

def l(str):
    global internationalization
    return internationalization.get("DEFAULT", str)