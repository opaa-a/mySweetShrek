import discord
import json
from discord.ext import commands
from dialogue.dialogue import *
from dialogue.errors import *

#---------------------------------------------------------------------------------------#       GLOBAL VARIABLES       #---------------------------------------------------------------------------------------#



#---------------------------------------------------------------------------------------#        GLOBAL FUNCTIONS       #---------------------------------------------------------------------------------------#



#---------------------------------------------------------------------------------------#       ITEM      #---------------------------------------------------------------------------------------#

class Item(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f'\n- Item from items.py is loaded')

    async def item_alaniche(ctx, target: discord.Member, item: str):
        from cogs.inventory import remove_item_from_inv 
        from cogs.essential import check_user_in_chan
        channel = ctx.guild.get_channel(804847478473883668)
        
        if check_user_in_chan(target, channel):
            return await ctx.reply(item_a_la_niche_success("user_already_in_chan", target))

        remove_item_from_inv(ctx.author, item, 1)
        return await target.move_to(channel), await ctx.reply(use_success("item_used", target, item, ctx.author))

    async def item_gtfo():
        return (f'test gtfo')

    async def item_shush():
        return (f'test shush')


#---------------------------------------------------------------------------------------#       COGS SETUP      #---------------------------------------------------------------------------------------#

def setup(client):
    client.add_cog(Item(client))