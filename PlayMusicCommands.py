# playMusicCommands.py
# import vlc
# import youtube_dl
import yt_dlp
import json
import re
from Config import *
from AudioPlayer import TaggedAudioSource, AudioPlayer
import queue
import os.path

import re


# Options and youtube_dl construct shamelessly stolen from
# Rapptz basic_voice example
# https://github.com/Rapptz/discord.py/blob/master/examples/basic_voice.py
# Suppress noise about console usage from errors
# youtube_dl.utils.bug_reports_message = lambda: ''


ydl_opts = {
    'format': 'm4a/bestaudio/best',
    # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
    }],
    'default_search': 'ytsearch3'
}

ffmpeg_options = {
    'options': '-vn -filter:a',
    'before_options':'-reconnect 1 -reconnect_at_eof 1 -reconnect_streamed 1 -reconnect_delay_max 7'
}



class LinkPlayer(commands.Cog):
    # https://stackoverflow.com/a/66116633 for the audio streaming options

    def __init__(self, bot, logger = None, audioplayers = None):
        self.bot = bot
        self.logger = logger
        self.music_queue = queue.Queue(m_queue_size)
        self.music_queue_timeout = voice_timeout
        self.music_queue_time = 0.0
        self.vc = None
        # TODO: should it be a fatal exception if audioplayer is None? It shouldn't happen, 
        # but if it does wouldn't it be good if I fixed the global audio player? 
        self.audioplayers = audioplayers

    
    @commands.command(name='play', help='play audio from a youtube link or from regular words wrapped around in quotes')
    async def play(self, ctx, *query):

        self.logger.debug('Attempting to play linked music')
        await ctx.typing()
        
        voice = ctx.author.voice

        if voice is None:
            sent_message = await ctx.send(str(ctx.author.name) + " is not in a channel.")
            await sent_message.delete(delay=5)
            return

        self.logger.debug(query)
        if not query:
            no_url_message = await ctx.send("There is no query")
            self.logger.debug('there was no query')
            await no_url_message.delete(delay=3)
            return

        query = ' '.join(query)
        # At some point here, I want to make find out whether the query is
        # a URL or a search query. If it's a URL, we can just skip to playing
        # the link. Otherwise, we'd need to present the channel with options
        # to play. 
        print (str(ctx.author) + " played used a command")
        

        with yt_dlp.YoutubeDL(ydl_opts) as ytdl:
        
            info = ytdl.extract_info(query, download=False)

            if 'entries' in info:
                self.logger.debug("There were multiple entries to choose")

                emoji_string_one = "1\uFE0F\u20E3"
                emoji_string_two =  "2\uFE0F\u20E3"
                emoji_string_three = "3\uFE0F\u20E3"
                
                chosen_video = await ctx.send("Pick the video you want to play by reacting to this message:")
                
                await chosen_video.add_reaction(emoji_string_one)
                await chosen_video.add_reaction(emoji_string_two)
                await chosen_video.add_reaction(emoji_string_three)

                await ctx.send("{} : {}".format(emoji_string_one, info["entries"][0]["title"]))
                await ctx.send("{} : {}".format(emoji_string_two, info["entries"][1]["title"]))
                await ctx.send("{} : {}".format(emoji_string_three, info["entries"][2]["title"]))
                
                new_video = None
                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) is not None            
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=15.0, check=check)
                except asyncio.TimeoutError:
                    await ctx.send("You didn't pick in time, not gonna do anything")
                    return
                else:
                    if str(reaction.emoji) == emoji_string_one:
                        new_video = info["entries"][0]["webpage_url"]
                        info = info["entries"][0]
                    if str(reaction.emoji) == emoji_string_two:
                        new_video = info["entries"][1]["webpage_url"]
                        info = info["entries"][1]
                    if str(reaction.emoji) == emoji_string_three:
                        new_video = info["entries"][2]["webpage_url"]
                        info = info["entries"][2]                
                    await ctx.send("I will now play: {}".format(new_video))


        playurl = ''
        maxbitrate = -1;

        for i in info['formats']:
            if i['format_id'] == '18':
                playurl = i['url']
                maxbitrate = i['filesize']
                break;
        self.logger.debug(info['url'])
        self.logger.debug(info['webpage_url'])
                
        

        url = info['webpage_url']

        video_title = info['title']

        if ctx.guild.id not in self.audioplayers:
            print (ctx.guild.id)
            self.audioplayers[ctx.guild.id] = AudioPlayer(self.bot, ctx, self.logger)
            print(f"There are now {len(self.audioplayers)} audioplayers")

        await self.audioplayers[ctx.guild.id].place_in_queue(ctx, TaggedAudioSource(playurl, tag=video_title))

        return

    @commands.command(name='pause', help='pause the bot playing something')
    async def pause(self, ctx):
        await self.audioplayers[ctx.guild.id].pause(ctx)

    @commands.command(name='stop', help='stop the music bot')
    async def stop(self, ctx):
        await self.audioplayers[ctx.guild.id].stop(ctx)

    @commands.command(name='skip', help='skip current song for next in queue')
    async def skip(self, ctx):
        await self.audioplayers[ctx.guild.id].skip(ctx)
        
    @commands.command(name='resume', help='resume the music bot')
    async def resume(self, ctx):
        await self.audioplayers[ctx.guild.id].resume(ctx)

    @commands.command(name='leave', help="tell the bot to leave the command because I'm too lazy to find out where to put a time out")
    async def leave(self, ctx):
        await self.audioplayers[ctx.guild.id].leave(ctx)
