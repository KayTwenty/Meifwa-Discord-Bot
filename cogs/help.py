import discord
import logging
import DiscordUtils

from discord import Embed
from discord.ext import commands
from discord.errors import Forbidden
from discord.utils import normalise_optional_params
from boot.meifwa import MeifwaBot

log = logging.getLogger("help cog")

async def send_embed(ctx, embed):
    try:
        await ctx.send(embed=embed)
    except Forbidden:
        try:
            await ctx.author.send(
                f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                f"May you inform the server team about this issue? :slight_smile: ",
                embed=embed,
            )
        except:
            ctx.send("It seems i don't have perms to send embeds in this channel.")


class Help(commands.Cog):
    def __init__(self, bot: MeifwaBot):
        self.bot = bot

    async def make_error_embed(self, ctx, name):
        emb = discord.Embed(
            title="lol, sadphroge \N{PENSIVE FACE}\N{PENSIVE FACE}\N{PENSIVE FACE}",
            description=f"ERROR 404 couldn't find `{name}` module",
            color=ctx.message.author.color,
        )
        return emb

    @commands.Cog.listener()
    async def on_ready(self):
        log.warn(f"{self.__class__.__name__} Cog has been loaded")

    @commands.guild_only()
    @commands.command(hidden=True)
    async def help(self, ctx, *, input: str = None):
        if "<@" in str(ctx.prefix) and ">" in str(ctx.prefix):
            ctx.prefix = f"@{str(self.bot.user).split('#')[0]} "
        if not input:
            emb = discord.Embed(
                title="Commands and modules",
                color=ctx.message.author.color,
                description=f"Use `{ctx.prefix}help <module>` to gain more information about that module.",
            )
            emb.set_footer(
                text=f"Requested by {ctx.message.author}",
                icon_url=self.bot.user.avatar.url
            )
            emb.set_thumbnail(url=ctx.message.author.avatar.url)
            emb.set_author(
                name=ctx.message.author.display_name,
                icon_url=ctx.message.guild.icon.url,
            )
            emb.add_field(
                name="Consider Upvoting?",
                value=f"[Click Here](https://discordbotlist.com/bots/meifwa/upvote)",
                inline=False
            )
            cogs_desc = ""
            for cog in self.bot.cogs:
                commands = self.bot.get_cog(cog).get_commands()
                hidden_count = 0
                if len(commands) == 0:
                    continue
                for command in commands:
                    if command.hidden:
                        hidden_count += 1
                if hidden_count == len(commands):
                    continue
                emb.add_field(
                    name=f"{cog}", value=self.bot.cogs[cog], inline=False)
            commands_desc = ""
            for command in self.bot.walk_commands():
                if not command.cog_name and not command.hidden:
                    commands_desc += f"{command.name} - {command.help}\n"
            if commands_desc:
                emb.add_field(
                    name="Not belonging to a module", value=commands_desc, inline=False
                )
            return await send_embed(ctx, emb)

        else:
            if input.lower() == "nsfw":
                if not ctx.channel.is_nsfw():
                    return await ctx.send("Ehhhh this commands works in nsfw channels only :flushed:")
            pages = []

            def make_embed():
                embed = Embed(
                    color=ctx.message.author.color, timestamp=ctx.message.created_at
                )
                embed.set_footer(
                    text=f"Requested by {ctx.message.author}",
                    icon_url=self.bot.user.avatar.url,
                )
                embed.set_thumbnail(url=ctx.message.author.avatar.url)
                embed.set_author(
                    name=ctx.message.author.display_name,
                    icon_url=self.bot.user.avatar.url,
                )
                return embed

            for cog in self.bot.cogs:
                if cog.lower() == input.lower():
                    threshold = 10
                    commands = self.bot.get_cog(cog).get_commands()
                    command_chunk = [
                        commands[i: i + threshold]
                        for i in range(0, len(commands), threshold)
                    ]
                    i = 0
                    embeds = []
                    command_list = ""
                    for chunk in command_chunk:
                        embed = make_embed()
                        for command in chunk:
                            embed.title = f"{command.cog_name} - Commands"
                            embed.description = self.bot.cogs[cog].__doc__
                            embed.set_footer(
                                text="Commands: @Meifwa help"
                            )
                            if command.hidden:
                                continue
                            i = i + 1
                            aliases = ""
                            description = ""
                            if len(command.aliases) != 0:
                                aliases = ", ".join(
                                    [alias for alias in command.aliases]
                                )
                            else:
                                aliases = "None"
                            description = command.description or "None"

                            command_list = f"{i}) `{ctx.prefix}{command.name}`\n"
                            embed.add_field(
                                inline=False,
                                name=f"{command_list}",
                                value=f"Aliases: **{aliases}**\nDescription: **{description}**\nUsage: **{ctx.prefix+command.name} {command.signature}**",
                            )
                            command_list = ""
                        embeds.append(embed)
                        embed = None
                    if i == 0:
                        emb = await self.make_error_embed(ctx, input)
                        return await send_embed(ctx, emb)
                    if len(embeds) == 1:
                        return await send_embed(ctx, embed=embeds[0])
                    else:
                        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(
                            ctx, remove_reactions=True
                        )
                        paginator.add_reaction(
                            "\N{Black Left-Pointing Double Triangle with Vertical Bar}",
                            "first",
                        )
                        paginator.add_reaction(
                            "\N{Black Left-Pointing Double Triangle}", "back"
                        )
                        paginator.add_reaction("\N{CROSS MARK}", "lock")
                        paginator.add_reaction(
                            "\N{Black Right-Pointing Double Triangle}", "next"
                        )
                        paginator.add_reaction(
                            "\N{Black Right-Pointing Double Triangle with Vertical Bar}",
                            "last",
                        )
                        return await paginator.run(embeds)
                    break

            else:
                emb = await self.make_error_embed(ctx, input)
                return await send_embed(ctx, emb)

def setup(bot):
    bot.add_cog(Help(bot))