import aiohttp
import discord
import random
import os
import json
import asyncio
import aiohttp
from asyncio import sleep
from discord.ext import commands

if os.path.exists(os.getcwd() + "/data/config.json"):
    with open("./data/config.json") as f:
        configData = json.load(f)
else:
    configTemplate = {"Token": "", "Prefix": ";"}
    with open(os.getcwd() + "/data/config.json", "w+") as f:
        json.dump(configTemplate, f)

TOKEN = configData["Token"]
BOT_PREFIX = configData["Prefix"]

client = commands.Bot(command_prefix = BOT_PREFIX, case_insensitive=True)
client.remove_command('help')


async def status(): #Status changer for the bot
    while True:
        await client.wait_until_ready()
        await client.change_presence(activity=discord.Streaming(name=";help", url="https://www.youtube.com/watch?v=lQBtXEAAkLU"))
        await sleep(1500)
        await client.change_presence(status=discord.Status.online, activity=discord.Game(";invite"))
        await sleep(1500)


client.run(TOKEN)