import aiohttp
import discord, asyncio
import logging
from random import randint
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from .utils import helpers

log = logging.getLogger("actions cog")

async def api_call(call_uri, state=True):
	async with aiohttp.ClientSession() as session:
		async with session.get(f"{call_uri}") as response:
			response = await response.json()
			if state:
				return response['url']
			if state == False:
				return response

class neko(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        log.warn(f"{self.__class__.__name__} Cog has been loaded")

    @commands.command(name="purr", description="Pics of Catgirls (old command)")
    async def purr(self, ctx):
        num = randint(1, 15)
        try:
            await ctx.reply(file = discord.File("data/Pic/{}.jpg".format(num)))
        except:
            await ctx.reply(file = discord.File("data/Pic/{}.gif".format(num)))

    @commands.cooldown(3, 5, commands.BucketType.user)
    @commands.command(name="poke", description="Get poked!11!!")
    async def poke(self, ctx, user: commands.Greedy[discord.Member] = None):
        if user == None:
            await ctx.message.reply(f"Why are you so lonely? Mention someone that you wanna poke, you can't poke yourself :(")
            return

        if user == ctx.author:
            await ctx.message.reply("Imagine poking yourself... why are you so lonely?")
            return
        poke_users = "".join(f'{users.mention} ' for users in user)
        embed = discord.Embed(
            title="***Poke poke***",
            description=f"**{ctx.message.author.name}** just poked {poke_users}",
            color=ctx.message.author.color,
            timestamp=ctx.message.created_at,
        )
        embed.set_image(url=await api_call("https://nekos.life/api/v2/img/poke"))
        embed.set_author(
                name=ctx.message.author.display_name,
                icon_url=self.client.user.avatar_url,
            )
        await ctx.reply(embed=embed)

    @commands.cooldown(3, 5, commands.BucketType.user)
    @commands.command(name="pat", description="Pat someone")
    async def pat(self, ctx, user: commands.Greedy[discord.Member] = None):
        if user == None:
            await ctx.message.reply(f"Mention someone you wanna pat ;)")
            return

        if user == ctx.author:
            await ctx.message.reply("Imagine patting yourself...")
            return
        pat_users = "".join(f'{users.mention} ' for users in user)
        embed = discord.Embed(
            title="*Cute pats*",
            description=f"**{ctx.message.author.name}** just patted {pat_users}",
            color=ctx.message.author.color,
            timestamp=ctx.message.created_at,
        )
        embed.set_image(url=await api_call("https://nekos.life/api/v2/img/pat"))
        embed.set_author(
                name=ctx.message.author.display_name,
                icon_url=self.client.user.avatar_url,
            )
        await ctx.reply(embed=embed)

    @commands.cooldown(3, 5, commands.BucketType.user)
    @commands.command(name="baka", description="YOU ARE A BAKA!!!!")
    async def baka(self, ctx, user: commands.Greedy[discord.Member] = None):
        if user == None:
            await ctx.message.reply(f"Who tf are you calling a baka?")
            return
        bakas = "".join(f'{users.mention} ' for users in user)
        embed = discord.Embed(
            title="**BAKA!!**",
            description=f"{bakas}, Hehe Sussy Baka!",
            color=ctx.message.author.color,
            timestamp=ctx.message.created_at,
        )
        embed.set_image(url=await api_call("https://nekos.life/api/v2/img/baka"))
        embed.set_author(
                name=ctx.message.author.display_name,
                icon_url=self.client.user.avatar_url,
            )
        await ctx.reply(embed=embed)

    @commands.cooldown(3, 5, commands.BucketType.user)
    @commands.command(name="lick", description="Lick someone")
    async def lick(self, ctx, user: commands.Greedy[discord.Member] = None):
        if user == None:
            await ctx.message.reply(f"Mention someone you wanna lick ;)")
            return
        licked_users = "".join(f'{users.mention} ' for users in user)
        embed = discord.Embed(
            title="*Slurp Slurp!*",
            description=f"**{ctx.message.author.name}** just licked {licked_users}",
            color=ctx.message.author.color,
            timestamp=ctx.message.created_at,
        )
        response = await api_call("http://api.nekos.fun:8080/api/lick", state=False)
        embed.set_image(url=response['image'])
        embed.set_author(
                name=ctx.message.author.display_name,
                icon_url=self.client.user.avatar_url,
            )
        await ctx.reply(embed=embed)

    @commands.cooldown(3, 5, commands.BucketType.user)
    @commands.command(name="hug", description="Hug someone UwU")
    async def hug(self, ctx, user: commands.Greedy[discord.Member] = None):
        if user == None:
            await ctx.message.reply(f"Awww you poor thing... ;0")
            return
        hugged_users = "".join(f'{users.mention} ' for users in user)
        embed = discord.Embed(
            title="Aww hugs uwu",
            description=f"**{ctx.message.author.name}** just hugged {hugged_users}",
            color=ctx.message.author.color,
            timestamp=ctx.message.created_at,
        )
        embed.set_image(url=await api_call("https://nekos.life/api/v2/img/hug"))
        embed.set_author(
                name=ctx.message.author.display_name,
                icon_url=self.client.user.avatar_url,
            )
        await ctx.reply(embed=embed)
    
    @commands.cooldown(3, 5, commands.BucketType.user)
    @commands.command(name="kiss", description="OwO Kiss someone :flushed:")
    async def kiss(self, ctx, user: commands.Greedy[discord.Member] = None):
        if user == None:
            await ctx.message.reply(f"Mention someone you wanna kiss ;)")
            return

        if user == ctx.author:
            await ctx.message.reply("Imagine kissing yourself...")
            return
            
        kissed_users = "".join(f'{users.mention} ' for users in user)
        embed = discord.Embed(
            title="Awww",
            description=f"**{ctx.message.author.name}** just kissed {kissed_users}",
            color=ctx.message.author.color,
            timestamp=ctx.message.created_at,
        )
        embed.set_image(url=await api_call("https://nekos.life/api/v2/img/kiss"))
        embed.set_author(
                name=ctx.message.author.display_name,
                icon_url=self.client.user.avatar_url,
            )
        await ctx.reply(embed=embed)

    @commands.cooldown(3, 5, commands.BucketType.user)
    @commands.command(name="cuddle", description="Cuddle someone")
    async def cuddle(self, ctx, user: commands.Greedy[discord.Member] = None):
        if user == None:
            await ctx.message.reply(f"Mention someone you wanna cuddle ;)")
            return
        cuddle_users = "".join(f'{users.mention} ' for users in user)
        embed = discord.Embed(
            title="Aww cuddles uwu",
            description=f"**{ctx.message.author.name}** just cuddled {cuddle_users}",
            color=ctx.message.author.color,
            timestamp=ctx.message.created_at,
        )
        embed.set_image(url=await api_call("https://nekos.life/api/v2/img/cuddle"))
        embed.set_author(
                name=ctx.message.author.display_name,
                icon_url=self.client.user.avatar_url,
            )
        await ctx.reply(embed=embed)

    @commands.cooldown(3, 5, commands.BucketType.user)
    @commands.command(name="slap", description="Bitch slap moment")
    async def slap(self, ctx, user: commands.Greedy[discord.Member] = None):
        if user == None:
            await ctx.message.reply(f"Mention someone you wanna slap ;)")
            return

        if user == ctx.author:
            await ctx.message.reply("Imagine slapping yourself...")
            return
        slapped_users = "".join(f'{users.mention} ' for users in user)
        embed = discord.Embed(
            title="**Damn son!**",
            description=f"{slapped_users} just got slapped by **{ctx.message.author.name}**.",
            color=ctx.message.author.color,
            timestamp=ctx.message.created_at,
        )
        embed.set_image(url=await api_call("https://nekos.life/api/v2/img/slap"))
        embed.set_author(
                name=ctx.message.author.display_name,
                icon_url=self.client.user.avatar_url,
            )
        await ctx.reply(embed=embed)

    @commands.cooldown(3, 5, commands.BucketType.user)
    @commands.command(name="tickle", description="Tickle someone!")
    async def tickle(self, ctx, user: commands.Greedy[discord.Member] = None):
        if user == None:
            await ctx.message.reply(f"Mention someone you wanna tickle ;)")
            return

        if user == ctx.author:
            await ctx.message.reply("Imagine tickling yourself...")
            return
        tickled_users = "".join([f"{users.mention} " for users in user])
        embed = discord.Embed(
            title="Tickle, tickle!",
            description=f"{tickled_users} just got tickled by **{ctx.message.author.name}**.",
            color=ctx.message.author.color,
            timestamp=ctx.message.created_at,
        )
        embed.set_image(url=await api_call("https://nekos.life/api/v2/img/tickle"))
        embed.set_author(
                name=ctx.message.author.display_name,
                icon_url=self.client.user.avatar_url,
            )
        await ctx.reply(embed=embed)

    @commands.cooldown(3, 5, commands.BucketType.user)
    @commands.command(name="feed", description="gib me food plz")
    async def feed(self, ctx, user: commands.Greedy[discord.Member] = None):
        if user == None:
            await ctx.message.reply(f"Who tf are you feeding?")
            return
        fed_users = "".join(f'{users.mention} ' for users in user)
        embed = discord.Embed(
            title="",
            description=f"**{ctx.message.author.name}** fed {fed_users}",
            color=ctx.message.author.color,
            timestamp=ctx.message.created_at,
        )
        embed.set_image(url=await api_call("https://nekos.life/api/v2/img/feed"))
        embed.set_author(
                name=ctx.message.author.display_name,
                icon_url=self.client.user.avatar_url,
            )
        await ctx.reply(embed=embed)

    @commands.cooldown(3, 5, commands.BucketType.user)
    @commands.command(name="bite", description="bite's users")
    async def bite(self, ctx, user: commands.Greedy[discord.Member] = None):
        if user == None:
            await ctx.message.reply(f"Who tf are you biting?")
            return
        bit_users = "".join(f'{users.mention} ' for users in user)
        embed = discord.Embed(
            title="",
            description=f"**{ctx.message.author.name}** bit {bit_users}",
            color=ctx.message.author.color,
            timestamp=ctx.message.created_at,
        )
        embed.set_image(url=await api_call("https://api.waifu.pics/sfw/bite"))
        embed.set_author(
                name=ctx.message.author.display_name,
                icon_url=self.client.user.avatar_url,
            )
        await ctx.reply(embed=embed)

    @commands.cooldown(3, 5, commands.BucketType.user)
    @commands.command(name="bonk", description="bonk users")
    async def bonk(self, ctx, user: commands.Greedy[discord.Member] = None):
        if user == None:
            await ctx.message.reply(f"No Bonk! :(")
            return
        bonk_users = "".join(f'{users.mention} ' for users in user)
        embed = discord.Embed(
            title="",
            description=f"**{ctx.message.author.name}** bonked {bonk_users}",
            color=ctx.message.author.color,
            timestamp=ctx.message.created_at,
        )
        embed.set_image(url=await api_call("https://api.waifu.pics/sfw/bonk"))
        embed.set_author(
                name=ctx.message.author.display_name,
                icon_url=self.client.user.avatar_url,
            )
        await ctx.reply(embed=embed)

def setup(client):
    client.add_cog(neko(client))