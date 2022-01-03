import discord 
from discord.ext import commands

from typing import Optional

from boot.dbmanagers import PrefixManager
from boot.context import MeifwaContext
from boot.meifwa import MeifwaBot

class Guild(commands.Cog):
    def __init__(self, bot: MeifwaBot):
        self.bot = bot
        self.prefix_manager = PrefixManager(bot=self.bot)

    @commands.group(name="prefix", description=";prefix set or ;prefix reset", invoke_without_command=True)
    async def prefix(self, ctx: commands.Context):
        g_prefix = self.bot.prefixes.get(str(ctx.guild.id)) or self.bot.get_config(
            "config", "config", "prefix"
        )
        await ctx.send(
            embed=discord.Embed(
                description=f"The current prefix for this guild is `{g_prefix}`",
                color=self.bot.ok_color,
            )
        )

    @prefix.command(name="set", description="Set a new prefix for this server")
    @commands.has_permissions(manage_guild=True)
    async def _set(self, ctx, prefix: str):
        if len(prefix) > 10:
            return await ctx.send("Prefix can't be longer than 10 characters.")
        await self.prefix_manager.add_prefix(ctx.guild.id, prefix)
        await ctx.send(
            embed=discord.Embed(
                title="New Prefix Set",
                description=f"New Prefix: `{prefix}`",
                color=self.bot.ok_color,
            )
        )

    @prefix.command(aliases=["reset"], name="default", description="Set the current prefix for this server back to default")
    @commands.has_permissions(manage_guild=True)
    async def default(self, ctx: commands.Context):
        await self.prefix_manager.remove_prefix(ctx.guild.id)
        await ctx.send(
            embed=discord.Embed(title="Prefix set back to normal", color=self.bot.ok_color)
        )

    @commands.command(aliases=["sinfo", "ginfo", "guildinfo"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def serverinfo(self, ctx: MeifwaContext, guild: discord.Guild = None):
        if guild is None:
            guild = ctx.guild

        weird_stuff = {
            "ANIMATED_ICON": "Animated Icon",
            "BANNER": "Banner Image",
            "COMMERCE": "Commerce",
            "COMMUNITY": "Community",
            "DISCOVERABLE": "Server Discovery",
            "FEATURABLE": "Featurable",
            "INVITE_SPLASH": "Splash Invite",
            "MEMBER_LIST_DISABLED": "Member list disabled",
            "MEMBER_VERIFICATION_GATE_ENABLED": "Membership Screening enabled",
            "MORE_EMOJI": "More Emojis",
            "NEWS": "News Channels",
            "PARTNERED": "Partnered",
            "PREVIEW_ENABLED": "Preview enabled",
            "PUBLIC_DISABLED": "Public disabled",
            "VANITY_URL": "Vanity URL",
            "VERIFIED": "Verified",
            "VIP_REGIONS": "VIP Voice Servers",
            "WELCOME_SCREEN_ENABLED": "Welcome Screen enabled",
            "THREADS_ENABLED": "Threads Enabled",
            "THREADS_ENABLED_TESTING": "Threads Testing",
            "PRIVATE_THREADS": "Private Threads",
            "SEVEN_DAY_THREAD_ARCHIVE": "Seven Days Thread Archive",
            "THREE_DAY_THREAD_ARCHIVE": "Three Days Thread Archive",
            "ROLE_ICONS": "Role Icons",
            "RELAYS": "Relays Enabled",
        }
        guild_features = [
            f"✅ {name}\n"
            for weird_stuff, name in weird_stuff.items()
            if weird_stuff in guild.features
        ]
        embed = discord.Embed(title=guild.name, color=self.bot.ok_color)
        embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(
            name="Owner",
            value=f"Name: **{guild.owner}**\nID: **{guild.owner.id}**",
            inline=True,
        )
        embed.add_field(
            name="Creation Time",
            value=f"<t:{int(guild.created_at.timestamp())}:F>",
            inline=False,
        )
        embed.add_field(
            name="Member Count", value=f"**{guild.member_count}**", inline=True
        )
        embed.add_field(
            name="Role Count",
            value="**{}**".format(len(guild.roles)),
            inline=True,
        )
        embed.add_field(
            name="Channel Count",
            value=f"Text: **{len(guild.text_channels)}**\n"
                  f"Voice: **{len(guild.voice_channels)}**\n"
                  f"Categories: **{len(guild.categories)}**\n"
                  f"Total **{len(guild.text_channels) + len(guild.voice_channels) + len(guild.categories)}**",
            inline=True,
        )
        embed.add_field(
            name="Emoji Count",
            value="**{}**".format(len(guild.emojis)),
            inline=True,
        )
        if guild_features:
            embed.add_field(
                name="Features", value="".join(guild_features), inline=False
            )
        if guild.banner:
            embed.set_image(url=guild.banner.url)
        elif guild.splash:
            embed.set_image(url=guild.splash.url)

        embed.set_footer(text=f"ID: {guild.id}")
        await ctx.send(embed=embed)

    @commands.command(aliases=["uinfo", "memberinfo", "minfo"])
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def userinfo(self, ctx: MeifwaContext, user: discord.Member = None):
        if user is None:
            user = ctx.author

        user_flags = "\n".join(
            i.replace("_", " ").title() for i, v in user.public_flags if v
        )
        roles = user.roles[-1:0:-1]
        embed = discord.Embed(color=user.color or self.bot.ok_color)
        embed.set_thumbnail(url=user.avatar.url)
        embed.add_field(name="Name", value=user)
        embed.add_field(name="ID", value=user.id)
        embed.add_field(
            name="Status & Activity",
            value=f"Status: {str(user.status).title()}\nActivity: {user.activity.name if user.activity else 'No Activity'}",
            inline=False,
        )
        embed.add_field(
            name="Account Creation",
            value=f"<t:{int(user.created_at.timestamp())}:F>",
        )
        embed.add_field(
            name=f"{ctx.guild} Join Date",
            value=f"<t:{int(user.joined_at.timestamp())}:F>"
            if user.joined_at
            else "Unknown.",
            inline=False,
        )
        if roles:
            embed.add_field(
                name=f"Roles **{(len(user.roles) - 1)}**",
                value=", ".join([x.mention for x in roles[:10]]),
                inline=False,
            )
        if user_flags:
            embed.add_field(
                name="Public User Flags",
                value=user_flags,
                inline=False,
            )
        if not user.bot:
            if banner := (await self.bot.fetch_user(user.id)).banner:
                embed.set_image(url=banner.url)
        await ctx.send(embed=embed)

    @commands.command(aliases=["av"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True)
    async def avatar(self, ctx: MeifwaContext, user: Optional[discord.Member]):
        """Check your avatars."""
        await ctx.channel.trigger_typing()
        if user is None:
            user = ctx.author
        av = user.avatar
        e = discord.Embed(
            title=f"{user.name}'s avatar", color=self.bot.ok_color
        )
        e.add_field(
            name="File Formations",
            value=f"[jpg]({av.with_format('jpg')}), "
                  f"[png]({av.with_format('png')}), "
                  f"[webp]({av.with_format('webp')}){',' if av.is_animated() else ''} "
                  f"{f'[gif]({av})' if av.is_animated() else ''}",
        )
        e.add_field(
            name="Animated", value="\u2705" if av.is_animated() else ":x:"
        )
        e.set_image(url=av.with_size(4096))
        e.set_footer(text=f"ID: {user.id}")
        await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(Guild(bot))