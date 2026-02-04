import youtube_dl
import yt_dlp
import re
from Config import *
import queue
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

    def __init__(self, bot):
        self.bot = bot
        self.music_queue = queue.Queue(m_queue_size)
        self.music_queue_timeout = voice_timeout
        self.music_queue_time = 0.0
        self.vc = None


    @tasks.loop(seconds=2.0, count=None)
    async def playQueue(self):

        logger.debug(str(self.playQueue.current_loop))

        nextItem = None
        if not self.music_queue.empty():
            logger.debug('Queue is not empty')

            if not self.vc.is_playing():
                logger.debug('Grabbing a new song')

                nextItem = self.music_queue.get()
        if nextItem is None:
            logger.debug('no new item yet')

            if self.vc is not None:
                logger.debug('voice client still connected')

                if not self.vc.is_playing():
                    logger.debug('voice client still not playing audio')

                    self.music_queue_time += 1.0
                    if self.music_queue_time == self.music_queue_timeout:
                        logger.debug('timeout reached, disconnecting from voice client and stopping loop')

                        await self.vc.disconnect()
                        self.vc = None
                        self.playQueue.stop()
                    
        else:
            logger.debug('resetting timeout')

            self.music_queue_time = 0.0
            if self.vc is not None:
                logger.debug('playing')

                ffmpeg_err = open("ffmpeg_log.txt", "w")
                source = nextItem
                source.stderr = ffmpeg_err
                self.vc.play(source, after=lambda e: print(f'Player error: {e}') if e else None, fec=False, signal_type='music')
                ffmpeg_err.close()

    @playQueue.before_loop
    async def before_playQueue(self):
        logger.debug('Waiting')
        if self.music_queue.empty():
            logger.debug('Queue was empty before playQueue loop began')
            playQueue.cancel()
        await self.bot.wait_until_ready()
        logger.debug('Stopped waiting')

    async def place_in_queue(self, ctx, source):

        if self.vc is None:
            self.vc = ctx.voice_client

        if self.vc.is_playing():
            self.music_queue.put(source)
            await ctx.send("Source: {} added to queue, position#{}".format(source.tag,self.music_queue.qsize()))

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
        logger.debug('messing with player')

        logger.debug(str(ctx.author) + " played used a command")
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
        logger.debug("pausing")
        await self.playerCommand(ctx, self.vc.pause, "Can't pause already paused song")
        self.playQueue.cancel() 



    async def stop(self, ctx):
        logger.debug("stopping")

        await self.playerCommand(ctx, self.vc.stop, "Can't stop audio that is not connected to channel")
        if not self.music_queue.empty():
            self.music_queue = queue.Queue(m_queue_size)


    async def skip(self, ctx):
        logger.debug("skipping")

        await self.playerCommand(ctx, self.vc.stop, "Can't stop audio that is not connected to channel")
        

    async def resume(self, ctx):
        logger.debug("resuming")

        await self.playerCommand(ctx, self.vc.resume, "Can't resume audio that is not connected to channel")
        self.playQueue.restart()



    async def leave(self, ctx):
        logger.debug("leaving channel")

        await ctx.voice_client.disconnect()
        self.playQueue.cancel()
        self.vc = None
        if not self.music_queue.empty():
            self.music_queue = queue.Queue(m_queue_size)
