# Autumn-IRC
Autumn is a simple and extensible IRC bot aimed at helping with moderation and user-friendliness. The goal of the bot is to be as accessible, user-friendly, and extensible as possible which is accentuated by asynchronous initialization, multi-threading, and of course dynamic plugin loading. With these features in place it is possible to create an entirely new IRC bot because of the plug-and-play nature of the code.

# Features
- Asynchronous
- Multithreaded
- Event based
- Dynamic plugin loading
- Colorized log output

# Getting Started
When running Autumn for the first time, it will automatically connect to the Rizon IRC network with a random name, so the username of the bot must be changed. Next, if the nick is registered, it is required to create a `.env` file in the root of the project folder called *Autumn*. The two variables that need to be set in the environment file are `AUTUMN-IRC_MASTER` which is the username of the bot owner, and `AUTUMN-IRC_PASSWORD` which is the password of the registered nick the bot will use; and remember to toggle `self.bot_registered` in `bot.py` to `True` if the nick is registered so the bot can identify with the provided nick password.

# Plugins
Currently there are only a handful of plugins for the bot because of simplicity and keeping the codebase fairly small. Most plugins that aren't available can be created from the provided plugin templates. Along with dynamically loaded plugins, the bot also features internal commands which can be modified from  within the `bot.py` file. The commands that already exist are again, very simple such as replying to the bot's name, replying with the sky's color, or even just a friendly hello.

##### Current Plugins:
** Note*: Private commands can only be run by the bot master and nobody else.

| Plugin          | Private   | Description                        |
|-----------------|:---------:|------------------------------------|
| autumn_hi.py    | No        | Sends hello to the sender          |
| autumn_join.py  | Yes       | Joins the specified IRC channel    |
| autumn_kick.py  | Yes       | Kicks a user from the IRC channel  |
| autumn_leave.py | Yes       | Leaves the specified IRC channel   |
| autumn_pong.py  | No        | Sends a ping to the issuer         |
| autumn_test.py  | No        | Sends a test message to the sender |
| autumn_torch.py | Yes       | Kills a process remotely           |

##### Plugin Template:
If you would like to create a plugin for Autumn you can do so by following the structure of the template below. The template is actually fairly straight-forward and easy to follow. The first thing to notice is that the `bot` object, `sender`, and the `channel` if any, are provided to the plugin upon startup. The plugin is also provided any given args and the first real argument can typically be accessed at `args[0][0][0]`. Also, another point to take notice of is since the plugins are dynamically loaded any changes that are saved will be reflected in a nearly real-time state. The final and most important aspect of plugins for the bot is the naming convention. Right now, plugin files need to have the prefix of `autumn_` and then the actual plugin name such as *`hi`* for example; and thus making the name of the file itself `autumn_hi.py` and therefore recognizable by the bot for loading into its dictionary.
```
#!/usr/bin/python

from modules import messages

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
            messages.send_message("PRIVMSG " + self.channel + " :" + message + "\n")
        else:
            messages.send_message("PRIVMSG " + self.sender + " :" + message + "\n")
```

# License
Copyright © ∞ Jason Drawdy

All rights reserved.

The MIT License (MIT)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Except as contained in this notice, the name of the above copyright holder shall not be used in advertising or otherwise to promote the sale, use or other dealings in this Software without prior written authorization.
