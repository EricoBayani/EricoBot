# playMusicCommands.py
import pafy
import vlc

from config import *

pafy.set_api_key(yt_key)

# https://stackoverflow.com/a/66116633 for the
# audio streaming clarification
@bot.command(name='play', help='play audio from a youtube link')
async def play(ctx, url = 'https://youtu.be/_2quiyHfJQw'):

    video = pafy.new(url)

    audiostream = video.getbestaudio()
    playurl = audiostream.url

    print('Attempting to play linked music')
    # Gets voice channel of message author

    print (str(ctx.author) + " played used a command")
    voice_channel = ctx.author.voice
    channel = None

    if voice_channel != None:
        channel = voice_channel.channel.name
        vc = await voice_channel.channel.connect()
        try:
            vc.play(discord.FFmpegPCMAudio(source=playurl, executable='C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe',
                                           before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',options='-vn'))
            await ctx.send('**Now playing:** {}'.format(url))
            
        except Exception:
            await vc.disconnect()
            logging.warning('Failed vc.play function')
        
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
# async def playerCommand(ctx, vc, callback, oppositeState, errorString="Can't do that yet"):
#     print('messing with player')

#     # Gets voice channel of message author

#     print (str(ctx.author) + " played used a command")
#     voice_channel = ctx.author.voice
#     channel = None

#     if voice_channel != None:
#         channel = voice_channel.channel.name
#         if !oppositeState:
#             try:
#                 callback()
#             except Exception:
#                 await vc.disconnect()
#                 logging.warning('Failed vc.pause function')
#         else:
#             sent_message = await ctx.send(errorString)
#             await sent_message.delete(delay=5)
#         # Sleep while audio is playing.
#         while vc.is_playing():
#             time.sleep(.1)
#         await vc.disconnect()
        
#     else:
#         sent_message = await ctx.send(str(ctx.author.name) + " is not in a channel.")
#         await sent_message.delete(delay=5)
#     # Delete command after the audio is done playing.
#     await ctx.message.delete()    
    
# @bot.command(name='pause', help='pause the bot playing something')
# async def pause(ctx):
#     print('Attempting to play linked music')
#     # Gets voice channel of message author

#     print (str(ctx.author) + " played used a command")
#     voice_channel = ctx.author.voice
#     channel = None

#     if voice_channel != None:
#         channel = voice_channel.channel.name
#         if vc.isplaying():
#             try:
#                 vc.pause()
#             except Exception:
#                 await vc.disconnect()
#                 logging.warning('Failed vc.pause function')
#         else:
#             sent_message = await ctx.send("Can't do that yet")
#             await sent_message.delete(delay=5)
#         # Sleep while audio is playing.
#         while vc.is_playing():
#             time.sleep(.1)
#         await vc.disconnect()
        
#     else:
#         sent_message = await ctx.send(str(ctx.author.name) + " is not in a channel.")
#         await sent_message.delete(delay=5)
#     # Delete command after the audio is done playing.
#     await ctx.message.delete()
# @bot.command(name='stop', help='stop the music bot')
# async def stop(ctx):
#     voice_channel = ctx.author.voice
#     vc = 
#     await playerCommand(ctx, 
