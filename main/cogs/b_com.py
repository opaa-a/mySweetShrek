import discord
import random
from discord.ext import commands
from facts_dic import *



class SwampCommand(commands.Cog):

    def __init__(self, client):
        self.client = client
        print(f"\n- SwampCommand from b_com is loaded.")
    
                # !swamp@ OR !swampAt -- MENTION A SPECIFIED MEMBER AND SEND TEXT
    @commands.command(aliases=['swamp@'])
    async def swampAt(self, ctx, member : discord.Member):
        await ctx.send(f"OI {member.mention}, GET THE FUCK OUT OF ME SWAMP YA FUCKING TWAT!")

    @swampAt.error
    async def error(self, ctx, error):

        if isinstance(error, commands.BadArgument):
            await ctx.reply(f'Username is not valid!')
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f'Oops! You need to specify a username!\n- !swamp@ <username>')
            return
                
                # !fa OR !facts -- SEND A RANDOM FACT FROM facts_dic.py AND EXPECT SOMETIMES AN ANSWER.
    @commands.command(aliases=['fa'])
    async def facts(self, ctx):

        client = discord.Client
        channel = ctx.channel
        random_fact = random.choice(fact_list)
        fact_index = fact_list.index(random_fact)
        
        await ctx.send(random_fact)

        def check(ans):
            if ans.content == answer_list[fact_index] and ans.channel == channel:
                return ans.content, ans.channel
        
        if answer_list[fact_index] == "null":
            print('\n!facts ; break ; no answer needed.')
            return
        
        else:
            answer = await client.wait_for(self.client, 'message', check=check, timeout=15)
            await answer.reply(f'Success! :joy::ok_hand:')
            return


def setup(client):
    client.add_cog(SwampCommand(client))