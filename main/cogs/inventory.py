import discord
import json
from discord.ext import commands
from cogs.economy import edit_vault
from cogs.economy import get_vault
from cogs.items import Item
from dialogue.dialogue import *
from dialogue.errors import *

#---------------------------------------------------------------------------------------#       GLOBAL VARIABLES       #---------------------------------------------------------------------------------------#



#---------------------------------------------------------------------------------------#        GLOBAL FUNCTIONS       #---------------------------------------------------------------------------------------#

def add_item_to_inv(userID: discord.Member, item: str, amount: int):
    with open('main/assets/vault.json') as vault:
        vault = json.load(vault)
        userID = str(userID)
        item = str(item)
        inventory = list(vault[userID]['inventory'])
        if item not in inventory:
            vault[userID]['inventory'][item] = amount
        vault[userID]['inventory'][item] += amount
    edit_vault(vault)

def remove_item_from_inv(userID: discord.Member, item: str, amount: int):
    with open('main/assets/vault.json') as vault:
        vault = json.load(vault)
        userID = str(userID)
        item = str(item)
        inventory = list(vault[userID]['inventory'])
        vault[userID]['inventory'][item] -= amount
    edit_vault(vault)

def display_inv(userID: discord.Member):
    with open('main/assets/vault.json') as vault:
        vault = json.load(vault)
        userID = str(userID)
        inventory = vault[userID]['inventory']
        
        return display_inv_success(inventory)

def check_item(userID: discord.Member, item: str):
    with open('main/assets/vault.json') as vault:
        vault = json.load(vault)
        userID = str(userID)
        inventory = vault[userID]['inventory']
        
        if item not in inventory or inventory[item] <= 0:
            return False
        return True

#---------------------------------------------------------------------------------------#      INVENTORY ESSENTIALS COMMANDS      #---------------------------------------------------------------------------------------#

class Inventory_Essentials(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f'\n- Inventory Essentials from inventory.py is loaded')

# display the help inventory section
    async def help_inv(self,ctx):
        await ctx.author.send(help_inv_success())
        #check if theme is selected
        def check(querry):
            return ctx.author == querry.author
        querry = await self.client.wait_for('message', check=check, timeout = 20)
        # iterate through the help file to fetch the store theme.
        with open('main/assets/help.json') as help_index:
            help_inv = json.load(help_index)
            help_inv = help_inv["General"]
            help_inv_exp_list = list(help_inv.values())
            help_inv_exp_index_list = []
            for i in help_inv_exp_list:
                help_inv_exp_index_list.append(help_inv_exp_list.index(i))
            #return if querry int unvalid
            try:
                if int(querry.content) not in help_inv_exp_index_list:
                    return await ctx.author.send(querry_exit('unknown_ID','general help'))
            # return if querry is not int
            except ValueError:
                return await ctx.author.send(querry_exit('valueError_int', 'general help'))
            #return if querry successful
            return await ctx.author.send(help_inv_querry(int(querry.content)))

# !inventory or !inv -- Takes no args. Display the inventory
    @commands.command(aliases=['inv'])
    async def inventory(self, ctx):
        return await ctx.message.add_reaction('📨'), await ctx.author.send(display_inv(ctx.author))

# !use -- Takes a mandatory arg. use an item in the inventory
    @commands.command()
    async def use(self, ctx, target: discord.Member, *, item: str):
        # check if user has vault
        if get_vault(ctx.author) != True:
            return error_user_has_no_vault(ctx.author)

        if isinstance(ctx.channel, discord.channel.DMChannel):
            return await ctx.author.send(use_success('command_in_dm'))

        if item == "A la niche!":
            
            if check_item(ctx.author, item):
                return await Item.item_alaniche(ctx, target, item)
                            
            return await ctx.reply(use_success("item_missing", target, item))
        
        if item == "GTFO!":
            if check_item(ctx.author, item):
                remove_item_from_inv(ctx.author, item, 1)
                await ctx.author.send(use_success("item_used", target, item, ctx.author))
                return await Item.item_gtfo(ctx, target)
            return await ctx.reply(use_success("item_missing", target, item))
        
        if item == "Shush!":
            if check_item(ctx.author, item):
                remove_item_from_inv(ctx.author, item, 1)
                await ctx.reply(use_success("item_used", target, item, ctx.author))
                return await Item.item_shush(ctx, target)
            return await ctx.reply(use_success("item_missing", target, item))

#---------------------------------------------------------------------------------------#   ECONOMY ESSENTIALS ERRORS   #---------------------------------------------------------------------------------------#

# !use error display
    @use.error
    async def error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            return print(log_error_bad_arg("use")), await ctx.author.send(error_use("bad_arg"))
        elif isinstance(error, commands.MissingRequiredArgument):
            return print(log_error_missing_arg("use")), await ctx.author.send(error_use("missing_arg"))
        # return await ctx.author.send(unknown_error())


#---------------------------------------------------------------------------------------#       COGS SETUP      #---------------------------------------------------------------------------------------#

def setup(client):
    client.add_cog(Inventory_Essentials(client))