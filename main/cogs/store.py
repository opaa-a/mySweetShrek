import discord
import json
from discord import user
from discord.ext import commands
from dialogue.dialogue import *
from dialogue.errors import *
from cogs.economy import *

#---------------------------------------------------------------------------------------#       GLOBAL VARIABLES       #---------------------------------------------------------------------------------------#



#---------------------------------------------------------------------------------------#        GLOBAL FUNCTIONS       #---------------------------------------------------------------------------------------#

def store_buy_item(userID, querry : str, price: int):
    # from cogs.economy import get_vault
    # from cogs.economy import get_balance
    # from cogs.economy import md_balance
    if querry == 'A la niche!':
        if get_vault(userID) == False:
            return error_user_has_no_vault()
        if get_balance(userID) < price:
            return error_user_cant_pay()
        return (f'test')
        
    if querry == 'GTFO!':
        if get_vault(userID) == False:
            return error_user_has_no_vault()
        if get_balance(userID) < price:
            return error_user_cant_pay()
        return (f'test')
    
    if querry == 'Shush!':
        if get_vault(userID) == False:
            return error_user_has_no_vault()
        if get_balance(userID) < price:
            return error_user_cant_pay()
        return (f'test')



#---------------------------------------------------------------------------------------#      STORE SHOWCASE COMMANDS      #---------------------------------------------------------------------------------------#

class Store(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f'\n- Store from store.py is loaded')

    @commands.command()
    async def store(self, ctx, param : str = None):
# message delivered if parameter is None or 'help'
        if param == None or param.lower() == 'help':
            await ctx.author.send(help_store_success())
            #check if theme is selected
            def check(querry):
                return ctx.author == querry.author 
            querry = await self.client.wait_for('message', check=check, timeout = 20)
            
            # iterate through the help file to fetch the store theme.
            with open('main/assets/help.json') as help_index:
                help_store = json.load(help_index)
                help_store = help_store["Store"]
                help_store_exp_list = list(help_store.values())
                help_store_exp_index_list = []
                for i in help_store_exp_list:
                    help_store_exp_index_list.append(help_store_exp_list.index(i))
            # return if querry unvalid
            if int(querry.content) not in help_store_exp_index_list:
                return await ctx.author.send(querry_exit())
            # return if querry successful
            return await ctx.author.send(help_store_querry(int(querry.content)))
        
# message delivered if parameter is 'showcase'
        if param.lower() == 'showcase':
            return await ctx.author.send(store_showcase_success())

# message delivered if parameter is 'buy'
        if param.lower() == 'buy':
            await ctx.author.send(store_buy_success())
            # check if product is selected
            def check(querry):
                return ctx.author == querry.author
            querry = await self.client.wait_for('message', check=check, timeout = 30)

            # iterate through the store_inv file to fetch store inventory items
            with open('main/assets/store_inv.json') as store_inv:
                store_inv = json.load(store_inv)
                store_inv_list = list(store_inv)
                store_item = store_inv[str(querry.content)]["price"]
                print(store_item)
            # return if querry unvalid
            if str(querry.content) not in store_inv_list:
                return await ctx.author.send(querry_exit())
            # return if querry successful
            return await ctx.author.send(store_buy_item(ctx.author, str(querry.content), store_item))

# message delivered if errors occurs
        return await ctx.reply(error_store("bad_arg"))



#---------------------------------------------------------------------------------------#       COGS SETUP      #---------------------------------------------------------------------------------------#

def setup(client):
    client.add_cog(Store(client))