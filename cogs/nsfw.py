import discord
import aiohttp
import logging

from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from boot.meifwa import MeifwaBot

log = logging.getLogger("NSFW cog")

async def api_call(call_uri, returnObj=False):
	async with aiohttp.ClientSession() as session:
		async with session.get(f"{call_uri}") as response:
			response = await response.json()
			if returnObj == False:
				return response["url"]
			elif returnObj == True:
				return response

class Nsfw(commands.Cog):
    def __init__(self, bot: MeifwaBot):
	    self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.warn(f"{self.__class__.__name__} Cog has been loaded")

    @commands.cooldown(5, 7, commands.BucketType.user)
    @commands.command(name="hentai", description="Yk what it does..")
    async def hentai(self, ctx):
        if ctx.channel.is_nsfw():
            embed = discord.Embed(
                title="Juicy henti for you!",
                color=ctx.message.author.color,
                timestamp=ctx.message.created_at,
            )

            embed.set_footer(
                text=f"Requested by {ctx.message.author.display_name}#{ctx.message.author.discriminator}",
                icon_url=ctx.message.author.avatar.url,
            )
            embed.set_author(
                name=self.bot.user.display_name, icon_url=self.bot.user.avatar.url
            )

            embed.set_image(
                url=await api_call("https://nekos.life/api/v2/img/Random_hentai_gif")
            )
            await ctx.message.reply(embed=embed)
        else:
            embed = discord.Embed(
                title="HoldUp!!",
                description="This command can only be used in a NSFW channel.",
                color=0xFF0000,
                timestamp=ctx.message.created_at,
            )
            await ctx.message.reply(embed=embed, delete_after=20)

    @commands.cooldown(5, 7, commands.BucketType.user)
    @commands.command(name="feet", aliases=["feetgif", "foot"])
    async def feet(self, ctx):
        if ctx.channel.is_nsfw():
            embed = discord.Embed(
                title="***Feet***",
                color=ctx.message.author.color,
                timestamp=ctx.message.created_at,
            )

            embed.set_footer(
                text=f"Requested by {ctx.message.author.display_name}#{ctx.message.author.discriminator}",
                icon_url=ctx.message.author.avatar.url,
            )
            embed.set_author(
                name=self.bot.user.display_name, icon_url=self.bot.user.avatar.url
            )

            embed.set_image(url=await api_call("https://nekos.life/api/v2/img/feetg"))
            await ctx.message.reply(embed=embed)
        else:
            embed = discord.Embed(
                title="HoldUp!!",
                description="This command can only be used in a NSFW channel.",
                color=0xFF0000,
                timestamp=ctx.message.created_at,
            )
            await ctx.message.reply(embed=embed, delete_after=20)

    @commands.cooldown(5, 7, commands.BucketType.user)
    @commands.command(name="cum", description="Yk what it does..")
    async def cum(self, ctx):
        if ctx.channel.is_nsfw():
            embed = discord.Embed(
                title="***Sticky white stuff!***",
                color=ctx.message.author.color,
                timestamp=ctx.message.created_at,
            )
            embed.set_footer(
                text=f"Requested by {ctx.message.author.display_name}#{ctx.message.author.discriminator}",
                icon_url=ctx.message.author.avatar.url,
            )
            embed.set_author(
                name=self.bot.user.display_name, icon_url=self.bot.user.avatar.url
            )
            embed.set_image(url=await api_call("https://nekos.life/api/v2/img/cum"))
            await ctx.message.reply(embed=embed)
        else:
            embed = discord.Embed(
                title="HoldUp!!",
                description="This command can only be used in a NSFW channel.",
                color=0xFF0000,
                timestamp=ctx.message.created_at,
            )
            await ctx.message.reply(embed=embed, delete_after=20)

    @commands.cooldown(5, 7, commands.BucketType.user)
    @commands.command(name="nekofuck", aliases=["nekosex", "nekogif"])
    async def nekofuck(self, ctx):
        if ctx.channel.is_nsfw():
            embed = discord.Embed(
                title="Catgirls!!!!",
                color=ctx.message.author.color,
                timestamp=ctx.message.created_at,
            )
            embed.set_footer(
                text=f"Requested by {ctx.message.author.display_name}#{ctx.message.author.discriminator}",
                icon_url=ctx.message.author.avatar.url,
            )
            embed.set_author(
                name=self.bot.user.display_name, icon_url=self.bot.user.avatar.url
            )
            embed.set_image(
                url=await api_call("https://nekos.life/api/v2/img/nsfw_neko_gif")
            )
            await ctx.message.reply(embed=embed)
        else:
            embed = discord.Embed(
                title="HoldUp!!",
                description="This command can only be used in a NSFW channel.",
                color=0xFF0000,
                timestamp=ctx.message.created_at,
            )
            await ctx.message.reply(embed=embed, delete_after=20)

    @commands.cooldown(5, 7, commands.BucketType.user)
    @commands.command(name="futanari", description="It's basically traps in a way") 
    async def futanari(self, ctx):
        if ctx.channel.is_nsfw():
            embed = discord.Embed(
                title="...",
                color=ctx.message.author.color,
                timestamp=ctx.message.created_at,
            )
            embed.set_footer(
                text=f"Requested by {ctx.message.author.display_name}#{ctx.message.author.discriminator}",
                icon_url=ctx.message.author.avatar.url,
            )
            embed.set_author(
                name=self.bot.user.display_name, icon_url=self.bot.user.avatar.url
            )
            embed.set_image(
                url=await api_call("https://nekos.life/api/v2/img/futanari")
            )
            await ctx.message.reply(embed=embed)
        else:
            embed = discord.Embed(
                title="HoldUp!!",
                description="This command can only be used in a NSFW channel.",
                color=0xFF0000,
                timestamp=ctx.message.created_at,
            )
            await ctx.message.reply(embed=embed, delete_after=20)
    
    @commands.cooldown(5, 7, commands.BucketType.user)
    @commands.command(name="boobs", description="Bondonkers", aliases=["boob"])
    async def boobs(self, ctx):
        if ctx.channel.is_nsfw():
            embed = discord.Embed(
                title="**Tiddies**!!!!!",
                color=ctx.message.author.color,
                timestamp=ctx.message.created_at,
            )
            embed.set_footer(
                text=f"Requested by {ctx.message.author.display_name}#{ctx.message.author.discriminator}",
                icon_url=ctx.message.author.avatar.url,
            )
            embed.set_author(
                name=self.bot.user.display_name, icon_url=self.bot.user.avatar.url
            )
            embed.set_image(url=await api_call("https://nekos.life/api/v2/img/boobs"))

            await ctx.message.reply(embed=embed)
        else:
            embed = discord.Embed(
                title="HoldUp!!",
                description="This command can only be used in a NSFW channel.",
                color=0xFF0000,
                timestamp=ctx.message.created_at,
            )
            await ctx.message.reply(embed=embed, delete_after=20)

    @commands.cooldown(5, 7, commands.BucketType.user)
    @commands.command(name="blowjob", aliases=["bj"])
    async def blowjob(self, ctx):
        if ctx.channel.is_nsfw():
            embed = discord.Embed(
                title="Blow. Job.",
                color=ctx.message.author.color,
                timestamp=ctx.message.created_at,
            )
            embed.set_footer(
                text=f"Requested by {ctx.message.author.display_name}#{ctx.message.author.discriminator}",
                icon_url=ctx.message.author.avatar.url,
            )
            embed.set_author(
                name=self.bot.user.display_name, icon_url=self.bot.user.avatar.url
            )
            embed.set_image(url=await api_call("https://nekos.life/api/v2/img/blowjob"))

            await ctx.message.reply(embed=embed)
        else:
            embed = discord.Embed(
                title="HoldUp!!",
                description="This command can only be used in a NSFW channel.",
                color=0xFF0000,
                timestamp=ctx.message.created_at,
            )
            await ctx.message.reply(embed=embed, delete_after=20)

    @commands.cooldown(5, 7, commands.BucketType.user)
    @commands.command()
    async def pussy(self, ctx):
        if ctx.channel.is_nsfw():
            embed = discord.Embed(
                title="Dang!",
                color=ctx.message.author.color,
                timestamp=ctx.message.created_at,
            )
            embed.set_footer(
                text=f"Requested by {ctx.message.author.display_name}#{ctx.message.author.discriminator}",
                icon_url=ctx.message.author.avatar.url,
            )
            embed.set_author(
                name=self.bot.user.display_name, icon_url=self.bot.user.avatar.url
            )
            embed.set_image(url=await api_call("https://nekos.life/api/v2/img/pussy"))

            await ctx.message.reply(embed=embed)
        else:
            embed = discord.Embed(
                title="HoldUp!!",
                description="This command can only be used in a NSFW channel.",
                color=0xFF0000,
                timestamp=ctx.message.created_at,
            )
            await ctx.message.reply(embed=embed, delete_after=20)

    @commands.cooldown(5, 7, commands.BucketType.user)
    @commands.command()
    async def spank(self, ctx, user: commands.Greedy[discord.Member] = None):
        if ctx.channel.is_nsfw():
            if user == None:
                await ctx.message.reply("Who do you want to spank?")
                return
            spanked_users = "".join([f"{users.mention} " for users in user])
            embed = discord.Embed(
                title="Oooof!",
                description=f"{spanked_users} got spanked by {ctx.author.mention}",
                color=ctx.message.author.color,
                timestamp=ctx.message.created_at,
            )
            embed.set_footer(
                text=f"Requested by {ctx.message.author.display_name}#{ctx.message.author.discriminator}",
                icon_url=ctx.message.author.avatar.url,
            )
            embed.set_author(
                name=self.bot.user.display_name, icon_url=self.bot.user.avatar.url
            )
            embed.set_image(url=await api_call("https://nekos.life/api/v2/img/spank"))
            await ctx.message.reply(embed=embed)
        else:
            embed = discord.Embed(
                title="HoldUp!!",
                description="This command can only be used in a NSFW channel.",
                color=0xFF0000,
                timestamp=ctx.message.created_at,
            )
            await ctx.message.reply(embed=embed, delete_after=20)

    @commands.cooldown(5, 7, commands.BucketType.user)
    @commands.command()
    async def trap(self, ctx):
        if ctx.channel.is_nsfw():
            embed = discord.Embed(
                color=ctx.message.author.color, timestamp=ctx.message.created_at
            )
            embed.set_footer(
                text=f"Requested by {ctx.message.author.display_name}#{ctx.message.author.discriminator}",
                icon_url=ctx.message.author.avatar.url,
            )
            embed.set_author(
                name=self.bot.user.display_name, icon_url=self.bot.user.avatar.url
            )
            embed.set_image(url=await api_call("https://nekos.life/api/v2/img/trap"))
            await ctx.message.reply(embed=embed)
        else:
            embed = discord.Embed(
                title="HoldUp!!",
                description="This command can only be used in a NSFW channel.",
                color=0xFF0000,
                timestamp=ctx.message.created_at,
            )
            await ctx.message.reply(embed=embed, delete_after=20)
        
    @commands.cooldown(5, 7, commands.BucketType.user)
    @commands.command(name="thicc", aliases=["thiccthigh", "animethigh"])
    async def thicc(self, ctx):
        if ctx.channel.is_nsfw():
            embed = discord.Embed(
                title="Thic thighs!",
                color=ctx.message.author.color,
                timestamp=ctx.message.created_at,
            )
            embed.set_footer(
                text=f"Requested by {ctx.message.author.display_name}#{ctx.message.author.discriminator}",
                icon_url=ctx.message.author.avatar.url,
            )
            embed.set_author(
                name=self.bot.user.display_name, icon_url=self.bot.user.avatar.url
            )
            embed.set_image(
                url=await api_call("https://shiro.gg/api/images/nsfw/thighs")
            )
            await ctx.message.reply(embed=embed)
        else:
            embed = discord.Embed(
                title="HoldUp!!",
                description="This command can only be used in a NSFW channel.",
                color=0xFF0000,
                timestamp=ctx.message.created_at,
            )
            await ctx.message.reply(embed=embed, delete_after=20)
    
    @commands.cooldown(3, 7, commands.BucketType.user)
    @commands.command(name="thigh", aliases=["thighs"])
    async def thigh(self, ctx):
        if ctx.channel.is_nsfw():
            response = await api_call("https://nekobot.xyz/api/image?type=thigh", True)
            embed = discord.Embed(
                title="", color=response["color"], timestamp=ctx.message.created_at
            )

            embed.set_footer(
                text=f"Requested by {ctx.message.author.display_name}#{ctx.message.author.discriminator}",
                icon_url=ctx.message.author.avatar.url,
            )
            embed.set_author(
                name=self.bot.user.display_name, icon_url=self.bot.user.avatar.url
            )

            embed.set_image(url=response["message"])
            await ctx.message.reply(embed=embed)
        else:
            embed = discord.Embed(
                title="HoldUp!!",
                description="This command can only be used in a NSFW channel.",
                color=0xFF0000,
                timestamp=ctx.message.created_at,
            )
            await ctx.message.reply(embed=embed, delete_after=20)

    @commands.cooldown(5, 7, commands.BucketType.user)
    @commands.command(name="lesbian")
    async def lesbian(self, ctx):
        if ctx.channel.is_nsfw():
            embed = discord.Embed(
                color=ctx.message.author.color, timestamp=ctx.message.created_at
            )
            embed.set_footer(
                text=f"Requested by {ctx.message.author.display_name}#{ctx.message.author.discriminator}",
                icon_url=ctx.message.author.avatar.url,
            )
            embed.set_author(
                name=self.bot.user.display_name, icon_url=self.bot.user.avatar.url
            )
            embed.set_image(url=await api_call("https://nekos.life/api/v2/img/les"))
            await ctx.message.reply(embed=embed)
        else:
            embed = discord.Embed(
                title="HoldUp!!",
                description="This command can only be used in a NSFW channel.",
                color=0xFF0000,
                timestamp=ctx.message.created_at,
            )
            await ctx.message.reply(embed=embed, delete_after=20)
        
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def erofeet(self, ctx):
        if ctx.channel.is_nsfw():
            embed = discord.Embed(
                title="",
                color=ctx.message.author.color,
                timestamp=ctx.message.created_at,
            )
            embed.set_footer(
                text=f"Requested by {ctx.message.author.display_name}#{ctx.message.author.discriminator}",
                icon_url=ctx.message.author.avatar.url,
            )
            embed.set_author(
                name=self.bot.user.display_name, icon_url=self.bot.user.avatar.url
            )
            embed.set_image(url=await api_call("https://nekos.life/api/v2/img/erofeet"))

            await ctx.message.reply(embed=embed)
        else:
            embed = discord.Embed(
                title="HoldUp!!",
                description="This command can only be used in a NSFW channel.",
                color=0xFF0000,
                timestamp=ctx.message.created_at,
            )
            await ctx.message.reply(embed=embed, delete_after=20) 


def setup(bot):
    bot.add_cog(Nsfw(bot))