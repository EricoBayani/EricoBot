# audioClipCommands.py

from config import *

# load_dotenv()

# a generic command that will play any sound file into
# voice when passed a file path to the sound.
async def play_audio(ctx, source_file):
    print('Attempting to play sound')
    # Gets voice channel of message author

    print (str(ctx.author) + " played used a command")
    voice_channel = ctx.author.voice
    channel = None

    # print(type(voice_channel))

    if voice_channel != None:
        channel = voice_channel.channel.name
        vc = await voice_channel.channel.connect()
        vc.play(discord.FFmpegPCMAudio(source=source_file, executable='C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe'))
        
        # Sleep while audio is playing.
        while vc.is_playing():
            time.sleep(.1)
        await vc.disconnect()
        
    else:
        sent_message = await ctx.send(str(ctx.author.name) + " is not in a channel.")
        await sent_message.delete(delay=5)
    # Delete command after the audio is done playing.
    await ctx.message.delete()
    
@bot.command(name='airhorn', help='play an airhorn sound in voice')
async def play_airhorn(ctx):

    await play_audio(ctx, local_path + "mlg-airhorn.mp3")

# jokes dictionary for easy random selection    
jokes_dict = {}
jokes_dict["brick_sucks"] = local_path + "brick-sucks.mp3"
    
@bot.command(name='joke', help='Play a funny prerecorded haha joke for the whole family!')
async def make_joke(ctx):
        
    joke_choice = rand.choice(list(jokes_dict.items()))

    await play_audio(ctx, joke_choice[1])
@bot.command(name='scarra_laugh', help='Play the laugh of the venerable Scarra!')    
async def scarra_laugh(ctx):

    await play_audio(ctx, local_path + "scarra-laugh.mp3")
@bot.command(name='chug', help='NUMER ONE VICOTRY ROYAEL')    
async def chugjug(ctx):

    if rand.random() > 0.5:
        if str(ctx.author) == kintorola:
            print ("Nah")
            await play_audio(ctx, local_path + "no.mp3")
        elif str(ctx.author) == brick:
            print ("lol_getrekt")
            await play_audio(ctx, local_path + "existence.mp3")
        elif str(ctx.author) == dix:
            print ("lol_usuckkek")
            await play_audio(ctx, local_path + "man-oth.mp3")            
        else:
            await play_audio(ctx, local_path + "my-chugjug-with-you.mp3")
            
    else:
        await play_audio(ctx, local_path + "chugjug-with-me.mp3")

@bot.command(name='got_downed', help='plays a fun message for when your friend gets downed')    
async def got_downed(ctx):

    await play_audio(ctx, local_path + "got-downed.mp3")

@bot.command(name='cbt', help='plays a funny audio clip of a well known form of play')    
async def cbt(ctx):
    await play_audio(ctx, local_path + "cbt-lol.mp3")

@bot.command(name='mychug', help='plays a funny audio clip of me singing a hit song')    
async def cbt(ctx):
    await play_audio(ctx, local_path + "my-chugjug-with-you.mp3")        
