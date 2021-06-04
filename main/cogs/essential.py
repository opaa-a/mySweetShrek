import discord
import json
from discord.ext import commands
from discord.ext.commands.errors import BadArgument
from cogs.inventory import Inventory_Essentials
from dialogue.dialogue import *
from dialogue.errors import *

#---------------------------------------------------------------------------------------#       GLOBAL VARIABLES       #---------------------------------------------------------------------------------------#



#---------------------------------------------------------------------------------------#        GLOBAL FUNCTIONS       #---------------------------------------------------------------------------------------#



#---------------------------------------------------------------------------------------#      ESSENTIAL COMMANDS      #---------------------------------------------------------------------------------------#

# Basic Commands regroup all the the useless/basic commands of the bot.
class Essential(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f"\n- Essential from basic.py is loaded.")

# display the help general section
    async def help_general(self,ctx):
        await ctx.author.send(help_general_success())
        #check if theme is selected
        def check(querry):
            return ctx.author == querry.author
        querry = await self.client.wait_for('message', check=check, timeout = 20)
        # iterate through the help file to fetch the store theme.
        with open('main/assets/help.json') as help_index:
            help_general = json.load(help_index)
            help_general = help_general["General"]
            help_general_exp_list = list(help_general.values())
            help_general_exp_index_list = []
            for i in help_general_exp_list:
                help_general_exp_index_list.append(help_general_exp_list.index(i))
            #return if querry int unvalid
            try:
                if int(querry.content) not in help_general_exp_index_list:
                    return await ctx.author.send(querry_exit('unknown_ID','general help'))
            # return if querry is not int
            except ValueError:
                return await ctx.author.send(querry_exit('valueError_int', 'general help'))
            #return if querry successful
            return await ctx.author.send(help_general_querry(int(querry.content)))

# !help -- Takes no mandatory args. display help.
    @commands.command()
    async def help(self, ctx):
        await ctx.author.send(help_index_success())
        # check if theme is selected
        def check(querry):
            return ctx.author == querry.author
        querry = await self.client.wait_for('message', check=check, timeout = 20)
        # iterate through the help file to fetch the index of themes.
        with open('main/assets/help.json') as help_index:
            help_theme = json.load(help_index)
            help_theme_list = list(help_theme)
            help_theme_index_list = []
            for i in help_theme_list:
                help_theme_index_list.append(help_theme_list.index(i))
        
        # return if querry int is unvalid
        try:
            if int(querry.content) not in help_theme_index_list:
                return await ctx.author.send(querry_exit('unknown_ID', 'index help'))
        # return if querry is not int
        except ValueError:
            return await ctx.author.send(querry_exit('valueError_int', 'index help'))
        
        # return if querry is successful
        if int(querry.content) == 0:
            return await Essential.help_general(self, ctx)
        if int(querry.content) == 1:
            from cogs.economy import Economy_Essentials
            return await Economy_Essentials.help_economy(self, ctx)
        if int(querry.content) == 2:
            from cogs.economy import Economy_Grind
            return await Economy_Grind.help_grind(self, ctx)
        if int(querry.content) == 3:
            from cogs.store import Store
            return await Store.store(self, ctx, 'help')
        if int(querry.content) == 4:
            from cogs.inventory import Inventory_Essentials
            return await Inventory_Essentials.help_inv(self, ctx)
        # return await ctx.author.send(querry_exit('index help'))

#---------------------------------------------------------------------------------------#       BASIC ERROR        #---------------------------------------------------------------------------------------#

    # @help.error
    # async def error(self, ctx, error):
    #     if isinstance(error, commands.BadArgument):
    #         print('test')
    #         await ctx.author.send(error_help("bad_arg"))

#---------------------------------------------------------------------------------------#       COGS SETUP       #---------------------------------------------------------------------------------------#

def setup(client):
    client.add_cog(Essential(client))