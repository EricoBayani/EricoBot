import youtube_dl
import yt_dlp
import re
from Config import *
# import queue
import asyncio
import os.path

import re


class TaggedAudioSource(discord.FFmpegPCMAudio):

    def __init__(self, source_path, before_options = '', options = '-vn', tag=''):
        super().__init__(source_path, before_options=before_options, options=options)
        self.tag = tag

# The AudioPlayer should be the only thing playing audio sources, and so audio commands should feed into the AudioPlayer. 
# The AudioPlayer should also be the only thing connected to voice. It should be in charge of its own voice channel connection.
class AudioPlayer:
    # https://stackoverflow.com/a/66116633 for the audio streaming options

    def __init__(self, bot, ctx, logger = None):
        self.bot = bot
        self.logger = logger
        self.music_queue = queue.Queue(m_queue_size)
        self.music_queue_timeout = voice_timeout
        self.music_queue_time = 0.0
        self.ctx = ctx
        self.vc = None


    @tasks.loop(seconds=2.0, count=None)
    async def playQueue(self):


        if self.vc != None and not self.vc.is_playing() and not self.music_queue.empty():
            self.music_queue_time = 0.0

            print('Grabbing a new song')
            print (f'queue location in memory: {hex(id(self.music_queue))}')
            nextItem = self.music_queue.get()

            ffmpeg_err = open("ffmpeg_log.txt", "w")
            source = nextItem
            source.stderr = ffmpeg_err
            self.vc.play(source, after=lambda e: print(f'Player error: {e}') if e else None, fec=False, signal_type='music')
            ffmpeg_err.close()

        else:

            print(f'self.vc: {str(type(self.vc))}, queue size: {self.music_queue.qsize()}')
            print (f'queue location in memory: {hex(id(self.music_queue))}')
            if self.music_queue.empty() and not self.vc.is_playing():
                self.music_queue_time += 1.0
                print(f'timing out after {self.music_queue_timeout - self.music_queue_time}')
            if self.music_queue_time == self.music_queue_timeout:
                print('timeout reached, disconnecting from voice client and stopping loop')

                await self.vc.disconnect()
                self.vc = None
                self.ctx = None
                self.playQueue.stop()


    @playQueue.before_loop
    async def before_playQueue(self):
        print('Waiting')
        if self.music_queue.empty():
            print('Queue was empty before playQueue loop began')
            self.playQueue.cancel()
        await self.bot.wait_until_ready()
        print('Stopped waiting')

    async def place_in_queue(self, ctx, source):
        self.vc = ctx.voice_client
        if self.vc == None:
            self.vc = await ctx.author.voice.channel.connect()

        if self.vc.is_playing():
            self.music_queue.put(source)
            await ctx.send("Source: {} added to queue, position# {}".format(source.tag,self.music_queue.qsize()))
            
        else:
            self.music_queue.put(source)
            await ctx.send('**Now playing:** {}'.format(source.tag))
            if not self.playQueue.is_running():
                await self.playQueue.start()


    # playerCommand is a template function for controlling the bot who's currently playing music
    # Input:
    # ctx: discord context
    # vc: voice channel object from context
    # callback: what function to use i.e. vc.pause(), vc.resume()
    # oppositeState: what to check to avoid contradiction i.e. isPlaying() is opposite state to pause() command
    # errorString: message about the state and why it can't happen i.e. User tried to pause already paused video
    async def playerCommand(self, ctx, callback, errorString="Can't do that yet"):
        print('messing with player')

        print(str(ctx.author) + " played used a command")
        voice_channel = ctx.author.voice
        channel = None

        if voice_channel != None:
            self.vc = ctx.voice_client

            try:
                callback()
            except Exception:
                await self.vc.disconnect()
                logging.error('Failed vc callback function')
                sent_message = await ctx.send(errorString)
                await sent_message.delete(delay=5)        

        else:
            sent_message = await ctx.send(str(ctx.author.name) + " is not in a channel.")
            await sent_message.delete(delay=5)



    async def pause(self, ctx):
        print("pausing")
        await self.playerCommand(ctx, self.vc.pause, "Can't pause already paused song")
        self.playQueue.cancel() 



    async def stop(self, ctx):
        print("stopping")

        await self.playerCommand(ctx, self.vc.stop, "Can't stop audio that is not connected to channel")
        if not self.music_queue.empty():
            self.music_queue = queue.Queue(m_queue_size)


    async def skip(self, ctx):
        print("skipping")

        await self.playerCommand(ctx, self.vc.stop, "Can't stop audio that is not connected to channel")
        

    async def resume(self, ctx):
        print("resuming")

        await self.playerCommand(ctx, self.vc.resume, "Can't resume audio that is not connected to channel")
        self.playQueue.restart()



    async def leave(self, ctx):
        print("leaving channel")

        await ctx.voice_client.disconnect()
        self.playQueue.cancel()
        self.vc = None
        if not self.music_queue.empty():
            self.music_queue = queue.Queue(m_queue_size)
