import discord
from decouple import config
from discord.ext import commands

TOKEN = config('DISCORD_TOKEN') # BOT TOKEN
GUILD = config('DISCORD_GUILD') # DISCORD SERVER TOKEN

intents = discord.Intents(messages=True,guilds=True,reactions=True,members=True,presences=True)   # SETUP INTENTS
client = commands.Bot(command_prefix= '!', intents=intents)  # SETUP THE CLIENT & PREFIX OF COMMANDS

@client.event
async def on_ready():
    global guild
    for guild in client.guilds: # CHECK FOR THE GUILD BOT IS IN.
        if guild.name == GUILD:
            break

    print(
        f'\n{client.user} IS OUT OF THE SWAMP AND READY TO ROCK THE SERVER!'    # PRINT INFORMATIONS OF SELF AND SERVER CONNECTED TO
        f'\n - Bot ID: {client.user}'
        f'\n - Guild Name: {guild.name}'
        f'\n - Guild ID: {guild.id}'
    )

def unfoldList(listName):
    unfold = f'\n - '.join([i for i in listName])
    return unfold
    

def guildMembers(ml, lp):  # FUNCTION TO LIST ALL GUILD MEMBERS
   
    ml = []

    for member in guild.members:
        if lp == "name":
            ml = f'\n - '.join([member.name for member in guild.members])
        elif lp == "id":
            ml = f'\n - '.join([member.id for member in guild.members])
    return ml


def invalidParameter(parameters):
    error_msg = f'Invalid Parameter, try again using:\n - {unfoldList(parameters)}'
    return error_msg
        

@client.command(aliases=['p'])      # COMMAND PING
async def ping(ctx):
    await ctx.send(f'{round(client.latency * 1000)} ms')

@client.command(aliases=['sw'])
async def swamp(ctx):
    await ctx.send(f"GET OUT OF ME SWAMP YA OLD CHUM'")

@client.command(aliases=['ml'])

async def ml_parameter_missing(ctx):
    parameter = ['name','id']
    await ctx.reply(invalidParameter(parameter))

async def memberList(ctx, lp):

    if lp != "name" and lp != "id":
        await ctx.send(
            f'Parameter "{lp}" is unvalid!"'
            f'\nPlease use either "name" or "id" as parameter.'
            )
    
    else:
        await ctx.send(
            f'Here the {lp} of the members of the server: '
            f'\n\n - {guildMembers("member list", lp)}'
            )

@client.command(aliases=['sw@'])
async def swampAt(ctx):
    pass


client.run(TOKEN)