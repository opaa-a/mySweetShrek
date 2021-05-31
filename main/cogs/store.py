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
            await ctx.author.send(store_success('help'))
            def check(querry):
                if isinstance(ctx.channel, discord.channel.DMChannel) and ctx.author == querry.author:
                    return True

            querry = await self.client.wait_for('message', check=check)
            

            if querry.content == None :
                return await ctx.author.send(qa_querry_exit())

            return await ctx.author.send(qa_querry(int(querry.content)))

        if param.lower() == 'showcase':
            return await ctx.author.send(store_success('showcase'))


#---------------------------------------------------------------------------------------#       COGS SETUP      #---------------------------------------------------------------------------------------#

def setup(client):
    client.add_cog(Store(client))