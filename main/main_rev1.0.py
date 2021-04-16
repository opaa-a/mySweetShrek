import discord
import random
from shrek_dictionary import *
from decouple import config
from discord.ext import commands

TOKEN = config('DISCORD_TOKEN') # BOT TOKEN
GUILD = config('DISCORD_GUILD') # DISCORD SERVER TOKEN
TEST_CHAN = config('DISCORD_TEST_CHAN') # DISCORD DEFAULT/ TEST CHANNEL

intents = discord.Intents(messages=True,guilds=True,reactions=True,members=True,presences=True)   # SETUP INTENTS
client = commands.Bot(command_prefix= '!', intents=intents)  # SETUP THE CLIENT & PREFIX OF COMMANDS

@client.event
async def on_ready():

    test_chan = client.get_channel(int(TEST_CHAN))

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

    await test_chan.send(
        f'{client.user} Is lit and drip :joy:'
        )

def unfoldList(listName):
    unfold = f'\n - '.join([i for i in listName])
    return unfold
    

def guildMembers(ml, lp):  # FUNCTION TO LIST ALL GUILD MEMBERS
    ml = []
    for member in guild.members:        # LP = LIST PARAMETER / ML = MEMBER LIST
        if lp == "name":
            ml = f'\n - '.join([member.name for member in guild.members])
        elif lp == "id":
            ml = f'\n - '.join([str(member.id) for member in guild.members])
    return ml   


def invalidParameter(parameters):       # DEFAULT MESSAGE WHEN NO PARAMETERS ARE GIVEN
    error_parameter = f'Invalid Parameter, try again using:\n - {unfoldList(parameters)}'
    return error_parameter
        

@client.command(aliases=['p'])      # PING COMMAND
async def ping(ctx):
    await ctx.send(f'{round(client.latency * 1000)} ms')

@client.command(aliases=['sw'])     # SWAMP COMMAND
async def swamp(ctx):
    await ctx.send(f"GET OUT OF ME SWAMP YA OLD CHUM'")

@client.command(aliases=['ml'])    # MEMBER LIST COMMAND -- NAME OR ID AS PARAMETER
async def memberList(ctx, lp):
    parameter = ['name','id']

    if lp != "name" and lp != "id":
        await ctx.reply(invalidParameter(parameter))
    
    else:
        await ctx.send(
            f'Here the {lp} of the members of the server: '
            f'\n\n - {guildMembers("member list", lp)}'
            )

@client.command(aliases=['@'])      # SWAMP AT COMMAND --  USERNAME AS PARAMETER
async def swampAt(ctx, target : discord.Member):
    await ctx.send(f"OI {target.mention}, GET THE FUCK OFF ME SWAMP YA OLD CHUM'")

@swampAt.error
async def error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send(f'Username is not valid!')

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
        await answer.reply(f'Success! :joy::ok_hand:')

client.run(TOKEN)