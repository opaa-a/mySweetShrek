import os
import discord
import json
from discord.ext import commands
from decouple import config
from discord.ext.commands.errors import ExtensionAlreadyLoaded, ExtensionNotFound, ExtensionNotLoaded
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


# ---------------------------------------------- # GLOABL FUNCTIONS # ---------------------------------------------- #

# function that dump new content to a specified json file
def edit_json(data, file):
    with open(file, 'w') as file:
        json.dump(data, file, indent=4)
        file.close()

# function that edit if a cog is loaded or unloaded in the cogs json file
def edit_cog_list(cog: str, method: str):
    with open('./main/assets/cogs.json') as cogs:
        cog_file = json.load(cogs)
    
    if method == "load":
        cog_file["COGS"][cog] = True

    elif method == "unload":
        cog_file["COGS"][cog] = False
    
    return edit_json(cog_file, "./main/assets/cogs.json")

# init_cog load all .py files located in ./main/cogs
def init_cog():
    cog_list = []
    # check if cog folder is empty
    for filename in os.listdir('./main/cogs'):         
        if filename.endswith(".py"):
            cog_list.append(f'cogs.{filename[:-3]}')
    # if cog folder not empty, load cogs
    if len(cog_list) > 0:
        # open cog file
        with open('./main/assets/cogs.json') as cogs:
            cog_file = json.load(cogs)
        # load cogs and add them to the file, passing them to True
        for cog in cog_list:
            cog_file["COGS"][cog] = True
            client.load_extension(cog)
        return print(Main_Log.init_cog_success), edit_json(cog_file, "./main/assets/cogs.json")
    # elif cog folder is empty, return error log
    elif len(cog_list) == 0:
        return print(Main_Log.init_cog_empty_cogs)

# ---------------------------------------------- # COMMANDS # ---------------------------------------------- #

@client.command()
async def load(ctx, cog: str):
    from cogs.essential import check_user_has_role
    # check if user has permissions to use the command
    if check_user_has_role(ctx.author, ADMIN_ROLE_ID):
        return print(Global_Log.command_has_been_used('load', ctx.author)), await ctx.reply(Global_Dialogue.user_not_allowed('load', ctx.author))
    # if conditions are met, try to execute
    try:
        client.load_extension(cog)
        edit_cog_list(cog, "load")
        return await ctx.reply(Main_Dialogue.load_command_success(cog, ctx.author))
    # if cog already loaded, return this exception
    except ExtensionAlreadyLoaded:
        return await ctx.reply(Main_ErrorHandler.load_error_cog_already_loaded(cog, ctx.author))
    # if cog does not exist, return this exception
    except ExtensionNotFound:
        return await ctx.reply(Main_ErrorHandler.load_error_cog_doesnt_exist(cog, ctx.author))
# handle missing requiered arg error for load command
@load.error
async def error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        print(Global_Log.command_has_been_used('load', ctx.author))
        return await ctx.reply(Global_Dialogue.arg_missing('load', ctx.author, '!load <cog>'))


@client.command()
async def unload(ctx, cog:str):
    from cogs.essential import check_user_has_role
    # check if user has permissions to use the command
    if check_user_has_role(ctx.author, ADMIN_ROLE_ID):
        return print(Global_Log.command_has_been_used('unload', ctx.author)), await ctx.reply(Global_Dialogue.user_not_allowed('unload', ctx.author))
    # if conditions are met, try to execute
    try:
        client.unload_extension(cog)
        edit_cog_list(cog, "unload")
        return await ctx.reply(Main_Dialogue.unload_command_success(cog, ctx.author))
    # if cog already unloaded, return this exception
    except ExtensionNotLoaded:
        return await ctx.reply(Main_ErrorHandler.unload_error_cog_already_unloaded(cog, ctx.author))
    # if cog does not exist, return this exception
    except ExtensionNotFound:
        return await ctx.reply(Main_ErrorHandler.unload_error_cog_doesnt_exist(cog, ctx.author))
# handle missing requiered arg error for unload command
@unload.error
async def error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        print(Global_Log.command_has_been_used('unload', ctx.author))
        return await ctx.reply(Global_Dialogue.arg_missing('unload', ctx.author, '!unload <cog>'))


@client.command()
async def reload(ctx, cog: str):
    from cogs.essential import check_user_has_role
    # check if user has permissions to use the command
    if check_user_has_role(ctx.author, ADMIN_ROLE_ID):
        return print(Global_Log.command_has_been_used('reload', ctx.author)), await ctx.reply(Global_Dialogue.user_not_allowed('reload', ctx.author))
    # if conditions are met, try to execute
    try:
        client.unload_extension(cog)
        client.load_extension(cog)
        return await ctx.reply(Main_Dialogue.reload_command_success(cog, ctx.author))
    # if cog is unloaded, return this exception
    except ExtensionNotLoaded:
        return await ctx.reply(Main_ErrorHandler.reload_error_cog_is_unloaded(cog, ctx.author))
    # if cog does not exist, return this exception
    except ExtensionNotFound:
        return await ctx.reply(Main_ErrorHandler.unload_error_cog_doesnt_exist(cog, ctx.author))
# handle missing required arg error for reload command
@reload.error
async def error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        print(Global_Log.command_has_been_used('reload', ctx.author))
        return await ctx.reply(Global_Dialogue.arg_missing('reload', ctx.author, '!reload <cog>'))


@client.command(aliases=['cl'])
async def coglist(ctx):
    from cogs.essential import check_user_has_role
    # check if user has permissions to use the command
    try:
        if check_user_has_role(ctx.author, ADMIN_ROLE_ID):
            return print(Global_Log.command_has_been_used('coglist', ctx.author)), await ctx.reply(Global_Dialogue.user_not_allowed('coglist', ctx.author))
    except AttributeError:
        return print(Global_Log.command_has_been_used('coglist', ctx.author)), await ctx.author.send(Global_Dialogue.command_executed_in_dm('coglist', ctx.author))
    # fecth the cogs json file and edit get its data
    with open('./main/assets/cogs.json') as cogs:
        cog_file = json.load(cogs)
        cog_dict = dict(cog_file["COGS"])
        cog_list = []
        # add a icon green or red depending on the status of the cog.
        for cog in cog_dict:
            if cog_dict[cog] == True:
                cog = f':green_circle:  **{cog}**'
                cog_list.append(cog)
            else:
                cog = f':red_circle:  **{cog}**'
                cog_list.append(cog)
        cog_list = '\n\n '.join(cog_list)
    # create the embed
    embed = discord.Embed(title="Cogs list",color=discord.Colour.random())
    embed.add_field(name="Here is the list of all the cogs.", value=f'\n{cog_list}')
    # return the result of the command.
    return Main_Dialogue.cl_command_success(ctx.author), await ctx.message.add_reaction(dialogue_icon.dm), await ctx.author.send(embed=embed)

@client.command()
async def source(ctx):
    print(Global_Log.command_has_been_used('source', ctx.author),'\n\t',Global_Log.command_run_without_exception('source'))
    return await ctx.reply(
        f'Here is my GitHub!'
        f'\nhttps://github.com/opaa-a/mySweetShrek'
        )
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