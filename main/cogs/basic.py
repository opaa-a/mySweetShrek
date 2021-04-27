import discord
from discord.ext import commands

class Basic_Commands(commands.Cog):

    def __init__(self, client):
        self.client = client
        print(f"\n- Basic Commands from basic is loaded.")
    
                # !swamp@ OR !swampAt -- MENTION A SPECIFIED MEMBER AND SEND TEXT
    @commands.command(aliases=['swamp@'])
    async def swampAt(self, ctx, member : discord.Member):
        await ctx.send(f"OI {member.mention}, GET THE FUCK OUT OF ME SWAMP YA FUCKING TWAT!")

    @swampAt.error
    async def error(self, ctx, error):

        if isinstance(error, commands.BadArgument):
            await ctx.reply(f':x:   Username is not valid!')
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f':x:   Oops! You need to specify a username!\n- !swamp@ <username>')
            return



def setup(client):
    client.add_cog(Basic_Commands(client))