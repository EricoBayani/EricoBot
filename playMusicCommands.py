# playMusicCommands.py
import pafy
import vlc
import youtube_dl
import re
from config import *

pafy.set_api_key(yt_key)


# Options and youtube_dl construct shamelessly stolen from
# Rapptz basic_voice example
# https://github.com/Rapptz/discord.py/blob/master/examples/basic_voice.py
# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True, # turned false to try and see how ytdl works
    'no_warnings': True,
    'default_search': 'ytsearch',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)



class LinkPlayer(commands.Cog):
    # https://stackoverflow.com/a/66116633 for the audio streaming options

    def __init__(self, bot):
        self.bot = bot
        self.music_queue = queue.Queue(m_queue_size)
        self.music_queue_timeout = voice_timeout
        self.music_queue_time = 0.0
        self.vc = None


    @tasks.loop(seconds=1.0, count=None)
    async def playQueue(self):
        # print(str(self.playQueue.current_loop))
        nextItem = None
        if not self.music_queue.empty():
            if not self.vc.is_playing():
                nextItem = self.music_queue.get()
        if nextItem is None:
            if self.vc is not None:
                if not self.vc.is_playing():
                    self.music_queue_time += 1.0
                    if self.music_queue_time == self.music_queue_timeout:
                        await self.vc.disconnect()
                        self.vc = None
                        self.playQueue.stop()
        else:
            self.music_queue_time = 0.0
            if self.vc is not None:
                self.vc.play(discord.FFmpegPCMAudio(source=nextItem[1],
                        executable='C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe',
                        before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',options='-vn'))
                    
                         
    @commands.command(name='play', help='play audio from a youtube link or from regular words wrapped around in quotes')
    async def play(self, ctx, *query):

        print('Attempting to play linked music')

        print(query)
        if query is None:
            no_url_message = await ctx.send("There is no query")
            print('there was no query')
            await no_url_message.delete(delay=3)
            return

        query = ' '.join(query)
        
        print (str(ctx.author) + " played used a command")

        info = ytdl.extract_info(query, download=False)
        if 'entries' in info:
            info = info['entries'][0]

        url = info['id']

        
        video = pafy.new(url)

        audiostream = video.getbestaudio()
        playurl = audiostream.url
        
        voice = ctx.author.voice
        # self.vc = ctx.voice_client
        if voice != None:

            if self.vc is None:
                self.vc = await voice.channel.connect(timeout=voice_timeout)
            # print(self.music_queue.empty())

            if self.vc.is_playing():
                self.music_queue.put((url, playurl))
                await ctx.send("Link: {} added to queue, position#{}".format(video.title,self.music_queue.qsize()))

            else:
                self.music_queue.put((url, playurl))
                await ctx.send('**Now playing:** {}'.format(video.title))
                if not self.playQueue.is_running():
                    await self.playQueue.start()

        else:
            sent_message = await ctx.send(str(ctx.author.name) + " is not in a channel.")
            await sent_message.delete(delay=5)        

        # await ctx.message.delete()

    # playerCommand is a template function for controlling the bot who's currently playing music
    # Input:
    # ctx: discord context
    # vc: voice channel object from context
    # callback: what function to use i.e. vc.pause(), vc.resume()
    # oppositeState: what to check to avoid contradiction i.e. isPlaying() is opposite state to pause() command
    # errorString: message about the state and why it can't happen i.e. User tried to pause already paused video

    async def playerCommand(self, ctx, callback, errorString="Can't do that yet"):
        print('messing with player')

        # Gets voice channel of message author

        print (str(ctx.author) + " played used a command")
        voice_channel = ctx.author.voice
        channel = None

        if voice_channel != None:
            self.vc = ctx.voice_client

            try:
                callback()
            except Exception:
                await vc.disconnect()
                logging.warning('Failed vc callback function')
                print('Failed vc callback function')
                sent_message = await ctx.send(errorString)
                await sent_message.delete(delay=5)        

        else:
            sent_message = await ctx.send(str(ctx.author.name) + " is not in a channel.")
            await sent_message.delete(delay=5)
        # # Delete command after the audio is done playing.
        # await ctx.message.delete()

    @commands.command(name='pause', help='pause the bot playing something')
    async def pause(self, ctx):
        print("pausing")
        # vc = ctx.voice_client
        self.playQueue.stop() # this pauses the playQueue task and can be started again        
        await self.playerCommand(ctx, self.vc.pause, "Can't pause already paused song")
        
        # await ctx.message.delete()

    @commands.command(name='stop', help='stop the music bot')
    async def stop(self, ctx):
        print("stopping")
        # vc = ctx.voice_client
        await self.playerCommand(ctx, self.vc.stop, "Can't stop audio that is not connected to channel")
        # self.playQueue.cancel()
        if not self.music_queue.empty():
            self.music_queue = queue.queue(m_queue_size)
        # await ctx.message.delete()

    @commands.command(name='skip', help='skip current song for next in queue')
    async def skip(self, ctx):
        print("skipping")
        # vc = ctx.voice_client
        await self.playerCommand(ctx, self.vc.stop, "Can't stop audio that is not connected to channel")
        
    @commands.command(name='resume', help='resume the music bot')
    async def resume(self, ctx):
        print("resuming")
        # vc = ctx.voice_client
        await self.playerCommand(ctx, self.vc.resume, "Can't resume audio that is not connected to channel")
        self.playQueue.start()
        # await ctx.message.delete()

    @commands.command(name='leave', help="tell the bot to leave the command because I'm too lazy to find out where to put a time out")
    async def leave(self, ctx):
        print("leaving channel")
        await ctx.voice_client.disconnect()
        self.playQueue.cancel()
        self.vc = None
        if not self.music_queue.empty():
            self.music_queue = queue.queue(m_queue_size)
        # await ctx.message.delete()
