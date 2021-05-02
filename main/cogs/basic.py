import discord
from discord.ext import commands
from dialogue.dialogue import *
from dialogue.errors import *

#---------------------------------------------------------------------------------------#      BASIC COMMANDS      #---------------------------------------------------------------------------------------#

# Basic Commands regroup all the the useless/basic commands of the bot.
class Basic_Commands(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f"\n- Basic Commands from basic is loaded.")


# !swamp@ OR !swampAt -- Take one arg, userID. Send the userID a spam message.
    @commands.command(aliases=['swamp@'])
    async def swampAt(self, ctx, userID : discord.Member):
        return await ctx.send(swampAt_success(userID))


#---------------------------------------------------------------------------------------#       BASIC ERROR        #---------------------------------------------------------------------------------------#

# !swamp@ error display
    @swampAt.error
    async def error(self, ctx, error):

        if isinstance(error, commands.BadArgument):
            return await ctx.reply(error_swampAt("bad_arg"))
        elif isinstance(error, commands.MissingRequiredArgument):
            return await ctx.reply(error_swampAt("missing_arg"))


#---------------------------------------------------------------------------------------#       COGS SETUP       #---------------------------------------------------------------------------------------#

def setup(client):
    client.add_cog(Basic_Commands(client))