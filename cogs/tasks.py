import asyncio
from asyncio import sleep
from asyncio.tasks import Task

from discord.ext import commands, tasks
import discord

from boot.meifwa import MeifwaBot


class Tasks(commands.Cog):
    def __init__(self, bot: MeifwaBot):
        self.bot = bot
        self.status_handler.start()

    @tasks.loop()
    async def status_handler(self):
        await self.bot.wait_until_ready()
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"@{self.bot.user.name} help"))
        await sleep(800)
        await self.bot.change_presence(activity=discord.Streaming(name=";invite", url="https://www.youtube.com/watch?v=eDiu5rk8Mno"))
        await sleep(800)
        await self.bot.change_presence(activity=discord.Game(f"with {len(self.bot.users)} humans!"))
        await sleep(800)
        await self.bot.change_presence(activity=di800d.Game(f"in {len(self.bot.guilds)} guilds"))
        await sleep(800)
        await self.bot.change_presence(activity=discord.Game("Spooktoburr"))
        await sleep(800)
        await self.bot.change_presence(activity=discord.Game("Transfrogmers"))
        await sleep(800)
        await self.bot.change_presence(activity=discord.Game("K-20 rad <3"))
        await sleep(800)
        await self.bot.change_presence(activity=discord.Game("Nyah Nyah"))
        await sleep(800)

def setup(bot):
    bot.add_cog(Tasks(bot))