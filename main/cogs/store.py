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

        if param == None or param.lower() == 'help':
            return await ctx.author.send(store_success('help'))


#---------------------------------------------------------------------------------------#       COGS SETUP      #---------------------------------------------------------------------------------------#

def setup(client):
    client.add_cog(Store(client))