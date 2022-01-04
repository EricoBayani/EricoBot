# bot.py


# from datetime import datetime
# from json_writer import JSON_Writer


#local modules
from config import *
from audioClipCommands import *
from askCommands import *
from playMusicCommands import *

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

def main():
    bot.run(TOKEN)
    print("Bot is online")    
    
if __name__ == '__main__':
    main()
