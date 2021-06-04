import discord
import json
from discord.ext import commands
from dialogue.dialogue import *
from dialogue.errors import *

#---------------------------------------------------------------------------------------#       GLOBAL VARIABLES       #---------------------------------------------------------------------------------------#



#---------------------------------------------------------------------------------------#        GLOBAL FUNCTIONS       #---------------------------------------------------------------------------------------#



#---------------------------------------------------------------------------------------#       ITEM      #---------------------------------------------------------------------------------------#

class Item(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f'\n- Item from items.py is loaded')
    
    def item_alaniche():
        return (f'test a la niche')

    def item_gtfo():
        return (f'test gtfo')

    def item_shush():
        return (f'test shush')


#---------------------------------------------------------------------------------------#       COGS SETUP      #---------------------------------------------------------------------------------------#

def setup(client):
    client.add_cog(Item(client))