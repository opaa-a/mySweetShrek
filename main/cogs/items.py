import discord
import asyncio
from discord.ext import commands
from discord.role import Role
from dialogue.dialogue import *
from dialogue.errors import *

#---------------------------------------------------------------------------------------#       GLOBAL VARIABLES       #---------------------------------------------------------------------------------------#



#---------------------------------------------------------------------------------------#        GLOBAL FUNCTIONS       #---------------------------------------------------------------------------------------#



#---------------------------------------------------------------------------------------#       ITEM      #---------------------------------------------------------------------------------------#

class Item(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f'\n- Item from items.py is loaded')

# ITEM A LA NICHE
    async def item_a_la_niche(ctx, target: discord.Member, item: str):
        # get the functions from the cog inventory
        from cogs.inventory import remove_item_from_inv 
        from cogs.essential import check_user_in_chan
        from cogs.essential import check_user_is_bot
        from cogs.essential import check_user_voice_chan
        
        # get the channel "la niche"
        channel = ctx.guild.get_channel(804847478473883668)
        
        # check if user is already in La niche 
        if check_user_in_chan(target, channel):
            return await ctx.reply(item_a_la_niche_success("target_already_in_chan", target))
        
        # check if user is a bot
        if check_user_is_bot(target):
            return await ctx.reply(item_a_la_niche_success("target_is_bot", target))
        
        # check if user is connected to a voice channel
        if check_user_voice_chan(target) is False:
            return await ctx.reply(item_a_la_niche_success("target_not_connected", target))

        # remove the used item from the inventory of the author
        remove_item_from_inv(ctx.author, item, 1)
        # move the target to the channel "la niche" & send success dialogue
        return await target.move_to(channel), await ctx.reply(use_success("item_used", target, item, ctx.author))

# ITEM MAUVAIS TOUTOU
    async def item_mauvais_toutou(ctx, target: discord.Member, item: str):
        # get the functions from the cog inventory, essential and economy
        from cogs.inventory import remove_item_from_inv 
        from cogs.essential import check_user_has_role
        from cogs.essential import check_user_is_bot
        from cogs.economy import check_vault
        
        # set the roles 'mauvais toutou' and 'bon toutou' /// Also decide how long the 'mauvais toutou' role is given. 24 hours here.
        role_mauvais_toutou = ctx.guild.get_role(805897076437155861)
        role_bon_toutou = ctx.guild.get_role(804849555094765598)
        role_hold_time = (60*60)*24

        # check if user already has role 'mauvais toutou'
        if check_user_has_role(target, 805897076437155861):
            return await ctx.reply(item_mauvais_toutou("target_already_has_role", target))
        
        # check if user is a bot
        if check_user_is_bot(target):
            return await ctx.reply(item_mauvais_toutou("target_is_bot", target))
        
        # check if user has a vault
        if check_vault(target) is False:
            return await ctx.reply(item_mauvais_toutou("target_is_not_registered", target))
        
        # remove the used item from the inventory of the author
        remove_item_from_inv(ctx.author, item, 1)
        # add the role to the target and remove the 'bon toutou' role if he had it
        await target.add_roles(role_mauvais_toutou)
        if check_user_has_role(target, 804849555094765598):
            await target.remove_roles(role_bon_toutou)
        # send success dialogue
        await ctx.reply(use_success("item_used", target, item, ctx.author))

        # wait for the role hold time to expire
        await asyncio.sleep(role_hold_time)
        # after role hold time, remove role 'mauvais toutou'
        return await target.remove_roles(role_mauvais_toutou)


# ITEM SHUSH
    async def item_shush(ctx, target: discord.Member, item: str):
        # get the functions from the cog inventory and essential
        from cogs.inventory import remove_item_from_inv
        from cogs.essential import check_user_is_muted
        from cogs.essential import check_user_is_bot
        from cogs.essential import check_user_voice_chan
        
        # set the mute time to 3 minutes (180 seconds)
        mute_time = 180

        # check if user is already muted
        if check_user_is_muted(target):
            return await ctx.reply(item_shush_success("target_is_already_muted", target))

        # check if user is a bot
        if check_user_is_bot(target):
            return await ctx.reply(item_shush_success("target_is_bot", target))
        
        # check if user is connected to a voice channel
        if check_user_voice_chan(target) is False:
            return await ctx.reply(item_shush_success("target_not_connected", target))
        
        # remove the used item from the inventory of the author
        remove_item_from_inv(ctx.author, item, 1)
        # mute the target
        await target.edit(mute=True)
        # send success dialogue
        await ctx.reply(use_success("item_used", target, item, ctx.author))
        
        # wait for the set mute time
        await asyncio.sleep(mute_time)
        # after mute time, unmute the target
        return await target.edit(mute=False)

#---------------------------------------------------------------------------------------#       COGS SETUP      #---------------------------------------------------------------------------------------#

def setup(client):
    client.add_cog(Item(client))