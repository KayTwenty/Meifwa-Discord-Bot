from asyncio import sleep

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
        await self.bot.change_presence(activity=discord.Game("Happy New Years!!"))
        await sleep(500)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"@{self.bot.user.name} help"))
        await sleep(500)
        await self.bot.change_presence(activity=discord.Game(f"with {len(self.bot.users)} humans!"))
        await sleep(500)
        await self.bot.change_presence(activity=discord.Game(f"in {len(self.bot.guilds)} servers"))
        await sleep(500)
        await self.bot.change_presence(activity=discord.Game("New Features Added!"))
        await sleep(500)
        
def setup(bot):
    bot.add_cog(Tasks(bot))