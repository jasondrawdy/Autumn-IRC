#!/usr/bin/python
# -------------------------------------------------------------------------
# utils.py - Contains tools for encoding, encrypting, and others.
# Author: Jason Drawdy
# Date: 5.3.20
# Version: 2.0.0 (Mangekyo)
#
# Description:
# This module contains tools for versioning, encoding, encryption and
# other utilities that may be used during the bots' IRC session.
# -------------------------------------------------------------------------

# =======================================
# Imports
# =======================================
import os
import sys
import importlib
from importlib import import_module
from modules import logging
from modules import messages

#=======================================
# Classes
#=======================================
class Loader:
    def __init__(self, bot, plugin, sender, channel, args=None):
        if args is None:
            args = []
        self.bot = bot
        self.plugin = plugin
        self.sender = sender
        self.channel = channel
        self.args = args

    def start(self):
        try:
            if logging.Logger.verbosity_level >= logging.Verbosity.DEFAULT:
                messages.print_message("Running '" + self.plugin + "' for %s" % self.sender, messages.MessageType.NOTICE)
            self.start_plugin(self.plugin, self.args)
        except Exception as exception:
            if self.channel is not None:
                messages.send_message(self.bot, "That plugin cannot be activated at the moment.", self.channel)
            else:
                messages.send_message(self.bot, "That plugin cannot be activated at the moment.", self.sender)

    @staticmethod
    def load_plugin(name):
        module = import_module("plugins.autumn_%s" % name)
        return module

    @staticmethod
    def reload_plugin(module):
        importlib.reload(module)

    def start_plugin(self, name, *args):
        self.plugin = self.load_plugin(name)
        plugin = self.plugin.Plugin(self.bot, self.sender, self.channel)
        plugin.start(args)

#=======================================
# Functions
#=======================================
def insert(source_str, insert_str, pos):
    return source_str[:pos]+insert_str+source_str[pos:]

def encode(data):
    version = check_version()
    if version is not None:
        try:
            if check_version():
                return bytes(data, "UTF-8")
            else:
                return bytes(data)
        except:
            raise Exception("The provided input could not be encoded.")
    else:
        raise Exception("The current version of Python could not be determined.")

def check_version():
    version = sys.version_info[0]
    if version >= 3:
        return True # Python 3
    else:
        return False # Python 2

def get_checksum(filename, block=2**20):
    import hashlib
    hashing = hashlib.md5()
    try:
        file = open(filename, 'rb')
        while True:
            data = file.read(block)
            if not data:
                break
            hashing.update(data)
    except IOError:
        if logging.Logger.verbosity_level >= logging.Verbosity.DEBUG:
            messages.print_message("File \'" + filename + "\' not found!", messages.MessageType.NONE, False)
        return None
    except Exception as error:
        return None
    return hashing.hexdigest()

def remove_key(dictionary, key):
    index = 0
    for item in dictionary:
        if item == key:
            try:
                del dictionary[index]
                break
            except Exception as error:
                break
        index += 1

def restart_program():
    # Restarts the current program, with file objects and descriptors cleanup
    python = sys.executable
    os.execl(python, python, *sys.argv)
