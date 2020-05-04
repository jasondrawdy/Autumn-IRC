#!/usr/bin/python
# -------------------------------------------------------------------------
# autumn_pong.py - Sends a friendly reply to the user.
# Author: Jason Drawdy
# Date: 5.3.20
# Version: 2.0.0 (Mangekyo)
#
# Description:
# Sends a reply to the user who issued the command.
# -------------------------------------------------------------------------

# =======================================
# Imports
# =======================================
from modules import utils

# =======================================
# Plugin
# =======================================
class Plugin(object):
    def __init__(self, bot, sender, channel):
        self.bot = bot
        self.sender = sender
        self.channel = channel
        
    def start(self, *args):
        message = "🏓"
        self.bot.irc.send(utils.encode("PRIVMSG " + self.sender + " :" + message + "\n"))
