import discord
import asyncio
import inspect
import io
import re
import subprocess
import textwrap
import traceback

from discord_components import Button, ButtonStyle, Select, SelectOption

from discord.ext import commands
from contextlib import redirect_stdout
from typing import Optional
from boot.funcs import box
from boot.meifwa import MeifwaBot

START_CODE_BLOCK_RE = re.compile(r"^((```py(thon)?)(?=\s)|(```))")

class BotOwner(commands.Cog):
    """Bot Owner only commands"""
    def __init__(self, bot: MeifwaBot):
        self.bot = bot
        self._last_result = None
        self.sessions = set()

    @staticmethod
    def cleanup_code(content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith("```") and content.endswith("```"):
            return START_CODE_BLOCK_RE.sub("", content)[:-3]
        # remove `foo`
        return content.strip("` \n")
    
    @staticmethod
    def get_syntax_error(self, e):
        if e.text is None:
            return f"```py\n{e.__class__.__name__}: {e}\n```"
        return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'

    @staticmethod
    def paginate(self, text: str):
        last = 0
        pages = []
        for curr in range(0, len(text)):
            if curr % 1980 == 0:
                pages.append(text[last:curr])
                last = curr
                appd_index = curr
        if appd_index != len(text) - 1:
            pages.append(text[last:curr])
        return list(filter(lambda a: a != "", pages))
    
    @commands.command(hidden=True)
    async def elevate(self, ctx: commands.Context, user: discord.User = None):
        """Elevate a user or yourself to ownership privilege"""
        if not ctx.author.id in self.bot.get_config("config", "config", "owner_ids"):
            return await ctx.send(
                embed=discord.Embed(
                    description="Your User's ID was not found in the OWNER config.",
                    color=self.bot.error_color,
                )
            )
        if not user:
            user = ctx.author
        if user.id in self.bot.owner_ids:
            return await ctx.send(
                embed=discord.Embed(
                    description=f"{user} is already in the ownership privilege set",
                    color=self.bot.error_color,
                )
            )
        components = discord.ui.MessageComponents(
            discord.ui.ActionRow(
                discord.ui.Button(label="yes", style=discord.ui.ButtonStyle.green)
            )
        )

        msg = await ctx.send(
            embed=discord.Embed(
                description="Are you sure you want to do this?\nClick yes to confirm.",
                color=self.bot.ok_color,
            ).set_footer(
                text="⚠️ Elevating people to OWNER privilege will allow them to use owner only commands."
            ),
            components=components,
        )

        def check(payload: discord.Interaction):
            if payload.message.id != msg.id:
                return False
            if payload.user.id not in self.bot.get_config("config", "config", "owner_ids"):
                self.bot.loop.create_task(
                    payload.response.send_message(
                        "You aren't in the bots owners!",
                        ephemeral=True,
                    )
                )
                return False
            return True

        try:
            payload = await self.bot.wait_for("component_interaction", check=check, timeout=10)
        except asyncio.TimeoutError:
            await msg.edit(components=None)
            await ctx.message.add_reaction("⏰")
            await ctx.send("`Confirmation Timed Out`")
            return
        await payload.response.defer_update()
        await msg.edit(components=None)
        self.bot.owner_ids.add(user.id)
        filtered = [
            await self.bot.fetch_user(x) for x in self.bot.owner_ids if not x == 000000000000
        ]
        await ctx.send(
            content=user.mention,
            embed=discord.Embed(
                description="You have two minutes.", color=self.bot.ok_color
            ).add_field(
                name="Current privileged People",
                value="```\n" + "\n".join(map(str, filtered)) + "\n```",
            ),
        )
        loop = asyncio.get_running_loop()

        def remove_owner():
            if user.id not in self.bot.owner_ids:
                pass
            self.bot.owner_ids.remove(user.id)
            self.bot.logger.info(
                f"Removed {user}({user.id}) from the elevated owner privilege set."
            )
        loop.call_later(120, remove_owner)

    @commands.command(hidden=True)
    async def delevate(self, ctx: commands.Context, user: discord.User = None):
        """Delevate a users ownership privilege"""
        if not ctx.author.id in self.bot.get_config("config", "config", "owner_ids"):
            return await ctx.send(
                embed=discord.Embed(
                    description="You are not authorized to complete this action",
                    color=self.bot.error_color,
                )
            )
        if not user:
            user = ctx.author
        if user.id not in self.bot.owner_ids:
            return await ctx.send(
                embed=discord.Embed(
                    description=f"{user} is currently does not have ownership privilege",
                    color=self.bot.error_color,
                )
            )
        self.bot.owner_ids.remove(user.id)
        await ctx.message.add_reaction("\u2705")

    @commands.command(name="eval", hidden=True)
    @commands.is_owner()
    async def _eval(self, ctx: commands.Context, *, body: str):
        """Evaluates python code"""

        env = {
            "bot": self.bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "_": self._last_result,
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f"```py\n{e.__class__.__name__}: {e}\n```")

        func = env["func"]
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f"```py\n{value}{traceback.format_exc()}\n```")
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction("\u2705")
            except:
                pass

            if ret is None:
                try:
                    return
                except:
                    paginated_text = self.paginate(value)
                    for page in paginated_text:
                        if page == paginated_text[-1]:
                            await ctx.send(f"```py\n{page}\n```")
                            break
                        await ctx.send(f"```py\n{page}\n```")
            else:
                self._last_result = ret
                try:
                    await ctx.send(f"```py\n{value}{ret}\n```")
                except:
                    paginated_text = self.paginate(f"{value}{ret}")
                    for page in paginated_text:
                        if page == paginated_text[-1]:
                            await ctx.send(f"```py\n{page}\n```")
                            break
                        await ctx.send(f"```py\n{page}\n```")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def restart(self, ctx: commands.Context):
        """Restarts the bot"""
        embed = discord.Embed(title="Are you sure you want me to restart?")
        embed.color = self.bot.ok_color
        components = discord.ui.MessageComponents(
            discord.ui.ActionRow(
                discord.ui.Button(
                    label="Yes", style=discord.ui.ButtonStyle.green, custom_id="YES_RESTART"
                ),
                discord.ui.Button(
                    label="No", style=discord.ui.ButtonStyle.red, custom_id="NO_RESTART"
                ),
            )
        )
        msg = await ctx.send(embed=embed, components=components)

        def check(payload: discord.Interaction):
            if payload.message.id != msg.id:
                return False
            if payload.user.id not in ctx.bot.owner_ids:
                self.bot.loop.create_task(
                    payload.response.send_message(
                        "You can't respond to this message!",
                        ephemeral=True,
                    )
                )
                return False
            return True

        try:
            payload = await self.bot.wait_for("component_interaction", check=check, timeout=60)
        except asyncio.TimeoutError:
            embed.title = "Timed out... I guess I will stay then"
            return await msg.edit(embed=embed, components=None)
        if payload.component.custom_id == "YES_RESTART":
            embed.title = "Attempting to restart. See you in a bit. :wave:"
            await msg.edit(embed=embed, components=None)
            await self.bot.close()
        else:
            embed.title = "I guess I will stay then"
            await msg.edit(embed=embed, components=None)

    @commands.command(aliases=["shutdown", "logout", "sleep"], hidden=True)
    @commands.is_owner()
    async def die(self, ctx: commands.Context):
        """Kills the bot process."""

        embed = discord.Embed(title="Are you sure you want me to shutdown?")
        embed.color = self.bot.ok_color
        components = discord.ui.MessageComponents(
            discord.ui.ActionRow(
                discord.ui.Button(
                    label="Yes", style=discord.ui.ButtonStyle.green, custom_id="YES_SHUT"
                ),
                discord.ui.Button(
                    label="No", style=discord.ui.ButtonStyle.red, custom_id="NO_SHUT"
                ),
            )
        )
        msg = await ctx.send(embed=embed, components=components)

        def check(payload: discord.Interaction):
            if payload.message.id != msg.id:
                return False
            if payload.user.id not in ctx.bot.owner_ids:
                self.bot.loop.create_task(
                    payload.response.send_message(
                        "You can't respond to this message!",
                        ephemeral=True,
                    )
                )
                return False
            return True

        try:
            payload = await self.bot.wait_for("component_interaction", check=check, timeout=60)
        except asyncio.TimeoutError:
            embed.title = "Timed out... I guess I will stay then"
            return await msg.edit(embed=embed, components=None)
        if payload.component.custom_id == "YES_SHUT":
            embed.title = "Goodbye then :wave:"
            await msg.edit(embed=embed, components=None)
            await self.bot.full_exit()
        else:
            embed.title = "I guess I will stay then"
            await msg.edit(embed=embed, components=None)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx: commands.Context, extension):
        """Load bot extensions"""
        try:
            self.bot.load_extension(extension)
            await ctx.send(
                embed=discord.Embed(
                    description=f":inbox_tray: Loaded `{extension}`",
                    color=self.bot.ok_color,
                )
            )
        except commands.ExtensionError as e:
            await ctx.send(embed=discord.Embed(description=e, color=self.bot.error_color))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx: commands.Context, extension):
        """Unload bot extensions"""
        try:
            self.bot.unload_extension(extension)
            await ctx.send(
                embed=discord.Embed(
                    description=f":outbox_tray: Unloaded `{extension}`",
                    color=self.bot.ok_color,
                )
            )
        except commands.ExtensionError as e:
            await ctx.send(embed=discord.Embed(description=e, color=self.bot.error_color))

    @commands.command(name="reload", hidden=True)
    @commands.is_owner()
    async def _reload(self, ctx: commands.Context, extension):
        """Reload bot extensions"""
        try:
            self.bot.reload_extension(extension)
            await ctx.send(
                embed=discord.Embed(
                    description=f":repeat: Reloaded `{extension}`",
                    color=self.bot.ok_color,
                )
            )
        except commands.ExtensionError as e:
            await ctx.send(embed=discord.Embed(description=e, color=self.bot.error_color))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reloadall(self, ctx: commands.Context):
        """Reloads everysingle cog the bot has"""
        await ctx.send(
            embed=discord.Embed(
                description="Attempting to reload all cogs/extensions", color=self.bot.ok_color
            )
        )
        await self.bot.reload_all_extensions(ctx)

    @commands.is_owner()
    @commands.command(hidden=True)
    async def update(self, ctx: commands.Context):
        """Update to the latest version of the master repo or whatever the latest commit of your fork is"""
        await ctx.send(
            embed=discord.Embed(
                description=f"Attempting to update {self.bot.user.name} to the latest commit/version.",
                color=self.bot.ok_color,
            )
        )
        process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
        output = process.communicate()[0]
        await ctx.send(
            embed=discord.Embed(
                description=f"Output: ```{str(output[:1800], 'utf-8')}```", color=self.bot.ok_color
            )
        )
        process = subprocess.Popen(["git", "describe", "--always"], stdout=subprocess.PIPE)
        output = process.communicate()[0]
        await ctx.send(
            embed=discord.Embed(description="Reloading all modules now.", color=self.bot.ok_color)
        )
        await asyncio.sleep(1.5)
        await self.bot.reload_all_extensions(ctx)
        await ctx.send(
            embed=discord.Embed(
                description=f"Sucessfully updated {self.bot.user.name} Version `{self.bot.version}` to `{str(output, 'utf-8')}`",
                color=self.bot.ok_color,
            )
        )

    @commands.command(hidden=True)
    @commands.is_owner()
    async def say(self, ctx, chan: Optional[discord.TextChannel] = None, *, msg):
        """Say something with the bot."""
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass
        if chan is None:
            await ctx.send(msg)
        else:
            await chan.send(msg)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def dm(self, ctx: commands.Context, user: discord.User, *, msg):
        """Direct Message A User"""
        try:
            await user.send(
                embed=discord.Embed(
                    title=f"Message from {ctx.author}",
                    description=msg,
                    color=self.bot.ok_color,
                )
            )
            await ctx.send(
                embed=discord.Embed(
                    description=f"Direct Message sent to {user}",
                    color=self.bot.ok_color,
                )
            )
        except (discord.HTTPException, discord.Forbidden) as e:
            await ctx.send(embed=discord.Embed(description=e, color=self.bot.error_color))

    @commands.command(name="erase", aliases=["sho"], hidden=True)
    @commands.is_owner()
    @commands.guild_only()
    async def erase(self, ctx: commands.Context, limit: int = 50) -> None:

        prefix = self.bot.get_config("config", "config", "prefix")

        if ctx.channel.permissions_for(ctx.me).manage_messages:
            messages = await ctx.channel.purge(
                check=lambda message: message.author == ctx.me
                or message.content.startswith(prefix),
                bulk=True,
                limit=limit,
            )
        else:
            messages = await ctx.channel.purge(
                check=lambda message: message.author == ctx.me, bulk=False, limit=limit
            )

        await ctx.send(
            embed=discord.Embed(
                description=f"Found and deleted `{len(messages)}` of my message(s) out of the last `{limit}` message(s).",
                color=self.bot.ok_color,
            ),
            delete_after=5,
        )

    @commands.command(hidden=True)
    @commands.is_owner()
    async def leave(self, ctx: commands.Context, guild: discord.Guild):
        await guild.leave()
        await ctx.send(f"Successfully left {guild.name}")

def setup(bot):
    bot.add_cog(BotOwner(bot))