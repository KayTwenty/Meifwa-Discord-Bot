import discord
import os
import logging
from discord.ext import commands

log = logging.getLogger("Utility cog")

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        log.warn(f"{self.__class__.__name__} Cog has been loaded")

    @commands.command(name="invite", description="Get a invite link to add me to your server")
    async def invite(self, ctx):

        perms = discord.Permissions.all()

        em = discord.Embed(color=discord.Color.blurple())

        em.set_author(name=self.bot.user.name,
                      icon_url=self.bot.user.avatar_url)
        em.set_thumbnail(url=ctx.message.author.avatar_url)
        em.add_field(
            name="Invite Me!",
            inline=False,
            value=f"[Click Here](<{discord.utils.oauth_url(self.bot.user.id, permissions=perms)}>)",
        )
        
        em.set_footer(text=f"{ctx.author}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=em)

def setup(client):
    client.add_cog(Config(client))