import discord
import json
import asyncio
from discord.ext import commands
from cogs.economy import edit_vault
from cogs.economy import check_vault
from cogs.items import Item
from dialogue.global_dialogue import *
from dialogue.inventory_dialogue import *

#---------------------------------------------------------------------------------------#       GLOBAL VARIABLES       #---------------------------------------------------------------------------------------#



#---------------------------------------------------------------------------------------#        GLOBAL FUNCTIONS       #---------------------------------------------------------------------------------------#

def add_item_to_inv(userID: discord.Member, item: str, amount: int):
    print()
    with open('main/assets/vault.json') as vault:
        vault = json.load(vault)
        userID = str(userID)
        item = str(item)
        inventory = list(vault[userID]['inventory'])
        if item not in inventory:
            vault[userID]['inventory'][item] = amount
        vault[userID]['inventory'][item] += amount
    edit_vault(vault)
    return print(Inventory_Log.md_inv_log(userID, 'add', item, amount))

def remove_item_from_inv(userID: discord.Member, item: str, amount: int):
    with open('main/assets/vault.json') as vault:
        vault = json.load(vault)
        userID = str(userID)
        item = str(item)
        vault[userID]['inventory'][item] -= amount
    edit_vault(vault)
    return print(Inventory_Log.md_inv_log(userID, 'rm', item, amount))

def display_inv(userID: discord.Member):
    with open('main/assets/vault.json') as vault:
        vault = json.load(vault)
        userID = str(userID)
        inventory = vault[userID]['inventory']
        
        return Inventory_Dialogue.display_inv_success(inventory)

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
        print(f'\n{log_format.INFO}- Inventory Essentials from inventory.py is loaded.{log_format.END}')

# display the help inventory section
    async def help_inv(self,ctx):
        await ctx.author.send(embed=Inventory_Dialogue.help_inv_success(ctx.author))
        #check if theme is selected
        def check(query):
            return ctx.author == query.author
        
        print(Global_Log.bot_is_waiting_for_query(ctx.author))
        try:
            query = await self.client.wait_for('message', check=check, timeout = 20)
        except asyncio.TimeoutError:
            return Global_Dialogue.query_exit('timeout','general help', ctx.author)
            
        # iterate through the help file to fetch the store theme.
        with open('main/assets/help.json') as help_index:
            help_inv = json.load(help_index)
            help_inv = help_inv["General"]
            help_inv_exp_list = list(help_inv.values())
            help_inv_exp_index_list = []
            for i in help_inv_exp_list:
                help_inv_exp_index_list.append(help_inv_exp_list.index(i))
            #return if query int unvalid
            try:
                if int(query.content) not in help_inv_exp_index_list:
                    return await ctx.author.send(Global_Dialogue.query_exit('unknown_ID','general help', ctx.author))
            # return if query is not int
            except ValueError:
                return await ctx.author.send(Global_Dialogue.query_exit('valueError_int', 'general help', ctx.author))
            #return if query successful
            return await ctx.author.send(embed=Inventory_Dialogue.help_inv_querry(int(query.content), ctx.author))

# !inventory or !inv -- Takes no args. Display the inventory
    @commands.command(aliases=['inv'])
    async def inventory(self, ctx):
        print(Global_Log.command_has_been_used('inventory', ctx.author))
        if check_vault(ctx.author) is False:
            return await ctx.reply(Global_Dialogue.user_not_registered('inventory'))
        return await ctx.message.add_reaction(dialogue_icon.dm), await ctx.author.send(embed=display_inv(ctx.author))

# !use -- Takes a mandatory arg. use an item in the inventory
    @commands.command()
    async def use(self, ctx, target: discord.Member, *, item: str):
        print(Global_Log.command_has_been_used('use', ctx.author))
        # check if user has vault
        if check_vault(ctx.author) is False:
            return await ctx.reply(Global_Dialogue.user_not_registered('use'))

        if isinstance(ctx.channel, discord.channel.DMChannel):
            return await ctx.author.send(Global_Dialogue.command_executed_in_dm('use', ctx.author))

        if item == "A la niche!":
            if check_item(ctx.author, item):
                return await Item.item_a_la_niche(ctx, target, item)
                            
            return await ctx.reply(Inventory_Dialogue.use_success("item_missing", target, item))
        
        if item == "Mauvais toutou!":
            if check_item(ctx.author, item):
                return await Item.item_mauvais_toutou(ctx, target, item)

            return await ctx.reply(Inventory_Dialogue.use_success("item_missing", target, item))
        
        if item == "Shush!":

            if check_item(ctx.author, item):
                return await Item.item_shush(ctx, target, item)
            
            return await ctx.reply(Inventory_Dialogue.use_success("item_missing", target, item))

#---------------------------------------------------------------------------------------#   ECONOMY ESSENTIALS ERRORS   #---------------------------------------------------------------------------------------#

# !use error display
    @use.error
    async def error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            print(Global_Log.command_has_been_used('use', ctx.auhtor))
            return await ctx.reply(Global_Dialogue.bad_arg('use', ctx.author, '!use <target> <item>   --   <target> being a connected user and <item> being a purchased item.'))
        elif isinstance(error, commands.MissingRequiredArgument):
            print(Global_Log.command_has_been_used('use', ctx.author))
            return await ctx.reply(Global_Dialogue.arg_missing('use', ctx.author, '!use <target> <item>'))
        # return await ctx.author.send(unknown_error())


#---------------------------------------------------------------------------------------#       COGS SETUP      #---------------------------------------------------------------------------------------#

def setup(client):
    client.add_cog(Inventory_Essentials(client))