import os
import random as rand
import time
import logging
import queue
# import multiprocessing
import asyncio

import discord 
from discord.ext import commands
from dotenv import load_dotenv


logging.basicConfig(filename='debug.log', level=logging.WARNING)

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

yt_key = os.getenv('YT_KEY')

bot = commands.Bot(command_prefix=[regular_prefix, regular_prefix_lower, kent_prefix, kent_prefix_lower], case_insensitive=True)

