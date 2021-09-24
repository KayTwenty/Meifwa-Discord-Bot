import discord
import random
import os
import json
import asyncio
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

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

async def status(): #Status changer for the bot
    while True:
        await client.wait_until_ready()
        await client.change_presence(status=discord.Status.online, activity=discord.Game("Prefix: ;"))
        await sleep(1500)
        await client.change_presence(status=discord.Status.online, activity=discord.Game("Version 3.7"))
        await sleep(1500)
        await client.change_presence(status=discord.Status.online, activity=discord.Game("Nya Nya"))
        await sleep(1500)

@client.event
async def on_ready():
    print("Logged in as: " + client.user.name + "\n")
client.loop.create_task(status())




client.run(TOKEN)