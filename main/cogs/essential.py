import discord
import json
import asyncio
from discord.ext import commands
from dialogue.global_dialogue import *
from dialogue.essential_dialogue import *

#---------------------------------------------------------------------------------------#       GLOBAL VARIABLES       #---------------------------------------------------------------------------------------#

global malus_rate
malus_rate = 0.20

global bonus_rate
bonus_rate = 1.10

global discount
discount = 0.10

global passive_income
passive_income_rate = 2.5

#---------------------------------------------------------------------------------------#        GLOBAL FUNCTIONS       #---------------------------------------------------------------------------------------#

def check_user_in_chan(userID: discord.Member, channel):
    chan_member = []
    for member in channel.members:
        chan_member.append(member.id)
    if userID.id in chan_member:
        return True
    return False

def check_user_is_bot(userID: discord.Member):
    if userID.bot:
        return True
    return False

def check_user_voice_chan(userID: discord.Member):
    voice_state = userID.voice
    if voice_state is None:
        return False
    return True

def check_user_is_muted(userID: discord.Member):
    if userID.voice.mute:
        return True
    return False

def check_user_has_role(userID: discord.Member, role_id):
    roles_id = []
    for x in userID.roles:
        roles_id.append(x.id)
    if role_id in roles_id:
        return True
    return False
#---------------------------------------------------------------------------------------#      ESSENTIAL COMMANDS      #---------------------------------------------------------------------------------------#

# Basic Commands regroup all the the useless/basic commands of the bot.
class Essential(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f'\n{log_format.INFO}- Essential from basic.py is loaded.{log_format.END}')

# display the help general section
    async def help_general(self,ctx):
        await ctx.author.send(embed=Essential_Dialogue.help_general_function_success(ctx.author))
        #check if theme is selected
        def check(query):
            return ctx.author == query.author
        
        print(Global_Log.bot_is_waiting_for_query(ctx.author))
        try:
            query = await self.client.wait_for('message', check=check, timeout = 20)
            # iterate through the help file to fetch the store theme.
        except asyncio.TimeoutError:
            return Global_Dialogue.query_exit('timeout','general help', ctx.author)
        
        with open('main/assets/help.json') as help_index:
            help_general = json.load(help_index)
            help_general = help_general["General"]
            help_general_exp_list = list(help_general.values())
            help_general_exp_index_list = []
            for i in help_general_exp_list:
                help_general_exp_index_list.append(help_general_exp_list.index(i))
            #return if query int unvalid
            try:
                if int(query.content) not in help_general_exp_index_list:
                    return await ctx.author.send(Global_Dialogue.query_exit('unknown_ID','general help', ctx.author))
            # return if query is not int
            except ValueError:
                return await ctx.author.send(Global_Dialogue.query_exit('valueError_int', 'general help', ctx.author))
            #return if query successful
            return await ctx.author.send(embed=Essential_Dialogue.help_general_querry(int(query.content), ctx.author))

# !help -- Takes no mandatory args. display help.
    @commands.command()
    async def help(self, ctx):
        # await ctx.author.send(Essential_Dialogue.help_command_success(ctx.author))
        await ctx.author.send(embed=Essential_Dialogue.help_command_success(ctx.author))
        await ctx.message.add_reaction(dialogue_icon.dm)
        # check if theme is selected
        def check(query):
            return ctx.author == query.author
        # bot is waiting for a query
        print(Global_Log.bot_is_waiting_for_query(ctx.author))
        try:
            query = await self.client.wait_for('message', check=check, timeout = 20)
        except asyncio.TimeoutError:
            return Global_Dialogue.query_exit('timeout','general help', ctx.author)

        # iterate through the help file to fetch the index of themes.
        with open('main/assets/help.json') as help_index:
            help_theme = json.load(help_index)
            help_theme_list = list(help_theme)
            help_theme_index_list = []
            for i in help_theme_list:
                help_theme_index_list.append(help_theme_list.index(i))
        
        # return if query int is unvalid
        try:
            if int(query.content) not in help_theme_index_list:
                return await ctx.author.send(Global_Dialogue.query_exit('unknown_ID', 'index help', ctx.author))
        # return if query is not int
        except ValueError:
            return await ctx.author.send(Global_Dialogue.query_exit('valueError_int', 'index help', ctx.author))
        
        # return if query is successful
        if int(query.content) == 0:
            return await Essential.help_general(self, ctx)
        if int(query.content) == 1:
            from cogs.economy import Economy_Essentials
            return await Economy_Essentials.help_economy(self, ctx)
        if int(query.content) == 2:
            from cogs.economy import Economy_Grind
            return await Economy_Grind.help_grind(self, ctx)
        if int(query.content) == 3:
            from cogs.store import Store
            return await Store.store(self, ctx, 'help')
        if int(query.content) == 4:
            from cogs.inventory import Inventory_Essentials
            return await Inventory_Essentials.help_inv(self, ctx)
    
    @commands.command()
    async def debug(self, ctx):
        check_user_has_role(ctx, ctx.author, 804849555094765598)
        return await ctx.reply('done')

#---------------------------------------------------------------------------------------#       COGS SETUP       #---------------------------------------------------------------------------------------#

def setup(client):
    client.add_cog(Essential(client))