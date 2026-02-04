# bot.py


# from datetime import datetime
# from json_writer import JSON_Writer
import sys
import os
#local modules
from Config import *
from discord import app_commands
from AudioPlayer import AudioPlayer
from AudioClipCommands import ClipPlayer
from AskCommands import AskWiki
from PlayMusicCommands import LinkPlayer

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=[regular_prefix, regular_prefix_lower, kent_prefix, kent_prefix_lower, '!e '], case_insensitive=True, intents = intents)

audioplayer = AudioPlayer(bot)

@bot.event
async def on_ready():
    # await bot.add_cog(AudioPlayer(bot))
    await bot.add_cog(LinkPlayer(bot, audioplayer))
    await bot.add_cog(ClipPlayer(bot, audioplayer))
    # await bot.add_cog(AskWiki(bot))
    assert bot.user is not None
    print('Current Python version is ', sys.version)
    print(f'{bot.user} (ID: {bot.user.id}) has connected to Discord!')
    print(os.getcwd())
    
def main():
    logger.setLevel(logging.DEBUG)

    bot.run(TOKEN)
    print("Bot is online")

if __name__ == '__main__':
    main()

