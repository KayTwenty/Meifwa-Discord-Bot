import discord, asyncio
import aiohttp
import logging
import random

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

async def api_link(call_uri, returnObj=False):
	async with aiohttp.ClientSession() as session:
		async with session.get(f"{call_uri}") as response:
			response = await response.json()
			if returnObj == False:
				return response["link"]
			elif returnObj == True:
				return response

class Nsfw(commands.Cog):
    def __init__(self, bot: MeifwaBot):
	    self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.warn(f"{self.__class__.__name__} Cog has been loaded")


    @commands.command(aliases=['sex', 'fuck'], description="You know what this does") #Frick Command
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
        embed.set_footer(text=f"Command: {ctx.prefix}fuck @mention")
        await ctx.reply(embed=embed)

    @commands.cooldown(5, 7, commands.BucketType.user)
    @commands.command(name="cum", description="Squirts milk")
    async def cum(self, ctx, user: commands.Greedy[discord.Member] = None):
        if ctx.channel.is_nsfw():
            if user == None:
                await ctx.message.reply(f"No cumming for you :)")
                return
            
            cum_users = "".join(f'{users.mention} ' for users in user)
            embed = discord.Embed(
                title="***Sticky white stuff!***",
                description=f"**{ctx.message.author.name}** just cummed to {cum_users}",
                color=ctx.message.author.color,
                timestamp=ctx.message.created_at,
            )
            embed.set_footer(text=f"Command: {ctx.prefix}cum @mention")
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
    @commands.command(name="nekofuck", aliases=["nekosex"], description="Try and see")
    async def nekofuck(self, ctx, user: commands.Greedy[discord.Member] = None):
        if ctx.channel.is_nsfw():
            if user == None:
                await ctx.message.reply(f"U Lonely fuck! U can't Nekofuck yourself :C")
                return
            
            nf_users = "".join(f'{users.mention} ' for users in user)
            embed = discord.Embed(
                title="Better than Hello Kitty",
                description=f"**{ctx.message.author.name}** prentended to be a Neko & fucked {nf_users}",
                color=ctx.message.author.color,
                timestamp=ctx.message.created_at,
            )
            embed.set_footer(text=f"Command: {ctx.prefix}nekofuck @mention")
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
    @commands.command(name="blowjob", aliases=["bj"], description="No It doesn't say PJ")
    async def blowjob(self, ctx, user: commands.Greedy[discord.Member] = None):
        if ctx.channel.is_nsfw():
            if user == None:
                await ctx.message.reply(f"U need to mention someone")
                return
            bj_users = "".join(f'{users.mention} ' for users in user)
            embed = discord.Embed(
                title="Blowjobbed",
                description=f"**{ctx.message.author.name}** sucked {bj_users}",
                color=ctx.message.author.color,
                timestamp=ctx.message.created_at,
            )
            embed.set_footer(text=f"Command: {ctx.prefix}blowjob @mention")
            embed.set_author(
                name=self.bot.user.display_name, icon_url=self.bot.user.avatar.url)
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
    @commands.command(name="spank", description="Spanks a naughty one")
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
            embed.set_footer(text=f"Command: {ctx.prefix}spank @mention")
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
    @commands.command(name="lesbian", description="Romantically Awesome!")
    async def lesbian(self, ctx, user: commands.Greedy[discord.Member] = None):
        if ctx.channel.is_nsfw():
            if user == None:
                await ctx.message.reply("MeNtIoN SoMeOnE")
                return

            lesbian_users = "".join([f"{users.mention} " for users in user])
            embed = discord.Embed(
                title="Oooof!",
                description=f"{lesbian_users} sexed {ctx.author.mention}",
                color=ctx.message.author.color,
                timestamp=ctx.message.created_at,
            )
            embed.set_footer(text=f"Command: {ctx.prefix}lesbian @mention")
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

    @commands.cooldown(5, 7, commands.BucketType.user)
    @commands.command(name="hentai", description="The best command")
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
    @commands.command(name="feet", aliases=["feetgif", "foot"], description="Yk what it does..")
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
    @commands.command(name="pussy", description="It's not a cat command")
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
    @commands.command(name="trap", description="Not a rat trap")
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
    @commands.command(name="thicc", aliases=["thiccthigh", "animethigh"], description="Dreamland command")
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
    @commands.command(name="thigh", aliases=["thighs"], description="Yk what it does..")
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


    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="erofeet", description="Feet in a way")
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


    @commands.command(aliases=["hn"])
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def hentainuke(self, ctx: commands.Context, *, tag: str = None):
        if ctx.channel.is_nsfw():
            available_tags = ["waifu", "neko", "trap", "blowjob"]

            if tag is None:
                tag = random.choice(available_tags)

            if tag is not None and tag.lower() == "list":
                tags = "\n".join(available_tags)
                return await ctx.send(
                    embed=discord.Embed(
                        title="Available Tags",
                        description=tags,
                        color=self.bot.ok_color,
                    )
                )
            if tag is not None and tag.lower() in available_tags:
                async with self.bot.session.post(
                    url=f"https://api.waifu.pics/many/nsfw/{tag}",
                    headers={
                        "Accept": "application/json",
                        "content-type": "application/json",
                    },
                    json={"files": ""},
                ) as resp:
                    step = 5  # the amount of files to display at a time
                    idx = 5  # set the index to start with
                    files = (await resp.json())["files"]
                    while idx < len(files):
                        sublist = files[idx - step : idx]  # [0:5], [5:10], etc
                        await ctx.send("\n".join(map(str, sublist)))
                        idx += step
            else:
                await ctx.send(
                    embed=discord.Embed(
                        title="TAG NOT FOUND",
                        description=f"{tag} was not found in the available tag list. Please run `{ctx.prefix}hb list`",
                        color=self.bot.error_color,
                    )
                )
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