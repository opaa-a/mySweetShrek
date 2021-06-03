import discord
import json
from discord.ext import commands
from dialogue.dialogue import *
from dialogue.errors import *

#---------------------------------------------------------------------------------------#       GLOBAL VARIABLES       #---------------------------------------------------------------------------------------#



#---------------------------------------------------------------------------------------#        GLOBAL FUNCTIONS       #---------------------------------------------------------------------------------------#



#---------------------------------------------------------------------------------------#      INVENTORY ESSENTIALS COMMANDS      #---------------------------------------------------------------------------------------#

class Inventory_Essentials(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f'\n- Economy Essentials from inventory.py is loaded')

    @commands.command(aliases=['inv'])
    async def inventory(self, ctx):
        return

#---------------------------------------------------------------------------------------#       COGS SETUP      #---------------------------------------------------------------------------------------#

def setup(client):
    client.add_cog(Inventory_Essentials(client))