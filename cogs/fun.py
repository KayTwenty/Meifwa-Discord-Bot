import discord, asyncio
import aiohttp
import random
import logging
import io

from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from boot.meifwa import MeifwaBot

async def api_call(call_uri, state=True):
	async with aiohttp.ClientSession() as session:
		async with session.get(f"{call_uri}") as response:
			response = await response.json()
			if state:
				return response['url']
			if state == False:
				return response

class Fun(commands.Cog):
    def __init__(self, bot: MeifwaBot):
        self.bot = bot

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

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=['meow', 'simba', 'cats'], description="Cats!!")
    async def cat(self, ctx):
        response = await api_call("http://aws.random.cat/meow", False)
        embed = discord.Embed(
            title="Cute catto!",
            color=ctx.message.author.color, 
            timestamp=ctx.message.created_at
            )
        embed.set_image(url=response['file'])
        embed.set_author(name=ctx.message.author.display_name,
                         icon_url=ctx.message.author.avatar.url)
        embed.set_footer(text=f"Command: {ctx.prefix}cat")
        await ctx.message.reply(embed=embed)

    @commands.cooldown(5, 7, commands.BucketType.user)
    @commands.command(name="goose", description="Shows a picture of a goose")
    async def goose(self, ctx):
        embed = discord.Embed(
            title="",
            color=ctx.message.author.color,
            timestamp=ctx.message.created_at
        )
        embed.set_author(name=ctx.message.author.display_name,
                         icon_url=ctx.message.author.avatar.url)
        embed.set_image(url=await api_call("https://nekos.life/api/v2/img/goose"))
        embed.set_footer(text=f"Command: {ctx.prefix}goose")
        await ctx.message.reply(embed=embed)

    @commands.cooldown(3, 7, commands.BucketType.user)
    @commands.command(name="waifu", description="Generates waifu")
    async def waifu(self, ctx):
        embed = discord.Embed(
            title="",
            color=ctx.message.author.color,
            timestamp=ctx.message.created_at
        )
        embed.set_author(name=ctx.message.author.display_name,
                         icon_url=ctx.message.author.avatar.url)
        embed.set_image(url=await api_call("https://nekos.life/api/v2/img/waifu"))
        embed.set_footer(text=f"Command: {ctx.prefix}waifu")
        await ctx.send(embed=embed)
    
    @commands.command()
    async def horny(ctx, user: discord.Member = None):
        user = user or ctx.author
        async with aiohttp.ClientSession() as session:
            async with session.get(
            f'https://some-random-api.ml/canvas/horny?avatar={user.display_avatar.with_format("png").url}'
        ) as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "horny.png")
                    em = discord.Embed(
                        title="bonk",
                        color=0xf1f1f1,
                    )
                    em.set_image(url="attachment://horny.png")
                    await ctx.send(embed=em, file=file)
                else:
                    await ctx.send('No horny :(')
                await session.close()

def setup(bot):
    bot.add_cog(Fun(bot))