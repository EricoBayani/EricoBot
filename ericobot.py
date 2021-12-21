# bot.py


# from datetime import datetime
# from json_writer import JSON_Writer


#local modules
from config import *
from audioClipCommands import *
from askCommands import *
from playMusicCommands import *



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
# audioClips = audioClipCommands(bot)
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    # await setup_days_json()

# audioClips = audioClipCommands(bot)


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



def main():
    bot.run(TOKEN)
    print("Bot is online")    
    
if __name__ == '__main__':
    main()
