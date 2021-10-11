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
        embed.set_footer(text=f"Command: {ctx.prefix}fuck @user")
        await ctx.reply(embed=embed)

    @commands.command(name="horny", description="Gives people horny license")
    async def horny(self, ctx, member: discord.Member = None):   
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'https://some-random-api.ml/canvas/horny?avatar={member.avatar_url_as(format="png")}'
            ) as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "horny.png")
                    embed = discord.Embed(title="Bam! U're free!", color=0xf1f1f1)
                    embed.set_author(name="Command used by: " + str(ctx.message.author), icon_url=ctx.message.author.avatar_url)
                    embed.set_image(url="attachment://horny.png")
                    embed.set_footer(text=f'Command: {ctx.prefix}horny @user')
                    await ctx.reply(embed=embed, file=file)
                else:
                    await ctx.reply('No horny :(')
                await session.close()

def setup(bot):
    bot.add_cog(Fun(bot))