import discord
from discord.ext import commands


#---------------------------------------------------------------------------------------#      BASIC COMMANDS      #---------------------------------------------------------------------------------------#

# Basic Commands regroup all the the useless/basic commands of the bot.
class Basic_Commands(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f"\n- Basic Commands from basic is loaded.")


# !swamp@ OR !swampAt -- Take one arg, userID. Send the userID a spam message.
    @commands.command(aliases=['swamp@'])
    async def swampAt(self, ctx, userID : discord.Member):
        await ctx.send(f"OI {userID.mention}, GET THE FUCK OUT OF ME SWAMP YA FUCKING TWAT!")


#---------------------------------------------------------------------------------------#       BASIC ERROR        #---------------------------------------------------------------------------------------#

# !swamp@ error display
    @swampAt.error
    async def error(self, ctx, error):

        if isinstance(error, commands.BadArgument):
            await ctx.reply(f':x:   Username is not valid!')
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f':x:   Oops! You need to specify a username!\n- !swamp@ <username>')
            return


#---------------------------------------------------------------------------------------#       COGS SETUP       #---------------------------------------------------------------------------------------#

def setup(client):
    client.add_cog(Basic_Commands(client))