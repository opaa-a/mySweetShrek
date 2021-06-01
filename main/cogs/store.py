import discord
import json
from discord.ext import commands
from decouple import config
from dialogue.dialogue import *
from dialogue.errors import *

#---------------------------------------------------------------------------------------#       GLOBAL VARIABLES       #---------------------------------------------------------------------------------------#


#---------------------------------------------------------------------------------------#        GLOBAL FUNCTIONS       #---------------------------------------------------------------------------------------#


#---------------------------------------------------------------------------------------#      STORE SHOWCASE COMMANDS      #---------------------------------------------------------------------------------------#

class Store(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f'\n- Store from store.py is loaded')


    @commands.command()
    async def store(self, ctx, param : str = None):

# message delivered if parameter is None or 'help'
        if param == None or param.lower() == 'help':
            await ctx.author.send(store_help_success())
            # check if questions are asked
            def check(querry):
                if isinstance(ctx.channel, discord.channel.DMChannel) and ctx.author == querry.author:
                    return True
            querry = await self.client.wait_for('message', check=check, timeout = 10)
            
            # iterate through the qa_list to fetch answers to questions.
            with open('main/assets/qa_list.json') as qa_list:
                qa_list = json.load(qa_list)
                answer_list = list(qa_list.values())
                answer_list_index = []
                for i in answer_list:
                    answer_list_index.append(answer_list.index(i))
            # return if querry invalid
            if int(querry.content) not in answer_list_index:
                return await ctx.author.send(store_help_querry_exit())
            # return if querry successful
            return await ctx.author.send(store_help_querry(int(querry.content)))
        
# message delivered if parameter is 'showcase
        if param.lower() == 'showcase':
            return await ctx.author.send(store_showcase_success())

# message delivered if errors occurs
        return await ctx.reply(error_store("bad_arg"))



#---------------------------------------------------------------------------------------#       COGS SETUP      #---------------------------------------------------------------------------------------#

def setup(client):
    client.add_cog(Store(client))