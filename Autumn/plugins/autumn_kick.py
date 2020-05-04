#!/usr/bin/python
# -------------------------------------------------------------------------
# autumn_kick.py - Kicks a user from an IRC channel.
# Author: Jason Drawdy
# Date: 5.3.20
# Version: 2.0.0 (Mangekyo)
#
# Description:
# Kicks a user from an IRC channel if given OP.
# -------------------------------------------------------------------------

# =======================================
# Imports
# =======================================
from modules import utils
from modules import messages

# =======================================
# Plugin
# =======================================
class Plugin(object):
    def __init__(self, bot, sender, channel):
        self.bot = bot
        self.sender = sender
        self.channel = channel

    # Kick a user from the channel.
    def start(self, *args):
        if self.sender == self.bot.bot_master:
            self.run(args)
        else:
            messages.send_message(self.bot, self.sender + ", I only listen to my master.", self.sender)

    def run(self, *args):
        params = args[0][0][0]
        if len(params) == 0:
            messages.send_message(self.bot, self.sender + ", '!kick' takes a required parameter -- <username> ", self.sender)
        else:
            if len(params) > 1:
                try:
                    username = params[1]
                    self.bot.irc.send(utils.encode("KICK " + self.channel + " " + username + "\n"))
                except:
                    messages.send_message(self.bot, self.sender + ", I can't kick anybody.", self.sender)
            else:
                messages.send_message(self.bot, self.sender + ", '!kick' takes a required parameter - <username>", self.sender)
