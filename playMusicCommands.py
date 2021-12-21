# playMusicCommands.py
import pafy


from config import *
@bot.command(name='play', help='play audio from a youtube link')
async def play(ctx, url = 'https://youtu.be/_2quiyHfJQw'):
    # video = None
    # try :
    video = pafy.new(url)
    # except KeyError:
    #     pass
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
            vc.play(discord.FFmpegPCMAudio(source=playurl, executable='C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe', pipe=True))
        except Exception:
            vc.disconnect()
        # Sleep while audio is playing.
        while vc.is_playing():
            time.sleep(.1)
        await vc.disconnect()
        
    else:
        sent_message = await ctx.send(str(ctx.author.name) + " is not in a channel.")
        await sent_message.delete(delay=5)
    # Delete command after the audio is done playing.
    await ctx.message.delete()    
