# playMusicCommands.py
import pafy
import vlc

from config import *

pafy.set_api_key(yt_key)


class LinkPlayer(commands.Cog):
    # https://stackoverflow.com/a/66116633 for the audio streaming options

    def __init__(self, bot):
        self.bot = bot
        self.music_queue = queue.Queue(50)
        self.music_queue_timeout = voice_timeout
        self.music_queue_time = 0.0
        self.vc = None

    # def playQueue(self, error=None):
    #     if error is not None:
    #         print(error)
    #     if not self.music_queue.empty():

    #         nextItem = self.music_queue.get()
    #         nexturl = nextItem[1]
    #         # vc = nextItem[2]
    #         print("Next item: {}".format(nextItem[0]))
    #         self.vc.play(discord.FFmpegPCMAudio(source=nextItem[1],
    #                                    executable='C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe',
    #                                    before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',options='-vn'),
    #             after=self.playQueue)
    #     else:
    #         if not self.vc.is_playing():
    #             self.vc.disconnect()

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
            
            self.vc.play(discord.FFmpegPCMAudio(source=nextItem[1],
                        executable='C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe',
                        before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',options='-vn'))
                    
            # await self.vc.disconnect()
            # self.vc = None
            # self.playQueue.stop()
            
                         
        # await self.vc.disconnect()
    
    # async def leaveQueue(self):
    #     if not self.vc.is_playing():
    #         if self.music_queue.empty():
    #             await vc.disconnect()
                         
    @commands.command(name='play', help='play audio from a youtube link')
    async def play(self, ctx, url = None):
        # print(ctx)
        # print(ctx.author)
        # print(ctx.author.voice)
        # print(ctx.author.voice.channel)
        video = pafy.new(url)

        audiostream = video.getbestaudio()
        playurl = audiostream.url

        print('Attempting to play linked music')

        if url is None:
            no_url_message = await ctx.send("There is no URL")
            await sent_message.delete(delay=3)
            return

        print (str(ctx.author) + " played used a command")
        voice = ctx.author.voice
        # self.vc = ctx.voice_client
        if voice != None:

            if self.vc is None:
                self.vc = await voice.channel.connect(timeout=voice_timeout)
            print(self.music_queue.empty())

            if self.vc.is_playing():
                self.music_queue.put((url, playurl))
                await ctx.send("Link: {} added to queue, position#{}".format(url,self.music_queue.qsize()))

            else:
                self.music_queue.put((url, playurl))
                await ctx.send('**Now playing:** {}'.format(url))
                await self.playQueue.start()

        else:
            sent_message = await ctx.send(str(ctx.author.name) + " is not in a channel.")
            await sent_message.delete(delay=5)        

        await ctx.message.delete()

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
                logging.warning('Failed vc.pause function')
                print('Failed vc.pause function')
                sent_message = await ctx.send(errorString)
                await sent_message.delete(delay=5)        

        else:
            sent_message = await ctx.send(str(ctx.author.name) + " is not in a channel.")
            await sent_message.delete(delay=5)
        # Delete command after the audio is done playing.
        await ctx.message.delete()

    @commands.command(name='pause', help='pause the bot playing something')
    async def pause(self, ctx):
        print("pausing")
        # vc = ctx.voice_client
        await playerCommand(ctx, self.vc.pause, "Can't pause already paused song")
        # await ctx.message.delete()

    @commands.command(name='stop', help='stop the music bot')
    async def stop(self, ctx):
        print("stopping")
        # vc = ctx.voice_client
        await playerCommand(ctx, self.vc.stop, "Can't stop audio that is not connected to channel")
        # await ctx.message.delete()

    @commands.command(name='resume', help='resume the music bot')
    async def resume(self, ctx):
        print("resuming")
        # vc = ctx.voice_client
        await playerCommand(ctx, self.vc.resume, "Can't resume audio that is not connected to channel")
        # await ctx.message.delete()

    @commands.command(name='leave', help="tell the bot to leave the command because I'm too lazy to find out where to put a time out")
    async def leave(self, ctx):
        print("leaving channel")
        await ctx.voice_client.disconnect()
        # await ctx.message.delete()
