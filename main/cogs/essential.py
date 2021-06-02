import discord
import json
from discord.ext import commands
from dialogue.dialogue import *
from dialogue.errors import *
from cogs.store import Store
#---------------------------------------------------------------------------------------#      BASIC COMMANDS      #---------------------------------------------------------------------------------------#

# Basic Commands regroup all the the useless/basic commands of the bot.
class Essential(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f"\n- Essential from basic.py is loaded.")


# !help -- Takes no mandatory args. display help.
    @commands.command()
    async def help(self, ctx):
        await ctx.author.send(help_index_success())
        # check if theme is selected
        def check(querry):
            return ctx.author == querry.author
        querry = await self.client.wait_for('message', check=check, timeout = 10)

        # iterate through the help file to fetch the index of themes.
        with open('main/assets/help.json') as help_index:
            help_theme = json.load(help_index)
            help_theme_list = list(help_theme)
            help_theme_index_list = []
            for i in help_theme_list:
                help_theme_index_list.append(help_theme_list.index(i))
        
        # return if querry is unvalid
        if int(querry.content) not in help_theme_index_list:
            return await ctx.author.send(help_index_querry_exit())
        
        # return if querry is successful
        if int(querry.content) == 0:
            return await ctx.author.send('general')
        if int(querry.content) == 1:
            return await ctx.author.send('economy')
        if int(querry.content) == 2:
            return await ctx.author.send('grind')
        if int(querry.content) == 3:
            return await Store.store(self, ctx)
        if int(querry.content) == 4:
            return await ctx.author.send('inventory')

#---------------------------------------------------------------------------------------#       BASIC ERROR        #---------------------------------------------------------------------------------------#



#---------------------------------------------------------------------------------------#       COGS SETUP       #---------------------------------------------------------------------------------------#

def setup(client):
    client.add_cog(Essential(client))