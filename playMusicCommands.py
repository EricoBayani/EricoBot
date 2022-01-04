# playMusicCommands.py
import pafy
import vlc

from config import *

pafy.set_api_key(yt_key)

# https://stackoverflow.com/a/66116633 for the audio streaming options
music_queue = queue.Queue(50)

def playQueue(error=None):
    if error is not None:
        print(error)
    if music_queue.empty():
        return
    nextItem = music_queue.get()
    nexturl = nextItem[1]
    vc = nextItem[2]
    print("Next item: {}".format(nextItem[0]))
    vc.play(discord.FFmpegPCMAudio(source=nextItem[1], executable='C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe',
                                           before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',options='-vn'), after=playQueue)        

    
@bot.command(name='play', help='play audio from a youtube link')
async def play(ctx, url = None):
    
    video = pafy.new(url)

    audiostream = video.getbestaudio()
    playurl = audiostream.url

    print('Attempting to play linked music')
    # Gets voice channel of message author

    if url is None:
        no_url_message = await ctx.send("There is no URL")
        await sent_message.delete(delay=3)
        return
    print (str(ctx.author) + " played used a command")
    voice_channel = ctx.author.voice
    vc = ctx.voice_client
    if voice_channel != None:

        if vc is None:
            vc = await voice_channel.channel.connect()
        print(music_queue.empty())
        
        if vc.is_playing():
            music_queue.put((url, playurl, vc))
            await ctx.send("Link: {} added to queue, position#{}".format(url,music_queue.qsize()))

        else:
            music_queue.put((url, playurl, vc))
            await ctx.send('**Now playing:** {}'.format(url))
            playQueue(ctx)
        
    else:
        sent_message = await ctx.send(str(ctx.author.name) + " is not in a channel.")
        await sent_message.delete(delay=5)
    # Delete command after the audio is done playing.
    
    await ctx.message.delete()

# playerCommand is a template function for controlling the bot who's currently playing music
# Input:
# ctx: discord context
# vc: voice channel object from context
# callback: what function to use i.e. vc.pause(), vc.resume()
# oppositeState: what to check to avoid contradiction i.e. isPlaying() is opposite state to pause() command
# errorString: message about the state and why it can't happen i.e. User tried to pause already paused video

async def playerCommand(ctx, callback, errorString="Can't do that yet"):
    print('messing with player')

    # Gets voice channel of message author

    print (str(ctx.author) + " played used a command")
    voice_channel = ctx.author.voice
    channel = None

    if voice_channel != None:
        vc = ctx.voice_client
        # if not oppositeState:
        try:
            callback()
        except Exception:
            await vc.disconnect()
            logging.warning('Failed vc.pause function')
            print('Failed vc.pause function')
        # else:
        #     sent_message = await ctx.send(errorString)
        #     await sent_message.delete(delay=5)        
    else:
        sent_message = await ctx.send(str(ctx.author.name) + " is not in a channel.")
        await sent_message.delete(delay=5)
    # Delete command after the audio is done playing.
    # await ctx.message.delete()
    
@bot.command(name='pause', help='pause the bot playing something')
async def pause(ctx):
    print("pausing")
    vc = ctx.voice_client
    await playerCommand(ctx, vc.pause, "Can't pause already paused song")
    await ctx.message.delete()

@bot.command(name='stop', help='stop the music bot')
async def stop(ctx):
    print("stopping")
    vc = ctx.voice_client
    await playerCommand(ctx, vc.stop, "Can't stop audio that is not connected to channel")
    await ctx.message.delete()

@bot.command(name='resume', help='resume the music bot')
async def resume(ctx):
    print("resuming")
    vc = ctx.voice_client
    await playerCommand(ctx, vc.resume, "Can't resume audio that is not connected to channel")
    await ctx.message.delete()
                      
@bot.command(name='leave', help="tell the bot to leave the command because I'm too lazy to find out where to put a time out")
async def leave(ctx):
    print("leaving channel")
    await ctx.voice_client.disconnect()
    await ctx.message.delete()
    
