import re
import json
import random
import discord

from pathlib import Path

parent = Path(__file__).resolve().parent

settings = json.load(open(parent.joinpath("settings.json"), 'r'))
token = settings["token"]
pattern = settings["pattern"]

dice_pattern = re.compile(pattern)

class YithDice(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
    async def on_message(self, message):
        if message.author.bot:
            return

        ptn = re.match(dice_pattern, message.content)
        if ptn != None:
            ptn = ptn.group(0)
            _ = re.split(r'[Dd]', ptn)
            M = int(_[0])
            N = int(_[1])
            if M > 0 and N > 1:
                res = [random.randint(1,N) for i in range(M)]
                mes = ""
                if len(res) > 1:
                    mes = "{:d} ({:s} / {:s})".format(sum(res), ",".join(map(str, res)), message.content)
                else:
                    mes = "{:d} ({:s})".format(sum(res), message.content)
                await message.channel.send(mes)

intents = discord.Intents.default()
intents.message_content = True
client = YithDice(intents=intents)
client.run(token)
