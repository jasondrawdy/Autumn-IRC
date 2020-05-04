#!/usr/bin/python
# -------------------------------------------------------------------------
# autumn_torch.py - Allows the master to remotely kill a process.
# Author: Jason Drawdy
# Date: 5.3.20
# Version: 2.0.0 (Mangekyo)
#
# Description:
# This plugin allows a bot master to kill a process remotely from the
# current bot's machine it is running on.
# -------------------------------------------------------------------------

# =======================================
# Imports
# =======================================
from modules import messages

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
            messages.send_message(self.bot, self.sender + ", I only listen to my master.", self.sender)

    def run(self, *args):
        params = args[0][0][0]
        if len(params) == 0:
            messages.send_message(self.bot, self.sender + ", '!torch' takes a required parameter -- <processName> ", self.sender)
        else:
            if len(params) > 1:
                process = params[1]
                self.torch(process)
            else:
                messages.send_message(self.bot, self.sender + ", '!torch' takes a required parameter - <processName>", self.sender)

    def torch(self, name):
        if name:
            try:
                import subprocess, signal, os
                p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
                out, err = p.communicate()
                processes = out.splitlines()
                count = 0
                for process in processes:
                    if str(process).find(name) != -1:
                        count += 1
                        try:
                            pid = int(process.split(None, 1)[0])
                            messages.send_message(self.bot, "\x02Process\x02: " + str(process), self.sender)
                            messages.send_message(self.bot, "\x02PID\x02: " + str(pid), self.sender)
                            os.kill(pid, signal.SIGKILL)
                            messages.send_message(self.bot, "\x0309Process " + str(pid) + " has been terminated.\n", self.sender)
                        except Exception as error:
                            messages.send_message(self.bot, str(error), self.sender)
                if count == 0:
                    messages.send_message(self.bot, "No processes could be found containing the name: \"" + name + "\"", self.sender)
            except Exception as error:
                messages.send_message(self.bot, str(error), self.sender)
        else:
            messages.send_message(self.bot, self.sender + ", '!torch' does not allow null names.", self.sender)
