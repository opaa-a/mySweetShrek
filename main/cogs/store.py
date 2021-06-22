import discord
import json
from discord.ext import commands
from cogs.inventory import add_item_to_inv
from dialogue.store_dialogue import *
from dialogue.global_dialogue import *


#---------------------------------------------------------------------------------------#       GLOBAL VARIABLES       #---------------------------------------------------------------------------------------#



#---------------------------------------------------------------------------------------#        GLOBAL FUNCTIONS       #---------------------------------------------------------------------------------------#

def store_buy_item(userID, query : str, price: int):
# import functions from economy
    from cogs.economy import check_vault, get_balance, md_balance
# buy item 'A la niche'
    if query == 'A la niche!':
        if check_vault(userID) == False:
            # return if user is not registered
            return Global_Dialogue.user_not_registered('store buy')
        if get_balance(userID) < price:
            # return if user has not enough money
            return Global_Dialogue.user_cant_pay('store buy')
        # purchase is successful, pay the item
        md_balance(userID, "sub", price)
        add_item_to_inv(userID, "A la niche!", 1)
        return Store_Dialogue.store_purchase_complete(str(query))
# buy item 'Mauvais toutou'  
    if query == 'Mauvais toutou!':
        if check_vault(userID) == False:
            # return if user is not registered
            return Global_Dialogue.user_not_registered('store buy')
        if get_balance(userID) < price:
            # return if user has not enough money
            return Global_Dialogue.user_cant_pay('store buy')
        # purchase is successful, pay the item
        md_balance(userID, "sub", price)
        add_item_to_inv(userID, "Mauvais toutou!", 1)
        return Store_Dialogue.store_purchase_complete(str(query))
# buy item 'Shush'  
    if query == 'Shush!':
        if check_vault(userID) == False:
            # return if user is not registered
            return Global_Dialogue.user_not_registered('store buy')
        if get_balance(userID) < price:
            # return if user has not enough money
            return Global_Dialogue.user_cant_pay('store buy')
        # purchase is successful, pay the item
        md_balance(userID, "sub", price)
        add_item_to_inv(userID, "Shush!", 1)
        return Store_Dialogue.store_purchase_complete(str(query))
    
    return Global_Dialogue.query_exit('unknown_ID', 'store', userID)


#---------------------------------------------------------------------------------------#      STORE COMMANDS      #---------------------------------------------------------------------------------------#

class Store(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f'\n{log_format.INFO}- Store from store.py is loaded.{log_format.END}')

    @commands.command()
    async def store(self, ctx, param : str = None):
        print(Global_Log.command_has_been_used('store', ctx.author))
# message delivered if parameter is None or 'help'
        if param == None or param.lower() == 'help':
            await ctx.author.send(Store_Dialogue.help_store_success(ctx.author))
            await ctx.message.add_reaction(dialogue_icon.dm)
            #check if theme is selected
            def check(query):
                return ctx.author == query.author 
            query = await self.client.wait_for('message', check=check, timeout = 20)
            print(Global_Log.bot_is_waiting_for_querry(ctx.author))
            
            # iterate through the help file to fetch the store theme.
            with open('main/assets/help.json') as help_index:
                help_store = json.load(help_index)
                help_store = help_store["Store"]
                help_store_exp_list = list(help_store.values())
                help_store_exp_index_list = []
                for i in help_store_exp_list:
                    help_store_exp_index_list.append(help_store_exp_list.index(i))
            # return if query int unvalid
            try:
                if int(query.content) not in help_store_exp_index_list:
                    return await ctx.author.send(Global_Dialogue.query_exit('unknown_ID', 'store help', ctx.author))
            # return if query is not int
            except ValueError:
                return await ctx.author.send(Global_Dialogue.query_exit('valueError_int', 'store help', ctx.author))
            # return if query successful
            return await ctx.author.send(Store_Dialogue.help_store_querry(int(query.content), ctx.author))
        
# message delivered if parameter is 'showcase'
        if param.lower() == 'showcase':
            return await ctx.message.add_reaction(dialogue_icon.dm), await ctx.author.send(Store_Dialogue.store_showcase_success())

# message delivered if parameter is 'buy'
        if param.lower() == 'buy':
            await ctx.author.send(Store_Dialogue.store_buy_success())
            await ctx.message.add_reaction(dialogue_icon.dm)
            # check if product is selected
            def check(query):
                return ctx.author == query.author
            query = await self.client.wait_for('message', check=check, timeout = 30)
            print(Global_Log.bot_is_waiting_for_querry(ctx.author))

            # iterate through the store_inv file to fetch store inventory items
            with open('main/assets/store_inv.json') as store_inv:
                store_inv = json.load(store_inv)
                store_inv_list = list(store_inv)
            # return if query unvalid
                if str(query.content) not in store_inv_list:
                    return await ctx.author.send(Global_Dialogue.query_exit('unknown_ID', 'store buy', ctx.author))
            # return if query successful
                store_item = store_inv[str(query.content)]["price"]
            return await ctx.author.send(store_buy_item(ctx.author, str(query.content), store_item))

# message delivered if errors occurs
        return await ctx.reply(Store_ErrorHandler.error_store("bad_arg"))

#---------------------------------------------------------------------------------------#   STORE ERRORS   #---------------------------------------------------------------------------------------#



#---------------------------------------------------------------------------------------#       COGS SETUP      #---------------------------------------------------------------------------------------#

def setup(client):
    client.add_cog(Store(client))