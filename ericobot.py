# bot.py
import os
import random as rand
import time
import discord 
from discord.ext import commands
from dotenv import load_dotenv

import wikipediaapi as wiki

from datetime import datetime
# from json_writer import JSON_Writer

#commands
import audioClipCommands
TOKEN = os.getenv('DISCORD_TOKEN')


regular_prefix = 'EricoPls '
regular_prefix_lower = regular_prefix.lower()
kent_prefix = 'KentSucks '
kent_prefix_lower = kent_prefix.lower()

# local_cache_writer = JSON_Writer()

bot = commands.Bot(command_prefix=[regular_prefix, regular_prefix_lower, kent_prefix, kent_prefix_lower], case_insensitive=True)

# dict for making sure days are counted once
# tuple[0] means today is that day
# tuple[1] means today was not already that day
# days_dict = {"":(False,False),
#              "":(False,False),
#              "":(False,False),
#              "":(False,False),
#              "":(False,False),
#              "":(False,False),
#              "":(False,False),
#              "":(False,False),}

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    # await setup_days_json()

        


# async def setup_days_json():
#     print("Setting up days JSON")
#     isSaturday = False
#     wasSaturday = False
#     #check if this key exists
#     if local_cache_writer.checkKey("Saturday") is False:
#         local_cache_writer.addPair("Saturday", False)
#     else:
#         wasSaturday = local_cache_writer.getPair("Saturday")
#         # is today Saturday?
#         if datetime.today().weekday() == 5:
#             isSaturday = True
#         else:
#             isSaturday = False


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
