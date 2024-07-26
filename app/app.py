import re
import json
import random
import discord

from pathlib import Path

parent = Path(__file__).resolve().parent

settings = json.load(open(parent.joinpath("settings.json"), 'r'))
token = settings["token"]

dice_pattern = "^\\d{1,2}[D]\\d{1,3}$"
secret_pattern = "^\\d{1,2}[S]\\d{1,3}$"

def pattern(S):
    ptn = re.match(dice_pattern, S)
    if ptn != None:
        ptn = ptn.group(0)
        _ = re.split(r'[D]', ptn)
        return 'D',[int(i) for i in _]

    ptn = re.match(secret_pattern, S)
    if ptn != None:
        ptn = ptn.group(0)
        _ = re.split(r'[S]', ptn)
        return 'S',[int(i) for i in _]

    return None

def diceroll(M,N):
    return [random.randint(1,N) for i in range(M)]

def dice_str(M,N,S):
    res = diceroll(M,N)

    if len(res) > 1:
        return "{:d} ({:s} / {:s})".format(sum(res), ",".join(map(str, res)), S)
    else:
        return "{:d} ({:s})".format(sum(res), S)

class YithDice(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def dice(self, C, N, message):
        if N[0] > 0 and N[1] > 1:
            mes = dice_str(N[0],N[1],message.content)
            await message.reply(mes)

    async def secret_dice(self, C, N, message):
        if N[0] > 0 and N[1] > 1:
            mes = dice_str(N[0],N[1],message.content)
            await message.reply("シークレットダイスを投げます。")
            await message.channel.send(mes)

    async def on_message(self, message):
        if message.author.bot:
            return

        a = pattern(message.content.upper())
        if a[0] == 'D':
            await self.dice(a[0],a[1],message)
        elif a[0] == 'S':
            await self.secret_dice(a[0],a[1],message)

intents = discord.Intents.default()
intents.message_content = True
client = YithDice(intents=intents)
client.run(token)
