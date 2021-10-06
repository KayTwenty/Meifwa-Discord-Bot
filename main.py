import discord
import os
import asyncio
import logging

from discord.ext import commands
from asyncio import sleep

from boot.dbmanagers import PrefixManager
from boot.meifwa import MeifwaBot
from boot.schema import schema

logging.getLogger("main")

def get_prefix(bot: MeifwaBot, msg: discord.Message):
    if not msg.guild or not str(msg.guild.id) in bot.prefixes:
        return commands.when_mentioned_or(bot.get_config("config", "config", "prefix"))(bot, msg)
    return commands.when_mentioned_or(bot.prefixes.get(str(msg.guild.id)))(bot, msg)

bot = MeifwaBot(command_prefix=get_prefix, case_insensitive=True)
pm = PrefixManager(bot=bot)

async def DatabaseInit(Schema: str):
    bot.logger.info("Initializing Database...")
    for i in Schema.split(";;"):
        await bot.db.execute(i)
    bot.logger.info("Schema Execution Complete.")
    bot.logger.info("Attempting To Append Prefixes To On-Memory Cache.")
    try:
        await pm.startup_caching()
    except Exception as e:
        bot.logger.critical(
            f"Error While Appending Guild Prefixes To Database.\nError: {e}\nExiting..."
        )
        exit(code=26)
    bot.logger.info("Guild Prefixes Successfully Appended To On-Memory Cache.")
    bot.logger.info("Database Initialization Complete.")

if not bot.get_config("configoptions", "options", "no_priviledged_owners"):
    for o in bot.get_config("config", "config", "owner_ids"):
        bot.owner_ids.add(o)

async def status(): #Status changer for the bot
    while True:
        await bot.wait_until_ready()
        await bot.change_presence(activity=discord.Streaming(name=";help", url="https://www.youtube.com/watch?v=lQBtXEAAkLU"))
        await sleep(1500)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(";invite"))
        await sleep(1500)
bot.loop.create_task(status())

asyncio.run(DatabaseInit(schema))
bot.logger.info(f"Starting Kurisu with Process ID {os.getpid()}")
bot.run(bot.get_config("config", "config", "token"))