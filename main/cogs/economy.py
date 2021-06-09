import discord
import json
import random
import asyncio
import datetime
from discord.ext import commands
from discord.ext import tasks
from decouple import config
from dialogue.dialogue import *
from dialogue.errors import *
from facts_dic import *


#---------------------------------------------------------------------------------------#       GLOBAL VARIABLES       #---------------------------------------------------------------------------------------#

# ID of the admin role on the current server. (used to check if a user is an admin)
ADMIN_ROLE_ID = config('DISCORD_ADMIN_ROLE_ID')


#---------------------------------------------------------------------------------------#        GLOBAL FUNCTIONS       #---------------------------------------------------------------------------------------#

# get_vault will search through the vault.json file with the userID specified
# and return get_vault as TRUE if userID is in vault or FALSE if userID isn't in the vault.
def get_vault(userID : discord.Member):
    with open('./main/assets/vault.json', 'r') as vault:
        vault = json.load(vault)
        userID = str(userID)

        if userID in vault:
            return True
        return False


# edit_vault is a simple updater function for the vault. when updates are made to the vault,
# this function is called and it will dump the updated version of the vault.json
def edit_vault(data, filename='./main/assets/vault.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
        file.close()


# check_admin as his name suggest, is a function to check is a specified userID is admin or not.
# It will return check_admin either as TRUE if userID is admin or FALSE if userID is not.
def check_admin(userID : discord.Member):
    aID = int(ADMIN_ROLE_ID)
    userRoles = []

    for role in userID.roles:
        userRoles.append(role.id)
    
    if aID in userRoles:
        return True
    return False


# md_balance (modify balance) is a function that take a userID, a method (add, sub or reset) and an amount.
# The userID will either have the amount substracted or added to his account. If reset is used, his account will be wiped.
def md_balance(userID : discord.Member, md_method : str, amount : int):       
    with open('./main/assets/vault.json') as vault:
        vault = json.load(vault)
        userID = str(userID)

        if userID in vault:
            if md_method == "add":
                vault[userID]["balance"] += amount
            elif md_method == "sub":
                vault[userID]["balance"] -= amount
            elif md_method == "reset":
                    vault[userID]["balance"] = 0

    edit_vault(vault)


# get_balance will return the balance of the userID specified as a int through the function.
def get_balance(userID):
    with open('./main/assets/vault.json') as vault:
        vault = json.load(vault)
        userID = str(userID)

        global balance
        balance = 0

        if userID in vault:
            balance = vault[userID]["balance"]
            return balance
        return False

# check_pay take a userID and an amount. The function will check if userID has a vault, 
# if TRUE then the function will check if the balance is greater than the amount. 
# If TRUE, canUserpay will return as TRUE. If FALSE, userCanPay will return as FALSE.  
def check_pay(userID, amount):
    if get_vault(userID) == False:
        return False
        
    if get_balance(userID) >= amount:
        return True
    return False


#---------------------------------------------------------------------------------------#      ECONOMY ESSENTIALS COMMANDS      #---------------------------------------------------------------------------------------#

# Economy Essentials will regroup every essentials commands for using the economy system.
class Economy_Essentials(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f"\n- Economy Essentials from bank.py is loaded.")

# display the help economy section
    async def help_economy(self,ctx):
        await ctx.author.send(help_economy_success())
        #check if theme is selected
        def check(querry):
            return ctx.author == querry.author
        querry = await self.client.wait_for('message', check=check, timeout = 20)
        # iterate through the help file to fetch the store theme.
        with open('main/assets/help.json') as help_index:
            help_economy = json.load(help_index)
            help_economy = help_economy["Economy"]
            help_economy_exp_list = list(help_economy.values())
            help_economy_exp_index_list = []
            for i in help_economy_exp_list:
                help_economy_exp_index_list.append(help_economy_exp_list.index(i))
            #return if querry unvalid
            try:
                if int(querry.content) not in help_economy_exp_index_list:
                    return await ctx.author.send(querry_exit('unknown_ID', 'economy help'))
            # return if querry is not int
            except ValueError:
                return await ctx.author.send(querry_exit('valueError_int', 'economy help'))
            #return if querry successful
            return await ctx.author.send(help_economy_querry(int(querry.content)))


# !register -- Take no args. Register the author of the command to the vault.
    @commands.command()
    async def register(self, ctx):
        author = str(ctx.author)

        with open('./main/assets/vault.json') as vault:
            vault = json.load(vault)
            registery = []

            for profile in vault:
                registery.append(profile)
                
            if  author in registery:
                await ctx.reply(error_user_is_already_registered())

            else:
                vault[author] = {"balance": 0, "reward": {"daily_reward_claim_date": False}, "inventory": {}}
                await ctx.reply(register_success())

        edit_vault(vault)


# !addcoins -- ADMIN ONLY. Take 2 args, a target userID and an amount.
    @commands.command()
    async def addcoins(self, ctx, amount : int, userID : discord.Member = None):
        amount = abs(amount)
        if userID == None:
            userID = ctx.author

        if check_admin(ctx.author) != True:
            return await ctx.reply(error_user_is_not_admin())

        if get_vault(userID) != True and userID == ctx.author:
            return await ctx.reply(error_user_has_no_vault())
        elif get_vault(userID) != True:
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

        if get_vault(userID) != True and author:
            return await ctx.reply(error_user_has_no_vault())
        elif get_vault(userID) != True:
            return await ctx.reply(error_user_has_no_vault(userID))
        
        get_balance(userID)
        if author:
            return await ctx.send(balance_success(balance))
        return await ctx.send(balance_success(balance, userID))


# !balancetop OR !baltop -- Takes no args. Display all the accounts on the vault,
# ordered from richest to poorest (first to last).
    @commands.command(aliases=['baltop'])
    async def balancetop(self, ctx):
        
        with open('./main/assets/vault.json') as vault:
            vault = json.load(vault)
            profiles = {}

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

        if get_vault(author) != True:
            return await ctx.reply(error_user_has_no_vault())

        if get_vault(userID) != True:
            return await ctx.reply(error_user_has_no_vault(userID))

        if check_pay(author, amount) == True:
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
        return await ctx.reply(unknown_error())

# !balance error display
    @balance.error
    async def error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            return print(log_error_missing_arg("balance")), await ctx.reply(error_balance("bad_arg"))
        return await ctx.reply(unknown_error())

# !pay error display
    @pay.error
    async def error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            return print(log_error_bad_arg("pay")), await ctx.reply(error_pay("bad_arg"))
        elif isinstance(error, commands.MissingRequiredArgument):
            return print(log_error_missing_arg("pay")), await ctx.reply(error_pay("missing_arg"))
        return await ctx.reply(unknown_error())

#---------------------------------------------------------------------------------------#       ECONOMY GRIND       #---------------------------------------------------------------------------------------#

# Economy Grind will regroup all the commands related to grinding of {currency}.
class Economy_Grind(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f'\n- Economy Grind from bank.py is loaded.')

# display the help grind section
    async def help_grind(self,ctx):
        await ctx.author.send(help_grind_success())
        #check if theme is selected
        def check(querry):
            return ctx.author == querry.author
        querry = await self.client.wait_for('message', check=check, timeout = 20)
        # iterate through the help file to fetch the store theme.
        with open('main/assets/help.json') as help_index:
            help_grind = json.load(help_index)
            help_grind = help_grind["Grind"]
            help_grind_exp_list = list(help_grind.values())
            help_grind_exp_index_list = []
            for i in help_grind_exp_list:
                help_grind_exp_index_list.append(help_grind_exp_list.index(i))
            #return if querry int unvalid
            try:
                if int(querry.content) not in help_grind_exp_index_list:
                    return await ctx.author.send(querry_exit('unknown_ID', 'grind help'))
            # return if querry is not int
            except ValueError:
                return await ctx.author.send(querry_exit('valueError_int', 'grind help'))
            #return if querry successful
            return await ctx.author.send(help_grind_querry(int(querry.content)))

# !coinflip OR !cf -- Takes one arg. Amount. Expect an answer after first message.
# Either Head or Tail, a coin is tossed, if author wins, he double his bet. If author lose,
# he lose the double of his bet.
    @commands.command(aliases=['cf'])
    async def coinflip(self, ctx, amount : int):
        from cogs.essential import check_user_has_role
        from cogs.essential import malus_rate
        from cogs.essential import bonus_rate

        amount = abs(amount)
        author = ctx.author
        cf_prize = amount * 2
        coin_faces = ["head","tail"]

        if get_vault(author) != True:
            return await ctx.reply(error_user_has_no_vault())

        if get_balance(author) < amount:
            return await ctx.reply(error_user_cant_pay())
        
        # add malus rate to the prize if user is 'mauvais toutou'
        if check_user_has_role(ctx.author, 805897076437155861):
            cf_prize = cf_prize - cf_prize * malus_rate
        # add bonus rate to the prize if user is 'bon toutou'
        if check_user_has_role(ctx.author, 804849555094765598):
            cf_prize = cf_prize * bonus_rate

        await ctx.send(coinflip_success(amount, author, "cf_init"))
        
        def check(ans):
            return ans.channel == ctx.channel and ans.author == ctx.author

        ans = await self.client.wait_for('message', check=check)

        if ans.content.lower() != 'tail' and ans.content.lower() != 'head':
            return await ctx.reply(error_coinflip("fail_ans"))

        guess = ans.content.lower()
        cf_result = random.choice(coin_faces)
        
        # if str(author) == bully:
        #     while guess == cf_result:
        #         cf_result = random.choice(coin_faces)

        await ctx.send(
            f'And the result is...'
            )
        await asyncio.sleep(1)
        await ctx.send(
            f'**{cf_result}**! :coin:'
            )
        await asyncio.sleep(1)

        if cf_result != guess:
            md_balance(author, "sub", amount)
            return await ctx.send(coinflip_success(amount, author, "cf_lose"))
        
        md_balance(author, "add", cf_prize)
        return await ctx.send(coinflip_success(cf_prize, author, "cf_win"))


# !facts OR !fa -- Takes no arg, but expect an answer. Send a fact to the context channel. 
# First person to get the right answer to the fact will earn between 1 and 15 {currency}.
    @commands.command(aliases=['fa'])
    async def facts(self, ctx):
        from cogs.essential import check_user_has_role
        from cogs.essential import malus_rate
        from cogs.essential import bonus_rate

        client = discord.Client
        channel = ctx.channel
        random_fact = random.choice(fact_list)
        fact_index = fact_list.index(random_fact)
        prize = random.randint(1,15)

        # add malus rate to the prize if user is 'mauvais toutou'
        if check_user_has_role(ctx.author, 805897076437155861):
            prize = prize - prize * malus_rate
        # add bonus rate to the prize if user is 'bon toutou'
        if check_user_has_role(ctx.author, 804849555094765598):
            prize = prize * bonus_rate

        await ctx.send(random_fact)

        def check(ans):
            return ans.content == answer_list[fact_index] and ans.channel == channel and ans.author != discord.Member.bot
        
        if answer_list[fact_index] != "null":
            answer = await client.wait_for(self.client, 'message', check=check, timeout=15)
            
        if  get_vault(answer.author) != True:
            return await answer.reply(facts_success("success_without_vault", prize))
            
        md_balance(answer.author, "add", prize)
        return await answer.reply(facts_success("success_with_vault", prize))

#---------------------------------------------------------------------------------------#   ECONOMY GRIND ERRORS   #---------------------------------------------------------------------------------------#

# !coinflip error display
    @coinflip.error
    async def error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply(error_coinflip("bad_arg"))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(error_coinflip("missing_arg"))
#---------------------------------------------------------------------------------------#       ECONOMY REWARDS       #---------------------------------------------------------------------------------------#

class Economy_Reward(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f"\n- Economy Rewards from bank.py is loaded.")

#---------------------------------------------------------------------------------------#       REWARDS FUNCTIONS       #---------------------------------------------------------------------------------------#

# daily_reward is the a daily claimable reward with a default amount of 1000
    def daily_reward(self, ctx, userID : discord.Member):
        from cogs.essential import check_user_has_role
        from cogs.essential import malus_rate
        from cogs.essential import bonus_rate

        with open('./main/assets/vault.json') as vault:
            vault = json.load(vault)
            date_now = str(datetime.date.today())
            reward = 1000
            
            userID = str(userID)
            dlr_claim = vault[userID]["reward"]["daily_reward_claim_date"]
            
            # add malus rate to the prize if user is 'mauvais toutou'
            if check_user_has_role(ctx.author, 805897076437155861):
                reward = reward - reward * malus_rate
            # add bonus rate to the prize if user is 'bon toutou'
            if check_user_has_role(ctx.author, 804849555094765598):
                reward = reward * bonus_rate

            if dlr_claim == False:
                vault[userID]["reward"]["daily_reward_claim_date"] = date_now
                vault[userID]["balance"] += reward
                edit_vault(vault)
                return daily_reward_success(userID, reward, "first_claim")

            if dlr_claim < date_now:
                vault[userID]["reward"]["daily_reward_claim_date"] = date_now
                vault[userID]["balance"] += reward
                edit_vault(vault)
                return daily_reward_success(userID, reward, "claim_success")

            return daily_reward_success(userID, reward)

#
    def passive_inc_reward(self, ctx):
        return

#---------------------------------------------------------------------------------------#       ECONOMY REWARDS COMMANDS      #---------------------------------------------------------------------------------------#

# !claim -- Takes an optionnal arg. Without arg, display the list of available rewards.
# With a reward name as a an arg, claim the specified reward if available.
    @commands.command()
    async def claim(self, ctx, reward_type : str = None):
        
        if get_vault(ctx.author) == False:
            return await ctx.reply(error_user_has_no_vault())
        
        if reward_type == None:
            return await ctx.reply(claim_success())

        if reward_type == "daily":
            return await ctx.reply(self.daily_reward(ctx, ctx.author))
        
        if reward_type == "p":
            return self.passive_inc_reward(ctx)


#---------------------------------------------------------------------------------------#   ECONOMY REWARDS ERRORS   #---------------------------------------------------------------------------------------#



#---------------------------------------------------------------------------------------#       COGS SETUP      #---------------------------------------------------------------------------------------#

def setup(client):
    client.add_cog(Economy_Essentials(client))
    client.add_cog(Economy_Grind(client))
    client.add_cog(Economy_Reward(client))