#!/usr/bin/python
# -------------------------------------------------------------------------
# autumn_hi.py - Sends a friendly hello to the user
# Author: Jason Drawdy
# Date: 5.3.20
# Version: 2.0.0 (Mangekyo)
#
# Description:
# Sends "Hello" to the user who issued the command.
# -------------------------------------------------------------------------

# =======================================
# Imports
# =======================================
from modules import utils

# =======================================
# Plugin
# =======================================
class Plugin:
    def __init__(self, bot, sender, channel):
        self.bot = bot
        self.sender = sender
        self.channel = channel
        
    def start(self, *args):
        self.greet(args)

    def greet(self, args):
        message = "✿ Greetings, love! ✿"
        if self.channel is not None:
            self.bot.irc.send(utils.encode("PRIVMSG " + self.channel + " :" + message + "\n"))
        else:
            self.bot.irc.send(utils.encode("PRIVMSG " + self.sender + " :" + message + "\n"))
