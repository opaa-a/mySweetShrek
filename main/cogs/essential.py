import discord
import json
from decimal import Decimal
from discord.ext import commands
from dialogue.global_dialogue import *
from dialogue.essential_dialogue import *

#---------------------------------------------------------------------------------------#       GLOBAL VARIABLES       #---------------------------------------------------------------------------------------#

global malus_rate
malus_rate = 0.20

global bonus_rate
bonus_rate = 1.10

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
        await ctx.author.send(Essential_Dialogue.help_general_function_success(ctx.author))
        #check if theme is selected
        def check(query):
            return ctx.author == query.author
        query = await self.client.wait_for('message', check=check, timeout = 20)
        # iterate through the help file to fetch the store theme.
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
                    return await ctx.author.send(Global_Dialogue.querry_exit('unknown_ID','general help', ctx.author))
            # return if query is not int
            except ValueError:
                return await ctx.author.send(Global_Dialogue.querry_exit('valueError_int', 'general help', ctx.author))
            #return if query successful
            return await ctx.author.send(Essential_Dialogue.help_general_querry(int(query.content), ctx.author))

# !help -- Takes no mandatory args. display help.
    @commands.command()
    async def help(self, ctx):
        await ctx.author.send(Essential_Dialogue.help_command_success(ctx.author))
        await ctx.message.add_reaction(dialogue_icon.dm)
        print(Global_Log.bot_is_waiting_for_querry(ctx.author))
        # check if theme is selected
        def check(query):
            return ctx.author == query.author
        # bot is waiting for a query
        query = await self.client.wait_for('message', check=check, timeout = 20)
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
                return await ctx.author.send(Global_Dialogue.querry_exit('unknown_ID', 'index help', ctx.author))
        # return if query is not int
        except ValueError:
            return await ctx.author.send(Global_Dialogue.querry_exit('valueError_int', 'index help', ctx.author))
        
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
        x = [300,900,5000,10000,50000]
        for stack in x:
            rate = stack / 100000
            inc = stack * rate
            reward = stack + inc
            await ctx.send(
                f'\n**STACK   ==   {stack}**'
                f'\n**RATE   ==   {rate}**'
                f'\n**INC   ==   {inc}**'
                f'\n**REWARD   ==   {reward}**'
                f'\n------------------------------'
                )

#---------------------------------------------------------------------------------------#       COGS SETUP       #---------------------------------------------------------------------------------------#

def setup(client):
    client.add_cog(Essential(client))