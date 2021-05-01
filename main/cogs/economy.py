import discord
import json
import random
import asyncio
import datetime
from dialogue.dialogue import *
from dialogue.errors import *
from decouple import config
from discord.ext import commands
from facts_dic import *


#---------------------------------------------------------------------------------------#       GLOBAL VARIABLES       #---------------------------------------------------------------------------------------#

# ID of the admin role on the current server. (used to check if a user is an admin)
ADMIN_ROLE_ID = config('DISCORD_ADMIN_ROLE_ID')


#---------------------------------------------------------------------------------------#        GLOBAL FUNCTIONS       #---------------------------------------------------------------------------------------#

# get_vault will search through the vault.json file with the userID specified
# and return user_has_vault as TRUE if userID is in vault or FALSE if userID isn't in the vault.
def get_vault(userID : discord.Member):
    with open('./main/vault.json', 'r') as vault:
        vault = json.load(vault)
        userID = str(userID)
        
        global user_has_vault
        user_has_vault = False

        for profile in vault:
            if userID == profile:
                user_has_vault = True
                return user_has_vault


# edit_vault is a simple updater function for the vault. when updates are made to the vault,
# this function is called and it will dump the updated version of the vault.json
def edit_vault(data, filename='./main/vault.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
        file.close()


# check_admin as his name suggest, is a function to check is a specified userID is admin or not.
# It will return user_is_admin either as TRUE if userID is admin or FALSE if userID is not.
def check_admin(userID : discord.Member):
    aID = int(ADMIN_ROLE_ID)
    userRoles = []
    
    global user_is_admin
    user_is_admin = False

    for role in userID.roles:
        userRoles.append(role.id)
    
    if aID in userRoles:
        user_is_admin = True
        return user_is_admin


# md_balance (modify balance) is a function that take a userID, a method (add, sub or reset) and an amount.
# The userID will either have the amount substracted or added to his account. If reset is used, his account will be wiped.
def md_balance(userID : discord.Member, md_method : str, amount : int):       
    with open('./main/vault.json') as vault:
        vault = json.load(vault)
        userID = str(userID)

        for profile in vault:
            if profile == userID:
                if md_method == "add":
                    vault[userID]["balance"] += amount
                elif md_method == "sub":
                    vault[userID]["balance"] -= amount
                elif md_method == "reset":
                    vault[userID]["balance"] = 0

    edit_vault(vault)


# get_balance will return the balance of the userID specified as a int variable named balance.
def get_balance(userID):
    with open('./main/vault.json') as vault:
        vault = json.load(vault)
        userID = str(userID)

        global balance
        balance = 0

        for profile in vault:
            if profile == userID:
                balance = vault[userID]["balance"]
                return balance


# check_pay take a userID and an amount. The function will check if userID has a vault, 
# if TRUE then the function will check if the balance is greater than the amount. 
# If TRUE, canUserpay will return as TRUE. If FALSE, userCanPay will return as FALSE.  
def check_pay(userID, amount):
    global canUserPay
    canUserPay = False
    
    get_vault(userID)
    get_balance(userID)

    if user_has_vault == False:
        return canUserPay
        
    if balance >= amount:
        canUserPay = True
        return canUserPay


#---------------------------------------------------------------------------------------#      ECONOMY ESSENTIALS COMMANDS      #---------------------------------------------------------------------------------------#

# Economy Essentials will regroup every essentials commands for using the economy system.
class Economy_Essentials(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f"\n- Economy Essentials from bank is loaded.")


# !register -- Take no args. Register the author of the command to the vault.
    @commands.command()
    async def register(self, ctx):
        author = str(ctx.author)

        with open('./main/vault.json') as vault:
            vault = json.load(vault)
            registery = []

            for profile in vault:
                registery.append(profile)
                
            if  author in registery:
                await ctx.reply(error_user_is_already_registered())

            else:
                vault[author] = {"balance": 0, "reward": {"daily_reward_claim_date": False}}
                await ctx.reply(register_success())

        edit_vault(vault)


# !addcoins -- ADMIN ONLY. Take 2 args, a target userID and an amount.
    @commands.command()
    async def addcoins(self, ctx, amount : int, userID : discord.Member = None):
        amount = abs(amount)
        if userID == None:
            userID = ctx.author

        check_admin(ctx.author)
        if user_is_admin != True:
            return await ctx.reply(error_user_is_not_admin())
        
        get_vault(userID)
        if user_has_vault != True and userID == ctx.author:
            return await ctx.reply(error_user_has_no_vault())
        elif user_has_vault != True:
            return await ctx.reply(error_user_has_no_vault(userID))

        md_balance(userID, "add", amount)
        if userID == ctx.author:
            return await ctx.reply(addcoins_success(amount))
        return await ctx.send(addcoins_success(amount, userID))                


# !balance OR !bal -- Take an optionnal arg: userID. Show the balance of the userID, 
# by default the author is the userID
    @commands.command(aliases=['bal'])
    async def balance(self, ctx, userID : discord.Member = None):
        author = False
        if userID == None:
            userID = str(ctx.author)
            author = True

        get_vault(userID)
        if user_has_vault != True and author:
            return await ctx.reply(error_user_has_no_vault())
        elif user_has_vault != True:
            return await ctx.reply(error_user_has_no_vault(userID))
        
        get_balance(userID)
        if author:
            return await ctx.send(balance_success(balance))
        return await ctx.send(balance_success(balance, userID))


# !balancetop OR !baltop -- Takes no args. Display all the accounts on the vault,
# ordered from richest to poorest (first to last).
    @commands.command(aliases=['baltop'])
    async def balancetop(self, ctx):
        
        with open('./main/vault.json') as vault:
            vault = json.load(vault)
            profiles = {}
            pre_format_baltop = []
            index = 0

            for profile in vault:
                bal = vault[profile]["balance"]
                profiles[profile] = bal
                baltop = sorted(profiles.items(), key=lambda x: x[1], reverse=True)

            await ctx.send(balancetop_success(baltop))


# !pay -- Take 2 args, userID and amount. Transfer amount from the author balance to the userID balance.
    @commands.command()
    async def pay(self, ctx, userID : discord.Member, amount : int):
        author = ctx.author
        amount = abs(amount)
        
        if userID == author:
            return await ctx.reply(error_user_cant_pay_himself())

        get_vault(author)
        if user_has_vault != True:
            return await ctx.reply(error_user_has_no_vault())

        get_vault(userID)
        if user_has_vault != True:
            return await ctx.reply(error_user_has_no_vault(userID))

        check_pay(author, amount)
        if canUserPay == True:
            md_balance(author, "sub", amount)
            md_balance(userID, "add", amount)
            return await ctx.reply(pay_success(amount, userID))

        return await ctx.reply(error_user_cant_pay())


#---------------------------------------------------------------------------------------#   ECONOMY ESSENTIALS ERRORS   #---------------------------------------------------------------------------------------#

# !addcoins error display
    @addcoins.error
    async def error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            return print(log_error_bad_arg("addcoins")), await ctx.reply(error_addcoins("bad_arg"))
        elif isinstance(error, commands.MissingRequiredArgument):
            return print(log_error_missing_arg("addcoins")), await ctx.reply(error_addcoins("missing_arg"))

        return await ctx.reply(f':exclamation: Unknown error, please contact the administrator.')
# !balance error display
    @balance.error
    async def error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            return print(log_error_missing_arg("balance")), await ctx.reply(error_balance("bad_arg"))
        return await ctx.reply(f':exclamation: Unknown error, please contact the administrator.')
# !pay error display
    @pay.error
    async def error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            return print(log_error_bad_arg(pay)), await ctx.reply(error_pay("bad_arg"))
        elif isinstance(error, commands.MissingRequiredArgument):
            return print(log_error_missing_arg(pay)), await ctx.reply(error_pay("missing_arg"))
        return await ctx.reply(f':exclamation: Unknown error, please contact the administrator.')

#---------------------------------------------------------------------------------------#       ECONOMY GRIND       #---------------------------------------------------------------------------------------#

# Economy Grind will regroup all the commands related to grinding of {currency}.
class Economy_Grind(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f"\n- Economy Grind from bank is loaded.")


# !coinflip OR !cf -- Takes one arg. Amount. Expect an answer after first message.
# Either Head or Tail, a coin is tossed, if author wins, he double his bet. If author lose,
# he lose the double of his bet.
    @commands.command(aliases=['cf'])
    async def coinflip(self, ctx, amount : int):
        bully = "Valgen#3271"
        amount = abs(amount)
        author = ctx.author
        channel = ctx.channel
        cf_prize = amount * 2
        coin_faces = ["head","tail"]

        get_vault(author)
        if user_has_vault == False:
            return await ctx.reply(
                f':x:   You don\'t even have an account, how do you expect to get {currency} exactly?'
                f'\n`- !register `     To register an account.'
                )

        get_balance(author)
        if balance < amount:
            return await ctx.reply(
                f':x:   You don\'t have enough money you fuckin\' donkey.'
                f'\n`- !balance `      To see how poor you are.'
                )

        await ctx.send(
            f':coin:  **{author}** is in a playful mood, {amount} {currency} have been bet! **head** or **tail**.'
            f'\n*you got to write it, like with your keyboard and stuff...*'
            )
        
        def check(ans):
            return ans.channel == ctx.channel and ans.author == ctx.author

        answer = await self.client.wait_for('message', check=check)

        if answer.content != 'tail' and answer.content != 'head':
            return await ctx.reply(
            f'You failed answering a simple "head or tail" question, no doubt that\'s why your life sucks.'
            f'\n`- !cf <amout> `    To try again.'                
            )

        guess = answer.content
        cf_result = random.choice(coin_faces)
        
        if str(author) == bully:
            while guess == cf_result:
                cf_result = random.choice(coin_faces)

        await ctx.send(
            f'And the result is...'
            )
        await asyncio.sleep(1)
        await ctx.send(
            f'**{cf_result}**! :coin:'
            )
        await asyncio.sleep(1)

        if cf_result != guess:
            md_balance(author, "sub", cf_prize)
            return await ctx.send(
                f'Congratulations **{author}**, you fucking lost **{cf_prize}** {currency} :joy::ok_hand:'
                )
        
        md_balance(author, "add", cf_prize)
        return await ctx.send(
            f'Okay okay, the luck was with you on this one {author}, you won **{cf_prize}** {currency} :confetti_ball:'
            )


# !facts OR !fa -- Takes no arg, but expect an answer. Send a fact to the context channel. 
# First person to get the right answer to the fact will earn between 1 and 15 {currency}.
    @commands.command(aliases=['fa'])
    async def facts(self, ctx):

        client = discord.Client
        channel = ctx.channel
        random_fact = random.choice(fact_list)
        fact_index = fact_list.index(random_fact)
        prize = random.randint(1,15)

        await ctx.send(random_fact)

        def check(ans):
            return ans.content == answer_list[fact_index] and ans.channel == channel
        
        if answer_list[fact_index] != "null":
            answer = await client.wait_for(self.client, 'message', check=check, timeout=15)
            get_vault(answer.author)            
            
            if  user_has_vault == True:
                md_balance(answer.author, "add", prize)
                await answer.reply(
                    f'Got it! :joy::ok_hand:'
                    f'*You earned {prize} {currency}!*'
                    )
            else:
                await answer.reply(
                    f'Got it! :joy::ok_hand:'
                    f'\n*You won nothing cuz you ain\'t registered, you fucking nerd.*'
                    )
        else:
            print('\n!facts ; break ; no answer needed.')


#---------------------------------------------------------------------------------------#   ECONOMY GRIND ERRORS   #---------------------------------------------------------------------------------------#

# !coinflip error display
    @coinflip.error
    async def error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(
                f':x:   Ohoh! Looks like you forgot to specify the amount!'
                f'\n`- !cf <amount> `'
                )
        elif isinstance(error, commands.BadArgument):
            await ctx.reply(
                f':x:   Ohoh! Looks like you don\'t know what a fucking number is!'
                f'\n`- !cf <amount> ` (amount being a number...)'
                )


#---------------------------------------------------------------------------------------#       ECONOMY REWARDS       #---------------------------------------------------------------------------------------#

class Economy_Reward(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f"\n- Economy Rewards from bank is loaded.")

#---------------------------------------------------------------------------------------#       REWARDS FUNCTIONS       #---------------------------------------------------------------------------------------#

    def daily_reward(ctx, userID : discord.Member):
        with open('./main/vault.json') as vault:
            vault = json.load(vault)
            
            claim_feedback = (
                f':x:   Looks like you already claimed that reward. Wait until tomorrow.'
                )
            date_now = str(datetime.date.today())
            reward = 1000
            
            userID = str(userID)
            dlr_claim = vault[userID]["reward"]["daily_reward_claim_date"]

            if dlr_claim == False:
                vault[userID]["reward"]["daily_reward_claim_date"] = date_now
                vault[userID]["balance"] += reward
                claim_feedback = (
                    f':partying_face:   | **{userID} is claiming his very first daily reward!**'
                    f'\n:coin:   | *{userID} got 1000 {currency} from his daily reward!*'
                    f'\n`- !claim daily `     *to get your own daily reward*'
                    )

                edit_vault(vault)
                return claim_feedback

            if dlr_claim < date_now:
                vault[userID]["reward"]["daily_reward_claim_date"] = date_now
                vault[userID]["balance"] += reward
                claim_feedback = (
                    f':calendar:   | {userID} Has claim his daily reward.'
                    f'\n:coin:   | {reward} {currency} Have been added to {userID}\'s account!'
                    f'\n`- !claim daily`    *To claim your own daily reward!*'
                    )

                edit_vault(vault)
                return claim_feedback

            return claim_feedback


#---------------------------------------------------------------------------------------#       ECONOMY REWARDS COMMANDS      #---------------------------------------------------------------------------------------#

    @commands.command()
    async def claim(self, ctx, reward_type : str = None):
        
        get_vault(ctx.author)
        if user_has_vault == False:
            return await ctx.reply(error_user_has_no_vault())
        
        if reward_type == None:
            return await ctx.reply(
                f'Here is the list of the your rewards waiting to be claimed:'
                f'\n- '
                )

        if reward_type == "daily":
            return await ctx.reply(self.daily_reward(ctx.author))
#---------------------------------------------------------------------------------------#   ECONOMY REWARDS ERRORS   #---------------------------------------------------------------------------------------#



#---------------------------------------------------------------------------------------#       COGS SETUP      #---------------------------------------------------------------------------------------#

def setup(client):
    client.add_cog(Economy_Essentials(client))
    client.add_cog(Economy_Grind(client))
    client.add_cog(Economy_Reward(client))