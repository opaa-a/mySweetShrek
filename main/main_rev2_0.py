import os
import discord
import json
from discord.ext import commands
from decouple import config

TOKEN = config('DISCORD_TOKEN') # DISCORD TOKEN IN ENV VAR
GUILD = config('DISCORD_GUILD') # DISCORD GUILD IN ENV VAR
DEF_CHAN = config('DISCORD_DEF_CHAN') # DISCORD DEFAULT CHANNEL IN ENV VAR  
ADMIN_ROLE_ID = config('DISCORD_ADMIN_ROLE_ID') # DISCORD ADMIN ROLE IDENTIFIER

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    
    default_chan = client.get_channel(int(DEF_CHAN))    # DEFINE THE DEFAULT CHANNEL THE BOT WILL BE DEBUGGED IN

    global guild 
    for guild in client.guilds:                         # DEFINE THE VAR GUILD TO BE EQUAL TO THE CURRENT GUILD
        if guild.name == GUILD:
            break

    print(
        f'\n##########    BOT INFORMATION     ##########'
        f'\n'
        f'\n1.         Bot ID: {client.user}'
        f'\n2.         Guild Name: {guild.name}'
        f'\n3.         Guild ID: {guild.id}'
        f'\n4.         Default Channel: {default_chan.name}'
        f'\n5.         Guild Owner: {guild.owner}'
        f'\n'
        f'\n############################################'
    )

    await default_chan.send(f"I'm up and running my dude :sunglasses:")
    init_cog()

                    # !load -- MANUALLY LOAD COGS
@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.reply(f':ballot_box_with_check:   {extension} has been successfully loaded!')

@load.error
async def error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply(f'Oops! You need to specify a cog!\n- `!load <cog>`')

                # !unload -- MANUALLY UNLOAD COGS
@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.reply(f':ballot_box_with_check:   {extension} has been successfully unloaded!')

@unload.error
async def error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply(f'Oops! You need to specify a cog!\n- `!unload <cog>`')

                # !reload -- RELOAD COGS
@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.reply(f':ballot_box_with_check:   {extension} has been successfully reloaded!')

@reload.error
async def error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply(f'Oops! You need to specify a cog!\n- `!reload <cog>`')

                # !coglist OR !cl -- LIST ALL THE AVAILABLE COGS.
@client.command(aliases=['cl'])
async def coglist(ctx):
    coglist = []
    
    for filename in os.listdir('./main/cogs'):
        if filename.endswith('.py') and filename != 'facts_dic.py':
            coglist.append(filename[:-3])
    
    coglist = f'\n- '.join([i for i in coglist])

    await ctx.send(f'Here is the list of the cogs:\n- {coglist}')

@client.command()
async def source(ctx):
    await ctx.reply(
        f'Here is the GitHub link of the bot:'
        f'\nhttps://github.com/opaa-a/mySweetShrek'
        )

def init_cog():
    for filename in os.listdir('./main/cogs'):         
        if filename.endswith(".py"):
            client.load_extension(f'cogs.{filename[:-3]}')
            
client.run(TOKEN)   