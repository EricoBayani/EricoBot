import os
import random as rand
import time
import discord 
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
regular_prefix = 'EricoPls '
regular_prefix_lower = regular_prefix.lower()
kent_prefix = 'KentSucks '
kent_prefix_lower = kent_prefix.lower()

brick = os.getenv('BRICK')
dix = os.getenv('DIX')
kintorola = os.getenv('KINTOROLA')

local_path = "C:\\Programming_Stuff\\Python Programs\\EricoBot\\resources\\"

# local_cache_writer = JSON_Writer()

bot = commands.Bot(command_prefix=[regular_prefix, regular_prefix_lower, kent_prefix, kent_prefix_lower], case_insensitive=True)

