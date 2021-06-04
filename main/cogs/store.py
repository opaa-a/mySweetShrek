import discord
import json
from discord.ext import commands
from cogs.inventory import add_item_to_inv
from dialogue.dialogue import *
from dialogue.errors import *

#---------------------------------------------------------------------------------------#       GLOBAL VARIABLES       #---------------------------------------------------------------------------------------#



#---------------------------------------------------------------------------------------#        GLOBAL FUNCTIONS       #---------------------------------------------------------------------------------------#

def store_buy_item(userID, querry : str, price: int):
# import functions from economy
    from cogs.economy import get_vault, get_balance, md_balance
# buy item 'A la niche'
    if querry == 'A la niche!':
        if get_vault(userID) == False:
            # return if user is not registered
            return error_user_has_no_vault()
        if get_balance(userID) < price:
            # return if user has not enough money
            return error_user_cant_pay()
        # log the purchase
        print(f'# STORE -- {userID} bought {querry}')
        # purchase is successful, pay the item
        md_balance(userID, "sub", price)
        add_item_to_inv(userID, "A la niche!", 1)
        return store_purchase_complete(str(querry))
# buy item 'GTFO'  
    if querry == 'GTFO!':
        if get_vault(userID) == False:
            # return if user is not registered
            return error_user_has_no_vault()
        if get_balance(userID) < price:
            # return if user has not enough money
            return error_user_cant_pay()
        # log the purchase
        print(f'# STORE -- {userID} bought {querry}')
        # purchase is successful, pay the item
        md_balance(userID, "sub", price)
        add_item_to_inv(userID, "GTFO!", 1)
        return store_purchase_complete(str(querry))
# buy item 'Shush'  
    if querry == 'Shush!':
        if get_vault(userID) == False:
            # return if user is not registered
            return error_user_has_no_vault()
        if get_balance(userID) < price:
            # return if user has not enough money
            return error_user_cant_pay()
        # log the purchase
        print(f'# STORE -- {userID} bought {querry}')
        # purchase is successful, pay the item
        md_balance(userID, "sub", price)
        add_item_to_inv(userID, "Shush!", 1)
        return store_purchase_complete(str(querry))
    # return querry_exit('store')


#---------------------------------------------------------------------------------------#      STORE COMMANDS      #---------------------------------------------------------------------------------------#

class Store(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f'\n- Store from store.py is loaded')

    @commands.command()
    async def store(self, ctx, param : str = None):
# message delivered if parameter is None or 'help'
        if param == None or param.lower() == 'help':
            await ctx.author.send(help_store_success())
            await ctx.message.add_reaction('📨')
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
            # return if querry int unvalid
            try:
                if int(querry.content) not in help_store_exp_index_list:
                    return await ctx.author.send(querry_exit('unknown_ID', 'store help'))
            # return if querry is not int
            except ValueError:
                return await ctx.author.send(querry_exit('valueError_int', 'store help'))
            # return if querry successful
            return await ctx.author.send(help_store_querry(int(querry.content)))
        
# message delivered if parameter is 'showcase'
        if param.lower() == 'showcase':
            return await ctx.message.add_reaction('📨'), await ctx.author.send(store_showcase_success())

# message delivered if parameter is 'buy'
        if param.lower() == 'buy':
            await ctx.author.send(store_buy_success())
            await ctx.message.add_reaction('📨')
            # check if product is selected
            def check(querry):
                return ctx.author == querry.author
            querry = await self.client.wait_for('message', check=check, timeout = 30)

            # iterate through the store_inv file to fetch store inventory items
            with open('main/assets/store_inv.json') as store_inv:
                store_inv = json.load(store_inv)
                store_inv_list = list(store_inv)
            # return if querry unvalid
                if str(querry.content) not in store_inv_list:
                    return await ctx.author.send(querry_exit('unknown_ID', 'store buy'))
            # return if querry successful
                store_item = store_inv[str(querry.content)]["price"]
            return await ctx.author.send(store_buy_item(ctx.author, str(querry.content), store_item))

# message delivered if errors occurs
        return await ctx.reply(error_store("bad_arg"))

#---------------------------------------------------------------------------------------#   STORE ERRORS   #---------------------------------------------------------------------------------------#



#---------------------------------------------------------------------------------------#       COGS SETUP      #---------------------------------------------------------------------------------------#

def setup(client):
    client.add_cog(Store(client))