# bot.py
import os
import random as rand
import time
import discord 
from discord.ext import commands
from dotenv import load_dotenv

import wikipediaapi as wiki

from datetime import datetime
from json_writer import JSON_Writer

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

brick = os.getenv('BRICK')
dix = os.getenv('DIX')
kintorola = os.getenv('KINTOROLA')

local_path = "C:\\Programming_Stuff\\Python Programs\\EricoBot\\resources\\"

regular_prefix = 'EricoPls '
regular_prefix_lower = regular_prefix.lower()
kent_prefix = 'KentSucks '
kent_prefix_lower = kent_prefix.lower()

local_cache_writer = JSON_Writer()

bot = commands.Bot(command_prefix=[regular_prefix, regular_prefix_lower, kent_prefix, kent_prefix_lower], case_insensitive=True)

# dict for making sure days are counted once
# tuple[0] means today is that day
# tuple[1] means today was not already that day
days_dict = {"":(False,False),
             "":(False,False),
             "":(False,False),
             "":(False,False),
             "":(False,False),
             "":(False,False),
             "":(False,False),
             "":(False,False),}

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await setup_days_json()

        


async def setup_days_json():
    print("Setting up days JSON")
    isSaturday = False
    wasSaturday = False
    #check if this key exists
    if local_cache_writer.checkKey("Saturday") is False:
        local_cache_writer.addPair("Saturday", False)
    else:
        wasSaturday = local_cache_writer.getPair("Saturday")
        # is today Saturday?
        if datetime.today().weekday() == 5:
            isSaturday = True
        else:
            isSaturday = False

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

@bot.command(name='ask', help='for now, it just spits back the question string,'
             'but will someday return a link to a kind of relavant page'
             'Please use quotes around a query that uses more than 1 word\n'
             'Example: EricoPls ask "League of Legends"')
async def ask(ctx, query):
    sent_messages = []
    echo = 'you asked {}'.format(query)
    print("***"+echo+"***")
    wikipedia = wiki.Wikipedia(language='en')
    wikipedia_query = None
    # try:
    wikipedia_query = wikipedia.page((str(query)))

    # except wikipedia.exceptions.DisambiguationError as e:
    #     wikipedia_query = wikipedia.page(e.options[0])
    if rand.random() > 0.9:
        sent_messages.append(await ctx.send('***you know,'
                                            'I actually did get the answer you\'re looking for'
                                            ', but here\'s cbt instead~~~***'))
        wikipedia_query=wikipedia.page('Cock and ball torture')    
    sent_messages.append(await ctx.send("***"+echo+"***"))
    answer_message = ((wikipedia_query.summary.split('.')))[0:2]
    if wikipedia_query is None or not answer_message[0]:
        sent_messages.append(await ctx.send('**Sorry, I couldn\'t find the page you are looking for**.'
                                            '**Here\'s CBT instead!!!**'))
        wikipedia_query=wikipedia.page('Cock and ball torture')        
    print (answer_message)
    sent_messages.append(await ctx.send('***' + answer_message[0] + '!' + '***'))
    sent_messages.append(await ctx.send("***Learn more at this link!\n***" + str(wikipedia_query.canonicalurl)))
    for msg in sent_messages:
        await msg.delete(delay=20)
    await ctx.message.delete(delay=20)
bot.run(TOKEN)
print("The bot is really online!")
