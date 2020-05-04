#!/usr/bin/python
# -------------------------------------------------------------------------
# autumn_test.py - Sends a friendly test message to the user.
# Author: Jason Drawdy
# Date: 5.3.20
# Version: 2.0.0 (Mangekyo)
#
# Description:
# Sends a test message to the user who issued the command.
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
        message = "Test module ∞ ⚭ ☨⚛︎ 🍪🍩🎂🍦🍕🍔🍟🥞🥓🥥🍓🍒🍑🍎🥝🌶🥒🥚🍏🍋🍉🍇🍅🥦🥨🍜🌮🍯🥂"
        self.bot.irc.send(utils.encode("PRIVMSG " + self.sender + " :" + message + "\n"))
