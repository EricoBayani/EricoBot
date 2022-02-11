# askCommands.py
import wikipediaapi as wiki

#local modules
from config import *

class AskWiki(commands.Cog):

    @commands.command(name='ask', help='for now, it just spits back the question string,'
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
