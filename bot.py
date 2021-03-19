import discord
from discord.ext import commands
import random
from random import randint
import os

TOKEN = "Enter Token Here"
BOT_PREFIX = '/'

bot = commands.Bot(command_prefix=BOT_PREFIX)

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("/purr"))
    print("Logged in as: " + bot.user.name + "\n")

@bot.command()
async def purr(ctx):
    num = randint(1, 15)
    try:
        await ctx.send(file = discord.File("Pic/{}.jpg".format(num)))
    except:
        await ctx.send(file = discord.File("Pic/{}.gif".format(num)))

@bot.command(pass_context=True)
async def cookie(ctx, member: discord.Member):
    """Give a cookie to someone."""
    embed = discord.Embed(title="This person has gave you a cookie!", description="**{1}** gave a cookie to **{0}**! :cookie:".format(member.name, ctx.message.author.name), color=0x25f079)
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def hug(ctx, member: discord.Member):
    """Hug someone."""
    embed = discord.Embed(title="Sending!", description="**{1}** hugs **{0}**!".format(member.name, ctx.message.author.name), color=0x25f079)
    embed.set_image(url="https://media1.tenor.com/images/29a4aef07fde6e590aeaa3381324bbd1/tenor.gif?itemid=18630098")
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def bonk(ctx, member: discord.Member):
    """Shoot someone."""
    embed = discord.Embed(title="**Hahaha! Get Bonked Nerd!!!**", description="**{1}** Bonked **{0}**!".format(member.name, ctx.message.author.name), color=0x25f079)
    embed.set_image(url="https://i.imgur.com/t1a9akh.gif")
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def fistbump(ctx, member: discord.Member):
    """Slap someone."""
    embed = discord.Embed(title="Wapow!", description="**{1}** Fistbumped **{0}**!".format(member.name, ctx.message.author.name), color=0x25f079)
    embed.set_image(url="https://media2.giphy.com/media/l0HlL6XHioKD5Gsgg/giphy.gif?cid=ecf05e473oo7yozme81o170s0i9tjwxdb7pq69ba46acewt0&rid=giphy.gif")
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def shoot(ctx, member: discord.Member):
    """Shoot someone."""
    embed = discord.Embed(title="Bingo Bango Bongo!", description="**{1}** shoots **{0}**!".format(member.name, ctx.message.author.name), color=0x25f079)
    embed.set_image(url="https://media.giphy.com/media/9umH7yTO8gLYY/giphy.gif")
    await ctx.send(embed=embed)

@bot.command()
async def poll(ctx, *, message):
    emb=discord.Embed(title=f"{message}", description="It's a poll!")
    msg=await ctx.channel.send(embed=emb)
    await msg.add_reaction('✅')
    await msg.add_reaction('❌')


bot.run(TOKEN)
