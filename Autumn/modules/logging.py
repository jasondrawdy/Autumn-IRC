#!/usr/bin/python
# -------------------------------------------------------------------------
# logging.py - Handles all remote and local logging.
# Author: Jason Drawdy
# Date: 5.3.20
# Version: 2.0.0 (Mangekyo)
#
# Description:
# Lightweight logging class for handling both networked and local actions.
# -------------------------------------------------------------------------

# =======================================
# Imports
# =======================================
import os
from datetime import datetime

# =======================================
# Classes
# =======================================
class Verbosity:
    NONE = 0 # No logging whatsoever.
    TRACE = 1 # Only logs entry and exit of classes and functions.
    DEFAULT = 2 # Most functions containing logs and important information.
    DEBUG = 3 # Everything that trace does except for all loops and other info.
    ALL = 4 # Literally just logs everything.

class Logger:
    verbosity_level = Verbosity.DEFAULT
    def __init__(self, log_path):
        self.log_path = log_path
        self.log_file = self.get_name() + ".log"
        self.log_location = self.log_path + self.log_file

    def create_entry(self, entry):
        if not os.path.exists(self.log_path):
            os.mkdir(self.log_path)
        file = open(self.log_location, 'a')
        file.write(entry + "\n")
        file.close()

    @staticmethod
    def check_path(path):
        if os.path.isfile(path):
            return True

    def get_name(self):
        date = datetime.now()
        date = date.strftime("%m%d%y")
        name = "log-" + date
        return name
