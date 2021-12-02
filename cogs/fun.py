import discord, asyncio

from discord.ext import commands
from boot.meifwa import MeifwaBot


expiry = 7200 # Max expiry time (2 Hours max)

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
    

    @commands.command()
    async def youtube(self, ctx):
        link = await self.client.togetherControl.create_link(ctx.author.voice.channel.id, 'youtube', max_age=expiry)
        embed = discord.Embed(
            color=ctx.message.author.color,
            title='YouTube Together Generated!',
            description=f'To open a room, [Click Here]({link})'
        )
        embed.set_thumbnail(url='https://cdn.vox-cdn.com/thumbor/0kpe316UpZWk53iw3bOLoJfF6hI=/0x0:1680x1050/1400x1400/filters:focal(706x391:974x659):format(gif)/cdn.vox-cdn.com/uploads/chorus_image/image/56414325/YTLogo_old_new_animation.0.gif')
        embed.set_footer(text='This link will expire after 2 hours')
        await ctx.reply(embed=embed)


    @commands.command()
    async def poker(self, ctx):
        link = await self.client.togetherControl.create_link(ctx.author.voice.channel.id, 'poker', max_age=expiry)
        embed = discord.Embed(
            color=ctx.message.author.color,
            title='Poker Room Generated!',
            description=f'To open a room, [Click Here]({link})'
        )
        embed.set_thumbnail(url='https://cdn.dribbble.com/users/1320536/screenshots/3151889/poker-chip.gif')
        embed.set_footer(text='This link will expire after 2 hours')
        await ctx.reply(embed=embed)


    @commands.command()
    async def chess(self, ctx):
        link = await self.client.togetherControl.create_link(ctx.author.voice.channel.id, 'chess', max_age=expiry)
        embed = discord.Embed(
            color=ctx.message.author.color,
            title='Chess Room Generated!',
            description=f'To open a room, [Click Here]({link})'
        )
        embed.set_footer(text='This link will expire after 2 hours')
        await ctx.reply(embed=embed)


    @commands.command()
    async def betrayal(self, ctx):
        link = await self.client.togetherControl.create_link(ctx.author.voice.channel.id, 'betrayal', max_age=expiry)
        embed = discord.Embed(
            color=ctx.message.author.color,
            title='Betrayal.io Room Generated!',
            description=f'To open a room, [Click Here]({link})'
        )
        embed.set_footer(text='This link will expire after 2 hours')
        await ctx.reply(embed=embed)
    

    @commands.command()
    async def fishington(self, ctx):
        link = await self.client.togetherControl.create_link(ctx.author.voice.channel.id, 'fishing', max_age=expiry)
        embed = discord.Embed(
            color=ctx.message.author.color,
            title='Fishington.io Room Generated!',
            description=f'To open a room, [Click Here]({link})'
        )
        embed.set_footer(text='This link will expire after 2 hours')
        await ctx.reply(embed=embed)
    

    @commands.command()
    async def lettertile(self, ctx):
        link = await self.client.togetherControl.create_link(ctx.author.voice.channel.id, 'letter-tile', max_age=expiry)
        embed = discord.Embed(
            color=ctx.message.author.color,
            title='Letter Tile Room Generated!',
            description=f'To open a room, [Click Here]({link})'
        )
        embed.set_footer(text='This link will expire after 2 hours')
        await ctx.reply(embed=embed)


    @commands.command()
    async def wordsnack(self, ctx):
        link = await self.client.togetherControl.create_link(ctx.author.voice.channel.id, 'word-snack', max_age=expiry)
        embed = discord.Embed(
            color=ctx.message.author.color,
            title='Word Snack Room Generated!',
            description=f'To open a room, [Click Here]({link})'
        )
        embed.set_footer(text='This link will expire after 2 hours')
        await ctx.reply(embed=embed)


    @commands.command()
    async def doodlecrew(self, ctx):
        link = await self.client.togetherControl.create_link(ctx.author.voice.channel.id, 'doodle-crew', max_age=expiry)
        embed = discord.Embed(
            color=ctx.message.author.color,
            title='Doodle-Crew Room Generated!',
            description=f'To open a room, [Click Here]({link})'
        )
        embed.set_footer(text='This link will expire after 2 hours')
        await ctx.reply(embed=embed)
    

    @commands.command()
    async def spellcast(self, ctx):
        link = await self.client.togetherControl.create_link(ctx.author.voice.channel.id, 'spellcast', max_age=expiry)
        embed = discord.Embed(
            color=ctx.message.author.color,
            title='SpellCast Room Generated!',
            description=f'To open a room, [Click Here]({link})'
        )
        embed.set_footer(text='This link will expire after 2 hours')
        await ctx.reply(embed=embed)


    @commands.command()
    async def awkword(self, ctx):
        link = await self.client.togetherControl.create_link(ctx.author.voice.channel.id, 'awkword', max_age=expiry)
        embed = discord.Embed(
            color=ctx.message.author.color,
            title='Awkword Room Generated!',
            description=f'To open a room, [Click Here]({link})'
        )
        embed.set_footer(text='This link will expire after 2 hours')
        await ctx.reply(embed=embed)


    @commands.command()
    async def checkers(self, ctx):
        link = await self.client.togetherControl.create_link(ctx.author.voice.channel.id, 'checkers', max_age=expiry)
        embed = discord.Embed(
            color=ctx.message.author.color,
            title='Checkers in the Park Room Generated!',
            description=f'To open a room, [Click Here]({link})'
        )
        embed.set_footer(text='This link will expire after 2 hours')
        await ctx.reply(embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))