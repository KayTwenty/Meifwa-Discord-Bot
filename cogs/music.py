import asyncio
import utils.classes.exceptions as Exceptions
import lavalink
import aiohttp
import datetime
import math

from discord.ext import commands
import discord

from utils.commons.regex import url_rx, track_title_rx
from boot.meifwa import MeifwaBot

class Music(commands.Cog):
    def __init__(self, bot: MeifwaBot):
        self.bot = bot
        self.bot.loop.create_task(self.node_init())
        self.ll_ip = self.bot.get_config("config", "music", "ll_host")
        self.ll_ws_port = self.bot.get_config("config", "music", "ll_port")
        self.ll_password = self.bot.get_config("config", "music", "ll_password")

    async def node_init(self):
        """Initialize LavaLink Node"""
        try:
            await lavalink.initialize(
                bot=self.bot, host=self.ll_ip, ws_port=self.ll_ws_port, password=self.ll_password
            )
            self.bot.logger.info(
                f"Initialized LavaLink Node\nIP: {self.ll_ip}\nPort: {self.ll_ws_port}"
            )
        except:
            self.bot.logger.warning(
                "Error thrown in Music Init. This usually means theres an error in your ll credentials.\nUnloading Cog Now."
            )
            self.cog_unload()

    async def ensure_voice(self, ctx):
        """ This check ensures that the bot and command author are in the same voicechannel. """
        player = self.bot.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))

        should_connect = ctx.command.name in ('play',)

        if not ctx.author.voice or not ctx.author.voice.channel:
            raise await ctx.reply("Join a voicechannel first")

        if not player.is_connected:
            if not should_connect:
                raise await ctx.reply("Not connected")

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:  
                raise await ctx.reply("I need the `CONNECT` and `SPEAK` permissions")

            player.store('channel', ctx.channel.id)
            await ctx.guild.change_voice_state(channel=ctx.author.voice.channel, self_deaf=True)
            await player.set_volume(50)
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                raise await ctx.reply("You need to be in my voicechannel.")
                
    async def track_hook(self, event):
        if isinstance(event, lavalink.events.TrackStartEvent):

            guild_id = int(event.player.guild_id)
            if event.track.duration < 30:
                event.player.delete("currentTrackData")
                return

            cleanTitle = track_title_rx.sub("", event.track.title)

            async with aiohttp.ClientSession() as cs:
                async with cs.get('https://some-random-api.ml/lyrics', params={'title': cleanTitle}) as r:
                    rawData = await r.json()
                    if 'error' in rawData:
                        event.player.delete("currentTrackData")
                        return
                    rawData['cleanTitle'] = cleanTitle
                    event.player.store("currentTrackData", rawData)

        elif isinstance(event, lavalink.events.QueueEndEvent):
            time = 0
            while time < 60:
                if event.player.is_playing:
                    raise
                else:
                    await asyncio.sleep(1)
                    time += 1
            event.player.delete("currentTrackData")
            guild_id = int(event.player.guild_id)
            guild = self.bot.get_guild(guild_id)
            await guild.change_voice_state(channel=None)

    @commands.command(name="find", description="Finds a song by name")
    async def find(self, ctx, *, query):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not query.startswith('ytsearch:') and not query.startswith('scsearch:'):
            query = 'ytsearch:' + query

        results = await player.node.get_tracks(query)

        if not results or not results['tracks']:
            return await ctx.reply('Nothing found.')

        tracks = results['tracks'][:10]  # First 10 results

        o = ''
        for index, track in enumerate(tracks, start=1):
            track_title = track['info']['title']
            track_uri = track['info']['uri']
            o += f'`{index}.` [{track_title}]({track_uri})\n'

        embed = discord.Embed(color=0x3cab2b, description=o)
        await ctx.reply(embed=embed)

    @commands.command(aliases=['p'], name="play", description="Plays a song by URL or Song name")
    async def play(self, ctx, *, query: str):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        query = query.strip('<>')

        if not url_rx.match(query):
            query = f'ytsearch:{query}'

        results = await player.node.get_tracks(query)

        if not results or not results['tracks']:
            return await ctx.reply('Nothing found!')

        embed = discord.Embed(color=0x3cab2b)

        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']

            for track in tracks:
                player.add(requester=ctx.author.id, track=track)

            embed.title = 'Playlist Enqueued!'
            embed.description = f'{results["playlistInfo"]["name"]} - {len(tracks)} tracks'
        else:
            track = results['tracks'][0]
            embed.title = 'Track Enqueued'
            embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})'
            embed.add_field(name="Channel", value=track["info"]["author"], inline=False)
            embed.set_thumbnail(url=f"https://i.ytimg.com/vi/{track['info']['identifier']}/hqdefault.jpg")
            embed.timestamp = datetime.datetime.utcnow()

            track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
            player.add(requester=ctx.author.id, track=track)

        await ctx.reply(embed=embed)
        # the current track.
        if not player.is_playing:
            await player.play()

    @commands.command(aliases=['np', 'playing'], name="now", description="Shows the currently playing track")
    async def now(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.current:
            return await ctx.reply("Nothing is playing.")

        position = lavalink.utils.format_time(player.position)
        if player.current.stream:
            duration = '🔴 LIVE'
        else:
            duration = lavalink.utils.format_time(player.current.duration)
        track = f'**[{player.current.title}]({player.current.uri})**\n({position}/{duration})'

        embed = discord.Embed(color=0x3cab2b, title="Now Playing", description=track)

        currentTrackData = player.fetch("currentTrackData")
        if currentTrackData != None:
            embed.set_thumbnail(url=currentTrackData["thumbnail"]["genius"])
            embed.description += f"\n[LYRICS]({currentTrackData['links']['genius']}) | [ARTIST](https://genius.com/artists/{currentTrackData['author'].replace(' ', '%20')})"

        await ctx.reply(embed=embed)

    @commands.command(aliases=['q'], name="queue", description="Shows the player's queue")
    async def queue(self, ctx, page: int = 1):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        playerQueueWithCurrent = [player.current] + player.queue

        if not playerQueueWithCurrent:
            return await ctx.reply('Nothing queued.')

        items_per_page = 10
        pages = math.ceil(len(playerQueueWithCurrent) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue_list = ''
        for index, track in enumerate(playerQueueWithCurrent[start:end], start=start):
            queue_list += f'`{index + 1}.` [**{track.title}**]({track.uri})\n'

        embed = discord.Embed(colour=0xae7cf9,
                              description=f'**{len(playerQueueWithCurrent)} tracks**\n\n{queue_list}')
        embed.set_footer(text=f'Viewing page {page}/{pages}')
        await ctx.reply(embed=embed)

    @commands.command(aliases=['vol'], name="volume", description="Changes the bot volume (1-100)")
    async def volume(self, ctx, volume: int = None):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not volume:
            return await ctx.reply(f'🔈 | {player.volume * 2}%')
        volume = max(1, min(volume, 100))

        await player.set_volume(volume / 2)
        await ctx.reply(f'🔈 | Set to {player.volume * 2}%')

    @commands.command(name="shuffle", description="Shuffles the player's queue")
    async def shuffle(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            return await ctx.reply('Nothing playing.')

        player.shuffle = not player.shuffle
        await ctx.reply('🔀 | Shuffle ' + ('enabled' if player.shuffle else 'disabled'))

    @commands.command(aliases=['loop'], name="loop", description="Repeats the current song until the command is invoked again")
    async def repeat(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.reply('Nothing playing.')

        player.repeat = not player.repeat
        await ctx.reply('🔁 | Repeat ' + ('enabled' if player.repeat else 'disabled'))

    @commands.command(name="seek", description="Seeks to a given position in a track")
    async def seek(self, ctx, *, seconds: int):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        track_time = player.position + (seconds * 1000)
        await player.seek(track_time)

        await ctx.reply(f'Moved track to **{lavalink.utils.format_time(track_time)}**')

    @commands.command(aliases=['resume', 'unpause'], name="pause/resume", description="Pauses/Resumes the current track")
    async def pause(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.reply('Not playing.')

        if player.paused:
            await player.set_pause(False)
            await ctx.reply('⏯ | Resumed')
        else:
            await player.set_pause(True)
            await ctx.reply('⏯ | Paused')

    @commands.command(name="skip", description="Skips the current track")
    async def skip(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        await player.skip()
        await ctx.reply('⏭ | Skipped.')

    @commands.command(aliases=['dc', 'stop'], name="dc", description="Disconnects the player from the voice channel and clears its queue")
    async def disconnect(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):

            return await ctx.reply('You\'re not in my voicechannel!')

        player.queue.clear()
        await player.stop()
        await ctx.guild.change_voice_state(channel=None)
        embed = discord.Embed(color=0x3cab2b, title="Meifwa Disconnected", description="Meifwa has disconnected from the voice channel")
        await ctx.reply(embed=embed)
    
    @commands.command(aliases=['re'], name="remove", description="Removes a song from playlist")
    async def remove(self, ctx, index: int):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.queue:
            return await ctx.send('Nothing queued.')

        if index > len(player.queue) or index < 1:
            return await ctx.send('Index has to be >=1 and <=queue size')

        index = index - 1
        removed = player.queue.pop(index)
        await ctx.send('Removed **' + removed.title + '** from the queue.')

def setup(bot):
    bot.add_cog(Music(bot))