#!/usr/bin/python
# -------------------------------------------------------------------------
# messages.py - Processes all incoming messages from the IRC server.
# Author: Jason Drawdy
# Date: 5.3.20
# Version: 2.0.0 (Mangekyo)
#
# Description:
# This module processes all messages received from the IRC socket and
# directs input and output to the proper functions/modules.
# -------------------------------------------------------------------------

# =======================================
# Imports
# =======================================
from datetime import datetime
from modules import commands
from modules import utils
from modules import logging

#=======================================
# Variables
#=======================================
null = -1

#=======================================
# Classes
#=======================================
class MessageType:
    NONE = 0
    GENERAL = 1
    NOTICE = 2
    SUCCESS = 3
    WARNING = 4
    EXCEPTION = 5

class MessageInfo:
    def __init__(self, message, sender, channel):
        self.message = message
        self.sender = sender
        self.channel = channel

class Colors:
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

    class Foreground:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

    class Background:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'

#=======================================
# Functions
#=======================================
def send_message(bot, message, target):
    bot.irc.send(utils.encode("PRIVMSG " + target + " :" + message + "\n"))

def print_message(message, message_type=MessageType.GENERAL, timestamps=True, log=True):
    data = message
    switch = {
        MessageType.NONE: "" + Colors.reset,
        MessageType.GENERAL: "[" + Colors.Foreground.lightgrey + "-" + Colors.reset + "]: ",
        MessageType.NOTICE: "[" + Colors.Foreground.orange + "i" + Colors.reset + "]: ",
        MessageType.SUCCESS: "[" + Colors.Foreground.green + "+" + Colors.reset + "]: ",
        MessageType.WARNING: "[" + Colors.Foreground.yellow + "!" + Colors.reset + "]: ",
        MessageType.EXCEPTION: "[" + Colors.Foreground.red + "x" + Colors.reset + "]: "
    }
    accent = switch.get(message_type, "")
    if timestamps:
        date = datetime.now()
        timestamp = date.strftime("%A, %d. %B %Y @ %I:%M:%S%p")
        message = "(" + Colors.Foreground.lightgrey + timestamp + Colors.reset + ") " + accent + data
    else:
        message = accent + data

    if log:
        logging.Logger("./log/").create_entry(message)

    message = colorize_message(message)
    print(message)

def colorize_message(message):
    # Text is colorized at different spots.
    x = message
    y = x

    index = x.find("#")
    if index != null:
        channel = x.split()
        for word in channel:
            if "#" in word:
                found = word[word.find("#"):]
                found = found.split('.')[0]
                if found.find(":") == -1:
                    if len(found) > 1:
                        bold = Colors.bold + found + Colors.reset
                        y = y.replace(found, bold)
    if x.find("@"):
        # Highlight the username.
        split = x.split("@")
        for word in split:
            if "!~" in word:
                t = word.split("~")
                username = t[0]
                username = username.split(":")
                username = username[len(username) - 1].replace("!", "")
                color = Colors.Foreground.cyan + username + Colors.reset
                y = y.replace(username, color)
            else:
                pass
                if "!" in word:
                    if ":!" not in word:
                        o = word.split("!")
                        u2 = o[0]
                        u2 = u2.split(":")
                        u2 = u2[len(u2) - 1]
                        color = Colors.bold + u2 + Colors.reset
                        y = y.replace(u2, color)
    # This'll be refactored into a dictionary...
    if x.find(" NOTICE "):
        bold = Colors.bold + " NOTICE " + Colors.reset
        y = y.replace(" NOTICE ", bold)
    if x.find(" PRIVMSG "):
        bold = Colors.bold + " PRIVMSG " + Colors.reset
        y = y.replace(" PRIVMSG ", bold)
    if x.find(" JOIN "):
        bold = Colors.bold + " JOIN " + Colors.reset
        y = y.replace(" JOIN ", bold)
    if x.find(" PART "):
        bold = Colors.bold + " PART " + Colors.reset
        y = y.replace(" PART ", bold)
    if x.find(" LEAVE "):
        bold = Colors.bold + " LEAVE " + Colors.reset
        y = y.replace(" LEAVE ", bold)
    if x.find(" QUIT "):
        bold = Colors.bold + " QUIT " + Colors.reset
        y = y.replace(" QUIT ", bold)
    if x.find(" MODE "):
        bold = Colors.bold + " MODE " + Colors.reset
        y = y.replace(" MODE ", bold)
    if x.find("Autumn"):
        color = Colors.Foreground.lightcyan + "Autumn" + Colors.reset
        y = y.replace("Autumn", color)
    if x.find("Shisui"):
        color = Colors.Foreground.red + "Shisui" + Colors.reset
        y = y.replace("Shisui", color)
    if x.find("PING :"):
        color = Colors.bold + "PING" + Colors.reset + " :"
        y = y.replace("PING :", color)
    if x.find("PONG :"):
        color = Colors.bold + "PONG" + Colors.reset + " :"
        y = y.replace("PONG :", color)
    return y

def process_message(bot, message):
    # Log what the server sent us.
    data = message.strip()
    if data:
        # Check if we should play ping-pong.
        if message.find("PING :") != null:
            if logging.Logger.verbosity_level >= logging.Verbosity.DEBUG:
                print_message(data, MessageType.GENERAL, True)
            commands.pong(bot, message)
            return
        if message.find("QUOTE") != null:
            if logging.Logger.verbosity_level >= logging.Verbosity.DEBUG:
                print_message(data, MessageType.GENERAL, True)
            pong = message.split(" ")[len(message.split(" ")) - 1]
            pong = "PING :" + pong
            commands.pong(bot, pong)
            return
        print_message(data, MessageType.GENERAL, True)
        # Check if we should identify to the network.
        if bot.bot_registered:
            if message.find("Password accepted - you are now recognized") != null:
                print_message("We have connected to the IRC server and successfully logged in.")
            else:
                if message.find("NOTICE") != null:
                    if message.find("This nickname is registered") != null:
                        # print("[!] Sending identify command")
                        bot.irc.send(utils.encode("PRIVMSG NickServ :identify " + bot.bot_password + "\n"))

        # Handle all other messages from the server
        if message.find("PRIVMSG") != null:
            # Split the name of the sender and its message.
            channel = None
            if message.find("#") != null:
                channel = message.split(' ')[2]
            sender = message.split('!', 1)[0][1:]
            contents = message.split('PRIVMSG', 1)[1].split(':', 1)[1]
            if sender == bot.bot_master or sender in bot.friends:
                if commands.iscommand(contents):
                    bundle = commands.CommandBundle(bot, contents, sender, channel)
                    commands.process_command(bundle)
    else:
        bot.irc.close()
        bot.connected = False
        print_message("The socket has been closed.", MessageType.WARNING)
