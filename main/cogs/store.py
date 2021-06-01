import discord
import json
from discord.ext import commands
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
            # check if theme is selected
            def check(querry):
                return ctx.author == querry.author  
            querry = await self.client.wait_for('message', check=check, timeout = 10)
            
            # iterate through the help file to fetch the store theme.
            with open('main/assets/help.json') as help_index:
                help_store = json.load(help_index)
                help_store = help_store["Store"]
                help_store_exp_list = list(help_store.values())
                help_store_exp_index_list = []
                for i in help_store_exp_list:
                    help_store_exp_index_list.append(help_store_exp_list.index(i))
            # return if querry invalid
            if int(querry.content) not in help_store_exp_index_list:
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