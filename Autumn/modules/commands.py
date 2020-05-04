#!/usr/bin/python
# -------------------------------------------------------------------------
# commands.py - Handles all command logic for Autumn.
# Author: Jason Drawdy
# Date: 5.3.20
# Version: 2.0.0 (Mangekyo)
#
# Description:
# This module controls all commands and how they are processed.
# -------------------------------------------------------------------------

# =======================================
# Imports
# =======================================
from modules import messages
from modules import utils
from modules import logging

#=======================================
# Variables
#=======================================
null = -1

#=======================================
# Classes
#=======================================
class CommandBundle(object):
    def __init__(self, bot, contents, sender, channel=null):
        self.bot = bot
        self.contents = contents
        self.sender = sender
        self.channel = channel

#=======================================
# Functions
#=======================================
def join_server(bot):
    messages.print_message("Connecting to " + bot.server_name + "...", messages.MessageType.GENERAL, True)
    bot.irc.connect((bot.server_name, bot.server_port))
    bot.irc.send(utils.encode("USER " + bot.bot_username + " Ping Pong " + bot.bot_realname + "\n"))
    bot.irc.send(utils.encode("NICK " + bot.bot_nick + "\n"))

def join_channel(bot, channel):
    message = null
    messages.print_message("Joining " + channel + "...", messages.MessageType.GENERAL, True)
    bot.irc.send(utils.encode("JOIN " + channel + "\n"))
    while message.find("End of /NAMES list.") == null:
        message = bot.irc.recv(bot.buffer).decode("UTF-8")
        message = message.strip('\n\r')
        if message.find("PING :") != null:
            if logging.Logger.verbosity_level >= logging.Verbosity.DEBUG:
                messages.print_message(message, messages.MessageType.NOTICE, True)
            pong(message)
        else:
            messages.print_message(message, messages.MessageType.NOTICE, True)

def process_command(bundle):
    # Check if we have an acceptable nick.
    if len(bundle.sender) < 32:
        # Parse our command.
        args = bundle.contents.split(" ")
        c = args[0]

        # Restart the bot if the master says so.
        if c.lower() == "!!restart":
            if bundle.sender == bundle.bot.bot_master:
                utils.restart_program()

        # Continue loading the plugin.
        command = bundle.bot.commands.get(c, null)
        if command != null:
            if isinstance(command, str):
                # Reply to the user or channel
                if bundle.channel is not None:
                    messages.send_message(bundle.bot, command, bundle.channel)
                else:
                    messages.send_message(bundle.bot, command, bundle.sender)
            else:
                # Create a new loader instance and run the plugin with args.
                try:
                    name = args[0].strip(bundle.bot.prefix).lower()
                    args[0] = bundle.sender
                    plugin = utils.Loader(bundle.bot, name, bundle.sender, bundle.channel, args)
                    command.loader = plugin
                    command.sender = bundle.sender
                    command.channel = bundle.channel
                    plugin.start()
                except Exception as error:
                    messages.send_message(bundle.bot, str(error), bundle.sender)
                    if logging.Logger.verbosity_level > logging.Logger.NONE:
                        messages.print_message(str(error), messages.MessageType.EXCEPTION, True)
def iscommand(message):
    # For now there's no real logic until the rewrite.
    return True

def pong(bot, ping):
    reply = ping.split(':')[1]
    bot.irc.send(utils.encode("PONG :" + reply + "\n"))
    if logging.Logger.verbosity_level >= logging.Verbosity.DEBUG:
        messages.print_message("PONG :" + reply, messages.MessageType.GENERAL, True)

def wave_action(bot, target):
    bot.socket.send(utils.encode("PRIVMSG " + target + " :\x01ACTION " + "waves at chat\n"))
