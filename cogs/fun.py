import discord, random

from discord.ext import commands
from boot.meifwa import MeifwaBot


class Fun(commands.Cog):
    def __init__(self, client: MeifwaBot):
        self.client = client

    @commands.command(name="8ball", aliases=['8balls', '8b']) #The Main 9Ball command
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

        embed=discord.Embed(title="The official 8Ball has Spoken.", color=ctx.message.author.color)
        embed.set_author(name="Asked by " + str(ctx.message.author), icon_url=ctx.message.author.avatar.url)
        embed.add_field(name="Question:", value=question, inline=False)
        embed.add_field(name="Answer:", value=random.choice(responses), inline=False)
        embed.set_footer(text=f"Commands: {ctx.prefix}8ball *question*")
        await ctx.send(embed=embed)
        await ctx.message.delete()

def setup(client):
    client.add_cog(Fun(client))