#!/usr/bin/python
# -------------------------------------------------------------------------
# autumn_join.py - Joins an IRC channel.
# Author: Jason Drawdy
# Date: 5.3.20
# Version: 2.0.0 (Mangekyo)
#
# Description:
# Joins an IRC channel when issued by the master.
# -------------------------------------------------------------------------

# =======================================
# Imports
# =======================================
from modules import messages
from modules import commands
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
        if self.sender == self.bot.bot_master:
            self.run(args)
        else:
            messages.send_message(self.bot, self.sender + ", I only listen to my master. ", self.sender)

    def run(self, args):
        params = args[0][0]
        if len(params) == 0:
            messages.send_message(self.bot, self.sender + ", '!join' takes a required parameter -- <channel> ", self.sender)
        else:
            if len(params) > 1:
                channel = params[1]
                try:
                    joined = self.join(channel)
                    if joined:
                        messages.print_message("Joined " + channel, messages.MessageType.SUCCESS)
                        messages.send_message(self.bot, "Joined " + channel, self.sender)
                except Exception as error:
                    messages.print_message(str(error), messages.MessageType.EXCEPTION)
                    messages.send_message(self.bot, str(error), self.sender)
            else:
                messages.send_message(self.bot, self.sender + ", '!join' takes a required parameter -- <channel> ", self.sender)

    def join(self, channel):
        try:
            messages.print_message("Joining " + channel + "...")
            self.bot.irc.send(utils.encode("JOIN " + channel + "\n"))
            while True:
                message = self.bot.irc.recv(self.bot.buffer).decode("UTF-8")
                message = message.strip('\n\r')
                if message:
                    messages.print_message(message, messages.MessageType.NOTICE)
                    if message.find("End of /NAMES list.") != null:
                        return True
                    if message.find(":Illegal") != null:
                        raise Exception("Could not join: " + channel + " - Illegal channel name.")
                    if message.find("PING :") != null:
                        commands.pong(self.bot, message)
                    if message.find(":Cannot") != null:
                        raise Exception("Could not join: " + channel + " - No invitation was given.")
                else:
                    break
            return True
        except Exception as error:
            raise Exception(error)
