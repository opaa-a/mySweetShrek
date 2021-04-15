import discord
import random
from shrek_dictionary import *
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
            ml = f'\n - '.join([str(member.id) for member in guild.members])
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
async def memberList(ctx, lp):
    parameter = ['name','id']

    if lp != "name" and lp != "id":
        await ctx.reply(invalidParameter(parameter))
    
    else:
        await ctx.send(
            f'Here the {lp} of the members of the server: '
            f'\n\n - {guildMembers("member list", lp)}'
            )

@client.command(aliases=['@'])
async def swampAt(ctx, name):
    memberNames = []
    for member in guild.members:
        memberNames.append(member.name)
        if name == member.name:
            await ctx.send(f"{member.mention} YOU BETTER GET OUT OF ME SWAMP BEFORE I SLAP YOUR STUPID ASS")
            break
    if name not in memberNames:
        await ctx.send(f'{name} is not a valid username!')


@client.command(aliases=['fa'])
async def swampFact(ctx):

    channel = ctx.channel
    random_fact = random.choice(fact_list)
    fact_index = fact_list.index(random_fact)
    await ctx.send(random_fact)

    def check(ans):
        if ans.content == answer_list[fact_index] and ans.channel == channel:
            return ans.content, ans.channel
    if  answer_list[fact_index] == 'null':
        print('break; no answer expected')
    else:
        answer = await client.wait_for('message', check=check, timeout=15)
        await answer.reply(f'Success!') 

    '''
    @client.event 
    async def on_message(message):
        if message.content != "null" and message.content == answer_list[i]:
            await ctx.reply(f'Bon toutou')
        else:
            await ctx.reply(f'test')
    '''

client.run(TOKEN)