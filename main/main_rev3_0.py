import os
import discord
from discord import user
from discord.ext import commands
from decouple import config
from discord.ext.commands.errors import ExtensionAlreadyLoaded, ExtensionNotLoaded, MissingAnyRole, MissingRequiredArgument
from dialogue.main_dialogue import *
from dialogue.global_dialogue import *
from dialogue.errors import *

# ---------------------------------------------- # GLOBAL VARIABLES # ---------------------------------------------- #

# Fetch env variables with config from decouple
TOKEN = config('DISCORD_TOKEN') # DISCORD SERVER TOKEN
GUILD = config('DISCORD_GUILD') # DISCORD SERVER GUILD
DEF_CHAN = config('DISCORD_DEF_CHAN') # DISCORD SERVER DEFAULT CHANNEL
ADMIN_ROLE_ID = config('DISCORD_ADMIN_ROLE_ID') # DISCORD ADMIN ROLE IDENTIFIER

# Declare intents and the client
intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True, voice_states=True)
client = commands.Bot(command_prefix='!', intents=intents, help_command=None)


# ---------------------------------------------- # CLASS # ---------------------------------------------- #



# ---------------------------------------------- # GLOABL FUNCTIONS # ---------------------------------------------- #

# init_cog load all .py files located in ./main/cogs
def init_cog():
    cog_list = []
    # check if cog folder is empty
    for filename in os.listdir('./main/cogs'):         
        if filename.endswith(".py"):
            cog_list.append(f'cogs.{filename[:-3]}')
    # if cog folder not empty, load cogs
    if len(cog_list) > 0:
        for cog in cog_list:
            client.load_extension(cog)
        return print(Main_Log.init_cog_success)
    # elif cog folder is empty, return error log
    elif len(cog_list) == 0:
        return print(Main_Log.init_cog_empty_cogs)

    return unknown_error()

def check_cog_exist(cog: str):
    cog_list = []
    for filename in os.listdir('./main/cogs'):         
        if filename.endswith(".py"):
            cog_list.append(f'cogs.{filename[:-3]}')
    
    if cog in cog_list:
        return True
    return False

# ---------------------------------------------- # COMMANDS # ---------------------------------------------- #

@client.command()
async def load(ctx, cog: str):
    from cogs.essential import check_user_has_role
    # check if user has permissions to use the command
    if check_user_has_role(ctx.author, ADMIN_ROLE_ID):
        return print(Global_Log.command_has_been_used('load', ctx.author, log_format.DATE)), await ctx.reply(Global_Dialogue.user_not_allowed('load', ctx.author))
    # check if the specified cog exist
    if check_cog_exist(cog) is False:
        return await ctx.reply(Main_ErrorHandler.load_error_cog_doesnt_exist(cog, ctx.author, log_format.DATE))
    # if conditions are met, try to execute
    try:
        client.load_extension(cog)
        return await ctx.reply(Main_Dialogue.load_command_success(cog, ctx.author))
    # if cog already loaded, return this exception
    except ExtensionAlreadyLoaded:
        return await ctx.reply(Main_ErrorHandler.load_error_cog_already_loaded(cog, ctx.author, log_format.DATE))
# handle missing requiered arg error for load command
@load.error
async def error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        print(Global_Log.command_has_been_used('load', ctx.author, log_format.DATE))
        return await ctx.reply(Global_Dialogue.arg_missing('load', ctx.author, '!load <cog>'))


@client.command()
async def unload(ctx, cog:str):
    from cogs.essential import check_user_has_role
    # check if user has permissions to use the command
    if check_user_has_role(ctx.author, ADMIN_ROLE_ID):
        return print(Global_Log.command_has_been_used('unload', ctx.author, log_format.DATE)), await ctx.reply(Global_Dialogue.user_not_allowed('unload', ctx.author))
    # check if the specified cog exist
    if check_cog_exist(cog) is False:
        return await ctx.reply(Main_ErrorHandler.unload_error_cog_doesnt_exist(cog, ctx.author, log_format.DATE))
    # if conditions are met, try to execute
    try:
        client.unload_extension(cog)
        return await ctx.reply(Main_Dialogue.unload_command_success(cog, ctx.author))
    # if cog already loaded, return this exception
    except ExtensionNotLoaded:
        return await ctx.reply(Main_ErrorHandler.unload_error_cog_already_unloaded(cog, ctx.author, log_format.DATE))
# handle missing requiered arg error for load command
@unload.error
async def error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        print(Global_Log.command_has_been_used('unload', ctx.author, log_format.DATE))
        return await ctx.reply(Global_Dialogue.arg_missing('unload', ctx.author, '!unload <cog>'))
# ---------------------------------------------- # EVENTS # ---------------------------------------------- #

@client.event
async def on_ready():
    # declare a default channel the bot will send a init message to.
    def_chan = client.get_channel(int(DEF_CHAN))
    # Get current guild from client's list of guilds.
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    
    # print log
    print(
        f'\n{log_format.INFO}BOT IS ONLINE'
        f'\n\n> BOT ID : {client.user}'
        f'\n> GUILD NAME : {guild.name}'
        f'\n> GUILD ID : {guild.id}'
        f'\n> DEFAULT CHANNEL : {def_chan.name}'
        f'\n> GUILD OWNER : {guild.owner}'
        f'\n{log_format.END}'
        )
    # send log
    #await def_chan.send(f':triangular_flag_on_post:    I am up and running...')
    # initialize cogs after client is ready.
    init_cog()

# run client
client.run(TOKEN)