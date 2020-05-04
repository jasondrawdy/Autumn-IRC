#!/usr/bin/python
#-------------------------------------------------------------------------
# main.py - Minimal IRC moderator bot for the Rizon network
# Author: Jason Drawdy
# Date: 5.3.20
# Version: 2.0.0 (Mangekyo)
#
# Description:
# Autumn is a simple IRC bot meant to aid in the moderating of a single
# channel under a single bot master and with minimal interaction/commands.
#-------------------------------------------------------------------------

# =======================================
# Imports
# =======================================
import sys
import socket
import asyncio
import _thread
from bot import Bot
from modules import commands
from modules import logging
from modules import messages

#=======================================
# Variables
#=======================================
# Globals
null = -1
NONE = messages.MessageType.NONE

# Local socket variables.
buffer = 4096
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Local instance of Autumn.
bot = Bot(irc, buffer)

#=======================================
# Classes
#=======================================
class Sentinel(object):
    def __init__(self, bot, path="/plugins"):
        self.bot = bot
        self.path = path

    async def refresh(self, time=1):
        while True:
            self.bot.load_plugins(self.path)
            await asyncio.sleep(time)

    @staticmethod
    async def process(time=1):
        if logging.Logger.verbosity_level > logging.Verbosity.TRACE:
            messages.print_message("Connecting to server...")
        commands.join_server(bot)
        bot.connected = True
        while bot.connected:
            try:
                # Obtain a message from the server/channel.
                message = irc.recv(buffer).decode("UTF-8")
                message = message.strip('\n\r')
                messages.process_message(bot, message)
                await asyncio.sleep(time)
            except Exception as error: # Typically when someone sends an invalid character code.
                messages.print_message(error, messages.MessageType.EXCEPTION)
        messages.print_message("Adiós, mi amor. 🌸")

#=======================================
# Functions
#=======================================
def start_processing():
    if logging.Logger.verbosity_level > logging.Verbosity.TRACE:
        messages.print_message("Processing messages...")
    sentinel = Sentinel(bot)
    asyncio.run(sentinel.process())

def start_processor():
    _thread.start_new_thread(start_processing, ())

def start_resolving():
    if logging.Logger.verbosity_level > logging.Verbosity.TRACE:
        messages.print_message("Loading plugins...")
    sentinel = Sentinel(bot, "plugins")
    asyncio.run(sentinel.refresh())

def start_resolver():
    _thread.start_new_thread(start_resolving, ())

def start_bot():
    if logging.Logger.verbosity_level > logging.Verbosity.DEFAULT:
        messages.print_message("Loading internal commands...")
        for command, obj in bot.commands.items():
            messages.print_message(("Command: %s" % command), messages.MessageType.NONE, False)
    start_processor()

def print_greeting():
    bold = messages.Colors.bold
    reset = messages.Colors.reset
    messages.print_message("===================================", NONE, False)
    messages.print_message("🌙      Welcome to: Autumn!      🌙", NONE, False)
    messages.print_message("===================================", NONE, False)
    messages.print_message("⇢ " + bold + "Author" + reset + ": Jason Drawdy", NONE, False)
    messages.print_message("⇢ " + bold + "Date" + reset + ": 5.3.20", NONE, False)
    messages.print_message("⇢ " + bold + "Version" + reset + ": 2.0.0 (Mangekyo) 🎃", NONE, False)
    messages.print_message("===================================", NONE, False)

#=======================================
# Initialization
#=======================================
def main():
    print_greeting()
    current = sys.path[0]
    sys.path.append(current + "/modules")
    sys.path.append(current + "/plugins")
    if logging.Logger.verbosity_level > logging.Verbosity.DEFAULT:
        messages.print_message("Appending system module paths...")
        for path in sys.path:
            messages.print_message(("Path: %s" % path), NONE, False)
    start_resolver()
    start_bot()
    wait() # Wait for for input since we're multi-threading.
    exit(0) # End the script gracefully.

def wait():
    input()

if __name__ == "__main__":
    main()
