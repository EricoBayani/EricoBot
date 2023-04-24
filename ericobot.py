# bot.py


# from datetime import datetime
# from json_writer import JSON_Writer
import sys

#local modules
from config import *
from audioClipCommands import ClipPlayer
from askCommands import AskWiki
from playMusicCommands import LinkPlayer

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=[regular_prefix, regular_prefix_lower, kent_prefix, kent_prefix_lower, '!e '], case_insensitive=True, intents = intents)


@bot.event
async def on_ready():
    
    await bot.add_cog(LinkPlayer(bot))
    await bot.add_cog(ClipPlayer(bot))
    await bot.add_cog(AskWiki(bot))
    print('Current Python version is ', sys.version)
    print(f'{bot.user.name} has connected to Discord!')
    

bot.run(TOKEN)
print("Bot is online")    
    
# if __name__ == '__main__':
#     main()

