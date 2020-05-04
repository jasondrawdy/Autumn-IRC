#!/usr/bin/python
#-------------------------------------------------------------------------
# bot.py - Encapsulation module for information pertaining to Autumn
# Author: Jason Drawdy
# Date: 5.3.20
# Version: 2.0.0 (Mangekyo)
#
# Description:
# This module controls all aspects of the bot itself such as its name and
# other information such as the commands and or the replies it uses.
#-------------------------------------------------------------------------

# =======================================
# Imports
# =======================================
import os
import sys
import random
from importlib import import_module
from pathlib import Path

from dotenv import load_dotenv
from modules import messages
from modules import logging
from modules import utils

#=======================================
# Variables
#=======================================
# Globals
null = -1

#=======================================
# Classes
#=======================================
class PluginInfo:
    def __init__(self, name, checksum, loader, sender, channel=null):
        self.name = name
        self.checksum = checksum
        self.loader = loader
        self.sender = sender
        self.channel = channel

class Bot(object):
    #=======================================
    # Query Information
    #=======================================
    connected = False
    prefix = "!" # The default prefix for Autumn is the exclamation point.
    commands = dict()
    friends = dict()

    def __init__(self, irc, buffer):
        #=======================================
        # Bot Information
        #=======================================
        self.bot_nick = "Autumn" + str(random.randint(1, 10000)) # Change this to your bot's name!
        self.bot_master = None # This is very important - set it in your '.env' file!
        self.bot_username = "Autumn" + str(random.randint(1, 10000)) # Make sure to set this to your bot's username!
        self.bot_realname = "Autumn" + str(random.randint(1, 10000)) # Make sure to set this to your bot's real name!

        # Only change these settings if the bot nick is registered.
        self.bot_registered = False # Make sure to toggle this if the nick is registered!
        self.bot_password = None # Set this in you '.env' file!

        #=======================================
        # Server Information
        #=======================================
        self.irc = irc
        self.buffer = buffer
        self.server_name = "irc.rizon.net"
        self.server_port = 6667
        self.server_channel = "#news"

        #=======================================
        # Command Information
        #=======================================
        # Add the rest of our commands dynamically.
        self.add_default_commands(self.bot_nick)
        self.add_default_friends(self.bot_master)

        # =======================================
        # Environment Information
        # =======================================
        user = False
        password = False
        try:
            current_path = Path('.') / '.env'
            load_dotenv(current_path)
            self.bot_master = os.environ['AUTUMN-IRC_MASTER']
            user = True
            if self.bot_registered:
                self.bot_password = os.environ['AUTUMN-IRC_PASSWORD']
                password = True
        except KeyError:
            if self.bot_registered:
                if not user and not password:
                    print("Please set the environment variables 'AUTUMN-IRC_MASTER' and 'AUTUMN-IRC_PASSWORD'")
                elif not user:
                    print("Please set the environment variable 'AUTUMN-IRC_MASTER'")
                elif not password:
                    print("Please set the environment variable 'AUTUMN-IRC_PASSWORD'")
            else:
                if not user:
                    print("Please set the environment variable 'AUTUMN-IRC_MASTER'")
                elif not password:
                    print("Please set the environment variable 'AUTUMN-IRC_PASSWORD'")
            sys.exit(1)

    def add_default_friends(self, master):
        self.friends[master                   ] = "Master"
        self.friends["Autumn"                 ] = "Self"
        #self.friends["Photon"                 ] = "Friend"

    def add_default_commands(self, name):
        self.commands[name                   ] = "❔"
        self.commands[Bot.prefix + "ping"    ] = "pong!"
        self.commands[Bot.prefix + "dance"   ] = "But, I don't know how..."
        self.commands[Bot.prefix + "color"   ] = "The sky is blue, dude!"
        self.commands[Bot.prefix + "fox"     ] = "Don't worry, I don't bite..."

    def check_plugins(self, path):
        # Obtain only Autumn plugin files.
        files = os.listdir(path)
        for file in files:
            if file.find(".py") != null:
                if file.find("autumn_") == null:
                    utils.remove_key(files, file)
            else:
                utils.remove_key(files, file)

        # Parse them as commands.
        for i in range(len(files)):
            files[i] = self.prefix + files[i][7:-3]

        # Check the bots' list of commands against what we found.
        commands = self.commands
        plugins = dict()
        for command in commands:
            instance = commands.get(command, null)
            if instance != null:
                if isinstance(instance, str):
                    plugins[command] = instance
                else:
                    if command in files:
                        plugins[command] = instance
                    else:
                        pass # Can't edit the dict while iterating..
            else:
                pass
        self.commands = plugins

    def load_plugins(self, path):
        self.check_plugins(path)
        plugins = os.listdir(path)
        for plugin in plugins:
            if plugin.find(".py") != null:
                if plugin.find("autumn_") != null:
                    name = plugin[7:-3] # Remove "autumn_" and ".py" from the filename
                    command = self.prefix + name
                    loader = utils.Loader(self, name, null, null)
                    module = self.commands.get(command, null)
                    if module != null:
                        # Reload the module
                        try:
                            filename = Path("./plugins/autumn_" + name + ".py")
                            checksum = utils.get_checksum(filename)
                            if checksum != module.checksum:
                                module.checksum = checksum
                                module = import_module("plugins.autumn_" + name)
                                loader.reload_plugin(module)
                                if logging.Logger.verbosity_level > logging.Verbosity.TRACE:
                                    messages.print_message("Plugin reloaded - " + plugin, messages.MessageType.NOTICE)
                        except:
                            utils.removekey(self.commands, command)
                            if logging.Logger.verbosity_level > logging.Verbosity.TRACE:
                                messages.print_message(plugin + " has been unloaded", messages.MessageType.NOTICE)
                    else:
                        try:
                            # Make a PluginInfo and toss it into the commands dictionary.
                            checksum = utils.get_checksum("./plugins/autumn_" + name + ".py")
                            info = PluginInfo(name, checksum, loader, null, null)
                            self.commands[command] = info
                            if logging.Logger.verbosity_level > logging.Verbosity.TRACE:
                                messages.print_message("Plugin loaded - " + plugin, messages.MessageType.NOTICE)
                                messages.print_message("Checksum: " + checksum)
                        except Exception as error:
                            messages.print_message(plugin + " could not be loaded.", messages.MessageType.WARNING)
