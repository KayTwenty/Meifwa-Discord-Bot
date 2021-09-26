import discord
import os
import logging
import aiohttp
from discord.ext import commands

log = logging.getLogger("Fun cog")

async def api_call(call_uri, state=True):
	async with aiohttp.ClientSession() as session:
		async with session.get(f"{call_uri}") as response:
			response = await response.json()
			if state:
				return response['url']
			if state == False:
				return response

class fun(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        log.warn(f"{self.__class__.__name__} Cog has been loaded")

    @commands.cooldown(5, 7, commands.BucketType.user)
    @commands.command(name="pizza", description="Hawt & Yummy")
    async def pizza(self, ctx):
        if ctx.channel.is_nsfw():
            embed = discord.Embed(
                title="Hot Pizza!!",
                color=ctx.message.author.color,
                timestamp=ctx.message.created_at,
            )

            embed.set_footer(
                text=f"Requested by {ctx.message.author.display_name}#{ctx.message.author.discriminator}",
                icon_url=ctx.message.author.avatar_url,
            )
            embed.set_author(
                name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url
            )

            embed.set_image(
                url=await api_call("https://foodish-api.herokuapp.com/images/pizza/")
            )
            await ctx.message.reply(embed=embed)

def setup(client):
    client.add_cog(fun(client))