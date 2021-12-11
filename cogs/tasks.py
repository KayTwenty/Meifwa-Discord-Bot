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
        await self.bot.change_presence(activity=discord.Game("Merry Christmas!! 🎄"))
        await sleep(300)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"@{self.bot.user.name} help"))
        await sleep(100)
        await self.bot.change_presence(activity=discord.Game(f"with {len(self.bot.users)} humans!"))
        await sleep(100)
        await self.bot.change_presence(activity=discord.Game(f"in {len(self.bot.guilds)} servers"))
        await sleep(100)
        await self.bot.change_presence(activity=discord.Game("PADORU PADORU!!"))
        await sleep(100)
        
def setup(bot):
    bot.add_cog(Tasks(bot))