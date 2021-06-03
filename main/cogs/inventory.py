import discord
import json
from discord import user
from discord.ext import commands
from cogs.economy import edit_vault
from dialogue.dialogue import *
from dialogue.errors import *

#---------------------------------------------------------------------------------------#       GLOBAL VARIABLES       #---------------------------------------------------------------------------------------#



#---------------------------------------------------------------------------------------#        GLOBAL FUNCTIONS       #---------------------------------------------------------------------------------------#

def add_item_to_inv(userID: str, item: str, amount: int):
    with open('main/assets/vault.json') as vault:
        vault = json.load(vault)
        userID = str(userID)
        inventory = vault[userID]['inventory']
        inventory_list = list(inventory)
        if item not in inventory_list:
            vault[userID]['inventory'] = {item:1}
        else :
            vault[userID]['inventory'][item] += amount
    edit_vault(vault)

def display_inv(userID):
    with open('main/assets/vault.json') as vault:
        vault = json.load(vault)
        userID = str(userID)
        inventory = vault[userID]['inventory']
        return display_inv_success(userID, inventory)

#---------------------------------------------------------------------------------------#      INVENTORY ESSENTIALS COMMANDS      #---------------------------------------------------------------------------------------#

class Inventory_Essentials(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f'\n- Economy Essentials from inventory.py is loaded')

    @commands.command(aliases=['inv'])
    async def inventory(self, ctx):
        return await ctx.author.send(display_inv(ctx.author))
        

#---------------------------------------------------------------------------------------#       COGS SETUP      #---------------------------------------------------------------------------------------#

def setup(client):
    client.add_cog(Inventory_Essentials(client))