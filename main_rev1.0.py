import discord
from decouple import config
from discord.ext import commands

TOKEN = config('DISCORD_TOKEN') # BOT TOKEN
GUILD = config('DISCORD_GUILD') # DISCORD SERVER TOKEN

intents = discord.Intents(messages=True,guilds=True,reactions=True,members=True,presences=True)   # SETUP INTENTS
client = commands.Bot(command_prefix= '!', intents=intents)  # SETUP THE CLIENT & PREFIX OF COMMANDS

@client.event
async def on_ready():
    
    for guild in client.guilds: # CHECK FOR THE GUILD BOT IS IN.
        if guild.name == GUILD:
            break

    print(
        f'\n{client.user} IS OUT OF THE SWAMP AND READY TO ROCK THE SERVER!'    # PRINT INFORMATIONS OF SELF AND SERVER CONNECTED TO
        f'\n - Bot ID: {client.user}'
        f'\n - Guild Name: {guild.name}'
        f'\n - Guild ID: {guild.id}'
    )

@client.command(aliases=['p'])      # COMMAND PING
async def ping(ctx):
    await ctx.send(f'{round(client.latency * 1000)} ms')

@client.command(aliases=['sw'])
async def swamp(ctx):
    await ctx.send(f"GET OUT OF ME SWAMP YA OLD CHUM'")

@client.command(aliases=['ml'])
async def memberList(ctx, p):

    if p == "name":
        guild = GUILD
        for member in guild.members:
            id = member.id
        await ctx.send(
            f'\nParamater is "{p}".'
            f'\nHere is the list of all the members of "{guild.name}"'
            f'\n{id}'
        )
    else:
        await ctx.send(f'Lack of paramater.')


@client.command(aliases=['sw@'])
async def swampAt(ctx, user):
    pass

client.run(TOKEN)