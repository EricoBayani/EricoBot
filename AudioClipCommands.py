# audioClipCommands.py

from Config import *
from discord.ext import commands
from AudioPlayer import TaggedAudioSource, AudioPlayer


class ClipPlayer(commands.Cog):    

    # a generic command that will play any sound file into
    # voice when passed a file path to the sound.

    def __init__(self, bot, logger = None, audioplayers = None):
        self.bot = bot
        self.logger = logger
        # jokes dictionary for easy random selection    
        self.jokes_dict = {}
        self.jokes_dict["brick_sucks"] = local_path + "brick-sucks.mp3"
        # TODO: should it be a fatal exception if audioplayer is None? It shouldn't happen, 
        # but if it does wouldn't it be good if I fixed the global audio player? 
        self.audioplayers = audioplayers


    async def play_audio(self, ctx, source_file, command_name='localfile'):
        print('Attempting to play sound')
        # Gets voice channel of message author

        print (str(ctx.author) + " used a command")
        voice_channel = ctx.author.voice

        # print(type(voice_channel))
        vc = ctx.voice_client
        if voice_channel != None:

            if vc is None:
                try:
                    vc = await voice_channel.channel.connect()
                except Exception as e:
                    print(f'Exception during voice channel connect: {e}')
                    return
            # vc.stop()

            if ctx.guild.id not in self.audioplayers:
                print (ctx.guild.id)
                self.audioplayers[ctx.guild.id] = AudioPlayer(self.bot, ctx, self.logger)
                print(f"There are now {len(self.audioplayers)} audioplayers")
            await self.audioplayers[ctx.guild.id].place_in_queue(ctx, TaggedAudioSource(source_file, tag=command_name))

            # # Sleep while audio is playing.
            #while vc.is_playing():
                # await asyncio.sleep(1)
            # await vc.disconnect()

        else:
            sent_message = await ctx.send(str(ctx.author.name) + " is not in a channel.")
            await sent_message.delete(delay=5)
        # Delete command after the audio is done playing.
        await ctx.message.delete()

    @commands.command(name='airhorn', help='play an airhorn sound in voice')
    async def play_airhorn(self, ctx):

        await self.play_audio(ctx, local_path + "mlg-airhorn.mp3", "local file")

    @commands.command(name='joke', help='Play a funny prerecorded haha joke for the whole family!')
    async def make_joke(self, ctx):

        joke_choice = rand.choice(list(self.jokes_dict.items()))

        await self.play_audio(ctx, joke_choice[1], "local file")
    @commands.command(name='scarra_laugh', help='Play the laugh of the venerable Scarra!')    
    async def scarra_laugh(self, ctx):

        await self.play_audio(ctx, local_path + "scarra-laugh.mp3", "local file")
    @commands.command(name='chug', help='NUMER ONE VICOTRY ROYAEL')    
    async def chugjug(self, ctx):

        if rand.random() > 0.5:
            if str(ctx.author) == kintorola:
                print ("Nah")
                await self.play_audio(ctx, local_path + "no.mp3", "local file")
            elif str(ctx.author) == brick:
                print ("lol_getrekt")
                await self.play_audio(ctx, local_path + "existence.mp3", "local file")
            elif str(ctx.author) == dix:
                print ("lol_usuckkek")
                await self.play_audio(ctx, local_path + "man-oth.mp3", "local file")            
            else:
                await self.play_audio(ctx, local_path + "my-chugjug-with-you.mp3", "local file")

        else:
            await self.play_audio(ctx, local_path + "chugjug-with-me.mp3", "local file")
            

    @commands.command(name='got_downed', help='plays a fun message for when your friend gets downed')    
    async def got_downed(self, ctx):

        await self.play_audio(ctx, local_path + "got-downed.mp3", "local file")

    @commands.command(name='cbt', help='plays a funny audio clip of a well known form of play')    
    async def cbt(self, ctx):
        await self.play_audio(ctx, local_path + "cbt-lol.mp3", "local file")

    # @commands.command(name='mychug', help='plays a funny audio clip of me singing a hit song')    
    # async def cbt(self, ctx):
    #     await self.play_audio(ctx, local_path + "my-chugjug-with-you.mp3", name)        
