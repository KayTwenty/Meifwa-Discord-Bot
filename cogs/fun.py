import discord, random

from discord.ext import commands
from boot.meifwa import MeifwaBot


expiry = 7200 # Max expiry time (2 Hours max)

class Fun(commands.Cog):
    def __init__(self, client: MeifwaBot):
        self.client = client

    @commands.command(aliases=['8balls', '8b']) #The Main 9Ball command
    async def _8ball(self, ctx, *, question):
        responses = ["As I see it, no.",
                    "It is decidedly so.",
                    "Without a doubt.",
                    "Yes - definitely",
                    "You may rely on it.",
                    "Most likely.",
                    "Kinda.",
                    "Yes.",
                    "Signs point to yes.",
                    "Yup.",
                    "Affirmative.",
                    "Don't count on it.",
                    "My reply is no",
                    "My Sources say no.",
                    "very doubtful.",
                    "**Yes.**",
                    "**No.**",
                    "Simp!",
                    "Definitely not!",
                    "Ask an admin",
                    "Maybe Not.",
                    "Nie.",
                    "Negative.",
                    "Definitely yes!",
                    "I can see it as true.",
                    "I can see it as false.",
                    "Idk m8... Ask Artic...",
                    "Oh hecc naw!",
                    "Definitely."]

        embed=discord.Embed(title="The official 9Ball has Spoken.", color=ctx.message.author.color)
        embed.set_author(name="Asked by " + str(ctx.message.author), icon_url=ctx.message.author.avatar.url)
        embed.add_field(name="Question:", value=question, inline=False)
        embed.add_field(name="Answer:", value=random.choice(responses), inline=False)
        embed.set_footer(text=f"Commands: {ctx.prefix}8ball *question*")
        await ctx.send(embed=embed)
        await ctx.message.delete()

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

def setup(client):
    client.add_cog(Fun(client))