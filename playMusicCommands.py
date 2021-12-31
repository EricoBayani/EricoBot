# playMusicCommands.py
import pafy
import vlc

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

    filename = audiostream.download()
    # instance = vlc.Instance()
    # player = instance.media_player_new()
    # media = instance.media_new(playurl)
    # media.get_mrl()
    # print(instance.audio_output_list_get())
    # player.set_media(media)
    
    print('Attempting to play linked music')
    # Gets voice channel of message author

    print (str(ctx.author) + " played used a command")
    voice_channel = ctx.author.voice
    channel = None

    if voice_channel != None:
        channel = voice_channel.channel.name
        vc = await voice_channel.channel.connect()
        try:
            vc.play(discord.FFmpegPCMAudio(source=filename, executable='C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe', pipe=True))
            await ctx.send('**Now playing:** {}'.format(filename))
            
        except Exception:
            await vc.disconnect()
            logging.warning('Failed vc.play function')
        # Sleep while audio is playing.
        while vc.is_playing():
            time.sleep(.1)
        await vc.disconnect()
        
    else:
        sent_message = await ctx.send(str(ctx.author.name) + " is not in a channel.")
        await sent_message.delete(delay=5)
    # Delete command after the audio is done playing.
    await ctx.message.delete()

    # player.release()
    # instance.release()
