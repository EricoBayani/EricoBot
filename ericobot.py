# bot.py


# from datetime import datetime
# from json_writer import JSON_Writer
import sys

#local modules
from config import *
from audioClipCommands import ClipPlayer
from askCommands import AskWiki
from playMusicCommands import LinkPlayer

bot = commands.Bot(command_prefix=[regular_prefix, regular_prefix_lower, kent_prefix, kent_prefix_lower, '!e '], case_insensitive=True)


@bot.event
async def on_ready():
    print('Current Python version is ', sys.version)
    print(f'{bot.user.name} has connected to Discord!')    

def main():
    bot.add_cog(LinkPlayer(bot))
    bot.add_cog(ClipPlayer(bot))
    bot.add_cog(AskWiki(bot))
    bot.run(TOKEN)
    print("Bot is online")    
    
if __name__ == '__main__':
    main()

