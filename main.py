import aiohttp
import discord
import random
import os
import json
import asyncio
import aiohttp
import rethinkdb as r
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
        await client.change_presence(activity=discord.Streaming(name=";help", url="https://www.youtube.com/watch?v=lQBtXEAAkLU"))
        await sleep(1500)
        await client.change_presence(status=discord.Status.online, activity=discord.Game(";invite"))
        await sleep(1500)

async def _init_rethink():
    r_conn = r.connect(host="127.0.0.1", port=28015, db="meifwa")

@client.event
async def on_ready():
    print("Logged in as: " + client.user.name + "\n")
client.loop.create_task(status())
client.loop.create_task(_init_rethink())

@client.command(name="invite", description="Get a invite link to add me to your server")
async def invite(ctx):

    perms = discord.Permissions.all()

    em = discord.Embed(color=discord.Color.blurple())

    em.set_author(name=client.user.name,
                icon_url=client.user.avatar_url)
    em.set_thumbnail(url=ctx.message.author.avatar_url)
    em.add_field(
        name="Invite Me!",
        inline=False,
        value=f"[Click Here](<{discord.utils.oauth_url(client.user.id, permissions=perms)}>)",
    )
    
    em.set_footer(text=f"{ctx.author}", icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=em)

async def send_cmd_help(ctx):
    return await ctx.send_help(ctx.command)

async def on_command_error(ctx, exception):
    error = getattr(exception, "original", exception)
    if isinstance(error, discord.NotFound):
        return
    elif isinstance(error, discord.Forbidden):
        return
    elif isinstance(error, discord.HTTPException) or isinstance(error, aiohttp.ClientConnectionError):
        return await ctx.send("Failed to get data.")
    if isinstance(exception, commands.NoPrivateMessage):
        return
    elif isinstance(exception, commands.DisabledCommand):
        return
    elif isinstance(exception, commands.BadArgument):
        await client.send_cmd_help(ctx)
    elif isinstance(exception, commands.MissingRequiredArgument):
        await client.send_cmd_help(ctx)
    elif isinstance(exception, commands.CheckFailure):
        await ctx.send("You are not allowed to use that command.", delete_after=5)
    elif isinstance(exception, commands.CommandOnCooldown):
        await ctx.send("Command is on cooldown... {:.2f}s left".format(exception.retry_after), delete_after=5)
    elif isinstance(exception, commands.CommandNotFound):
        return
    return

client.run(TOKEN)