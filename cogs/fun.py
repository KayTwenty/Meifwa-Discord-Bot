import discord, asyncio
import aiohttp
import random
import logging
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

from boot.meifwa import MeifwaBot

class fun(commands.Cog):
    def __init__(self, bot: MeifwaBot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
    
    def cog_unload(self):
        del self.session

    @commands.command(aliases=['sex', 'fuck']) #Frick Command
    async def frick(self, ctx, member: discord.Member):
        embed = discord.Embed(title=f"{ctx.message.author.name} wants to fuck you. Do you accept?", description="Type yes or no.", color=self.bot.error_color, timestamp=ctx.message.created_at)
        embed.set_author(name=ctx.message.author.display_name, icon_url=self.bot.user.avatar.url)
        await ctx.send(embed=embed)
        
        try:
            msg = await self.bot.wait_for("message", check=lambda x: x.channel == ctx.message.channel and x.author == member, timeout=60.0)
            if msg.content.lower() != "yes":
                return await ctx.send(f"**{member.name} declined** :|")
        except asyncio.TimeoutError:
            return await ctx.send("**Cancelled.**")
         
        embed = discord.Embed(title="This person had sex with you ;)", description="**{1}** fucked **{0}**!".format(member.name, ctx.message.author.name), color=ctx.message.author.color, timestamp=ctx.message.created_at)
        embed.set_author(name="Fucked by " + str(ctx.message.author), icon_url=ctx.message.author.avatar.url)
        embed.set_image(url="https://media1.tenor.com/images/fa98b23ca1dba1925da62f834f27153f/tenor.gif?itemid=19355212")
        embed.set_footer(text="Command: ;fuck @user")
        await ctx.reply(embed=embed)

    @commands.command(name="invite", description="Get a invite link to add me to your server")
    async def invite(self, ctx):
        perms = discord.Permissions.all()

        em = discord.Embed(color=discord.Color.blurple())

        em.set_author(name=self.bot.user.name,
                    icon_url=self.bot.user.avatar.url)
        em.set_thumbnail(url=ctx.message.author.avatar_url)
        em.add_field(
            name="Invite Me!",
            inline=False,
            value=f"[Click Here](<{discord.utils.oauth_url(self.bot.user.id, permissions=perms)}>)",
        )

        em.set_footer(text=f"{ctx.author}", icon_url=ctx.message.author.avatar.url)
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(fun(bot))