import discord, asyncio
import rethinkdb as r
import aiohttp
import random
import base64, json
import logging
import re
import typing
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from .utils.chat_formatting import bold

from .utils import helpers

r_conn = r.connect(db="meifwa")

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
    
    def cog_unload(self):
        self.session.close()
        del self.session

    async def get_cached_user(self, user_id: int):
            cache = await self.bot.redis.get("user_cache:{}".format(user_id))
            if cache is None:
                cache = await self.bot.fetch_user(user_id)
                cache = {
                    "name": cache.name,
                    "id": cache.id,
                    "discriminator": cache.discriminator
                }
                await self.bot.redis.set("user_cache:{}".format(user_id), base64.b64encode(
                    json.dumps(cache).encode("utf8")
                ).decode("utf8"), expire=1800)
            else:
                cache = json.loads(base64.b64decode(cache))
            return cache

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def marry(self, ctx, user: discord.Member):
        if user == ctx.author:
            return await ctx.send(bold("You can't marry yourself."))
        author_data = r.table("marriage").get(str(ctx.author.id)).run(r_conn)
        if not author_data:
            author_data = {
                "id": str(ctx.author.id),
                "marriedTo": []
            }
        r.table("marriage").insert(author_data).run(r_conn)
        
        if str(user.id) in author_data.get("marriedTo", []):
            return await ctx.send(bold("You are already married to that user."))
        elif len(author_data.get("marriedTo", [])) >= 4:
            return await ctx.send(bold("You are married to too many users"))

        user_data = r.table("marriage").get(str(user.id)).run(r_conn)
        if not user_data:
            user_data = {
                "id": str(user.id),
                "marriedTo": []
            }
        r.table("marriage").insert(user_data).run(r_conn)
        
        if len(user_data.get("marriedTo", [])) >= 4:
            return await ctx.send("That user is already married to too many users")

        a_name = helpers.clean_text(ctx.author.name)
        u_name = helpers.clean_text(user.name)
        await ctx.send("{} is wanting to marry {}!\n{} type yes to accept!".format(a_name, u_name, user.mention))

        try:
            msg = await self.bot.wait_for("message", check=lambda x: x.channel == ctx.message.channel and x.author == user, timeout=15.0)
            if msg.content.lower() != "yes":
                return await ctx.send("Marriage Cancelled.")
        except asyncio.TimeoutError:
            return await ctx.send("Marriage Cancelled.")

        await ctx.send(f"🎉 {ctx.author.mention} ❤ {user.mention} 🎉")

        author_marriedTo = author_data.get("marriedTo", [])
        user_marriedTo = user_data.get("marriedTo", [])
        author_marriedTo.append(str(user.id))
        user_marriedTo.append(str(ctx.author.id))
        r.table("marriage").get(str(ctx.author.id)).update({"marriedTo": author_marriedTo}).run(r_conn)
        r.table("marriage").get(str(user.id)).update({"marriedTo": user_marriedTo}).run(r_conn)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def divorce(self, ctx, user: typing.Union[discord.User, discord.Member, int]):
        if isinstance(user, int):
            try:
                converter = commands.UserConverter()
                user = await converter.convert(ctx, str(user))
            except commands.BadArgument:
                user_re_match = re.match("[0-9]{12,22}", str(user))
                if user_re_match is None:
                    return await ctx.send_help(ctx.command)
                user = await self.bot.fetch_user(int(user_re_match.group(0)))

        if user.id == ctx.author.id:
            return await ctx.send("You can't divorce yourself")

        author_data = r.table("marriage").get(str(ctx.author.id)).run(r_conn)
        if not author_data:
            return await ctx.send(bold("You are not married"))
        user_data = r.table("marriage").get(str(user.id)).run(r_conn)
        if not user_data:
            return await ctx.send("That user is not married to anyone")
        if not str(ctx.author.id) in user_data.get("marriedTo", []):
            return await ctx.send("That user is not married to you")

        await ctx.send("**Are you sure you want to divorce {}?**".format(helpers.clean_text(user.name)))

        try:
            msg = await self.bot.wait_for("message", check=lambda x: x.channel == ctx.message.channel and x.author == ctx.author, timeout=15.0)
            if msg.content.lower() != "yes":
                return await ctx.send("**Cancelled.**")
        except asyncio.TimeoutError:
            return await ctx.send("**Cancelled.**")

        new_author_married = []
        for u in author_data.get("marriedTo", []):
            if u != str(user.id):
                new_author_married.append(u)

        new_user_married = []
        for u in user_data.get("marriedTo", []):
            if u != str(ctx.author.id):
                new_user_married.append(u)

        r.table("marriage").get(str(user.id)).update({"marriedTo": new_user_married}).run(r_conn)
        r.table("marriage").get(str(ctx.author.id)).update({"marriedTo": new_author_married}).run(r_conn)
        await ctx.send("{} divorced {} 😦😢".format(helpers.clean_text(ctx.author.name), helpers.clean_text(user.name)))

    @commands.command(aliases=['sex', 'fuck']) #Frick Command
    async def frick(self, ctx, member: discord.Member):
        embed = discord.Embed(title=f"{ctx.message.author.name} wants to fuck you. Do you accept?", description="Type yes or no.", color=ctx.message.author.color)
        await ctx.send(embed=embed)
        
        try:
            msg = await self.bot.wait_for("message", check=lambda x: x.channel == ctx.message.channel and x.author == ctx.author, timeout=15.0)
            if msg.content.lower() != "yes":
                return await ctx.send("**Cancelled.**")
        except asyncio.TimeoutError:
            return await ctx.send("**Cancelled.**")
         
        embed = discord.Embed(title="This person had sex with you ;)", description="**{1}** fucked **{0}**!".format(member.name, ctx.message.author.name), color=ctx.message.author.color, timestamp=ctx.message.created_at)
        embed.set_author(name="Fucked by " + str(ctx.message.author), icon_url=ctx.message.author.avatar_url)
        embed.set_image(url="https://media1.tenor.com/images/fa98b23ca1dba1925da62f834f27153f/tenor.gif?itemid=19355212")
        embed.set_footer(text="Command: ;fuck @user")
        await ctx.reply(embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))