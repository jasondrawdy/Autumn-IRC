#!/usr/bin/python
# -------------------------------------------------------------------------
# autumn_leave.py - Leaves an IRC channel.
# Author: Jason Drawdy
# Date: 5.3.20
# Version: 2.0.0 (Mangekyo)
#
# Description:
# This module allows the bot to leave a channel when issued by the master.
# -------------------------------------------------------------------------

# =======================================
# Imports
# =======================================
from modules import messages
from modules import utils

# =======================================
# Variables
# =======================================
null = -1

# =======================================
# Plugin
# =======================================
class Plugin(object):
    def __init__(self, bot, sender, channel):
        self.bot = bot
        self.sender = sender
        self.channel = channel

    def start(self, *args):
        if len(args) == 0:
            messages.send_message(self.bot, self.sender + ", ''!leave' takes a required parameter -- <channel>", self.sender)
        else:
            params = args[0][0]
            channel = params[1]
            if len(params) > 0:
                if self.sender == self.bot.bot_master:
                    try:
                        messages.send_message(self.bot, "Attempting to leave: " + channel, self.sender)
                        self.bot.irc.send(utils.encode("PART " + channel + "\n"))
                        messages.send_message(self.bot, "Left " + channel, self.sender)
                    except Exception as error:
                        messages.send_message(self.bot, "Unable to leave: " + channel, self.sender)
                else:
                    messages.send_message(self.bot, self.sender + ", I only listen to my master.", self.sender)
            else:
                messages.send_message(self.bot, self.sender + ", ''!leave' takes a required parameter -- <channel>", self.sender)
