import discord
import json
import random
import asyncio
import datetime
from decimal import Decimal
from discord.ext import commands
from decouple import config
from dialogue.dialogue import *
from dialogue.errors import *
from dialogue.economy_dialogue import *


#---------------------------------------------------------------------------------------#       GLOBAL VARIABLES       #---------------------------------------------------------------------------------------#

# ID of the admin role on the current server. (used to check if a user is an admin)
ADMIN_ROLE_ID = config('DISCORD_ADMIN_ROLE_ID')

#---------------------------------------------------------------------------------------#        GLOBAL FUNCTIONS       #---------------------------------------------------------------------------------------#

# check_vault will search through the vault.json file with the userID specified
# and return check_vault as TRUE if userID is in vault or FALSE if userID isn't in the vault.
def check_vault(userID : discord.Member):
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
def md_balance(userID : discord.Member, method : str, amount: int):
    with open('./main/assets/vault.json') as vault:
        vault = json.load(vault)
        userID = str(userID)

        if userID in vault:
            if method == "add":
                vault[userID]["balance"] += amount
            elif method == "sub":
                vault[userID]["balance"] -= amount
            elif method == "reset":
                    vault[userID]["balance"] = 0
    edit_vault(vault)
    return print(Economy_Essential_Log.md_balance_log(userID, method, amount))

# get_balance will return the balance of the userID specified as a int through the function.
def get_balance(userID):
    with open('./main/assets/vault.json') as vault:
        vault = json.load(vault)
        userID = str(userID)

        if userID in vault:
            balance = vault[userID]["balance"]
            # balance = round(float(fbalance),2)
            return balance
        return False

# check_pay take a userID and an amount. The function will check if userID has a vault, 
# if TRUE then the function will check if the balance is greater than the amount. 
# If TRUE, canUserpay will return as TRUE. If FALSE, userCanPay will return as FALSE.  
def check_pay(userID, amount):
    if check_vault(userID) == False:
        return False
        
    if get_balance(userID) >= amount:
        return True
    return False

# check_former_bon_toutou is a function to check if a user registered into the vault has been the latest bon toutou
# This function will return a var userID that is a discord.Member.
def check_former_bon_toutou(userID: discord.Member):
    userID = str(userID)
    with open('./main/assets/vault.json') as vault:
        vault = json.load(vault)
        if vault[userID]['reward']['former_bon_toutou'] == True:
            return True
        return False

# md_bon_toutou_status will modify BOOL value of former_bon_toutou in the vault
# it will set to True to the new bon toutou and set to False to the former.
def md_bon_toutou_status(userID: discord.Member):
    userID = str(userID)
    with open('./main/assets/vault.json') as vault:
        vault = json.load(vault)
        for profile in vault:
            if vault[profile]['reward']['former_bon_toutou'] == True:
                vault[profile]['reward']['former_bon_toutou'] = False
        vault[userID]['reward']['former_bon_toutou'] = True
        edit_vault(vault)
        

#---------------------------------------------------------------------------------------#      ECONOMY ESSENTIALS COMMANDS      #---------------------------------------------------------------------------------------#

# Economy Essentials will regroup every essentials commands for using the economy system.
class Economy_Essentials(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f"\n{log_format.INFO}- Economy Essentials from bank.py is loaded.{log_format.END}")

# display the help economy section
    async def help_economy(self,ctx):
        await ctx.author.send(Economy_Essential_Dialogue.help_economy_function_success(ctx.author))
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
                    return await ctx.author.send(Global_Dialogue.querry_exit('unknown_ID', 'economy help', ctx.author))
            # return if querry is not int
            except ValueError:
                return await ctx.author.send(Global_Dialogue.querry_exit('valueError_int', 'economy help', ctx.author))
            #return if querry successful
            return await ctx.author.send(Economy_Essential_Dialogue.help_economy_querry(int(querry.content), ctx.author))


# !register -- Take no args. Register the author of the command to the vault.
    @commands.command()
    async def register(self, ctx):
        # log the command
        print(Global_Log.command_has_been_used('register', ctx.author))
        author = str(ctx.author)
        # call check_vault to check if user is already registered
        if check_vault(ctx.author):
            return await ctx.reply(Economy_Essential_ErrorHandler.user_already_registered())
        # if user not registered, dumb informations to the DB
        with open('./main/assets/vault.json') as vault:
            vault = json.load(vault)
            vault[author] = {"balance": 0, "reward": {"daily_reward_claim_date": False, "former_bon_toutou": False}, "inventory": {}}   ### IF ANYTHING IS ADDED TO THE VAULT PROFILE OF A USER, ADD VALUE AND KEY HERE.
        return edit_vault(vault), await ctx.reply(Economy_Essential_Dialogue.register_success())

# !reloadVAULT -- take no args. Reload the vault to dump new changes.
    @commands.command()
    async def reloadVAULT(self, ctx):
        # log 
        print(Global_Log.command_has_been_used('reloadVAULT', ctx.author))
        # check if user has permissions
        if check_admin(ctx.author) is False:
            return await ctx.reply(Global_Dialogue.user_not_allowed('reloadVAULT', ctx.author))
        # open vault
        with open('./main/assets/vault.json') as vault:
            vault = json.load(vault)
            for userID in vault:
                vault[userID]['reward']['former_bon_toutou'] = False ### THIS IS THE LINE TO CHANGE WHEN SOMTHING NEEDS TO BE DUMPED INTO THE VAULT
                # dump new content
                edit_vault(vault)
        # return dm
        return await ctx.message.add_reaction(dialogue_icon.dm), await ctx.author.send(Economy_Essential_Dialogue.reloadVAULT_success('vault[userID][\'reward\'][\'former_bon_toutou\'] = False'))

# !addcoins -- ADMIN ONLY. Take 2 args, a target userID and an amount.
    @commands.command()
    async def addcoins(self, ctx, amount : int, userID : discord.Member = None):
        # log the command
        print(Global_Log.command_has_been_used('addcoins', userID))
        # this prevent negative numbers to be added to an account
        amount = abs(amount)
        # check if author is getting his own informations or a user informations
        if userID == None:
            userID = ctx.author
        # call check_admin to check if user is allowed to perform this command
        if check_admin(ctx.author) is False:
            return await ctx.reply(Global_Dialogue.user_not_allowed('addcoins', userID))
        # call check_vault to check if user is registered
        if check_vault(userID) is False and userID == ctx.author:
            return await ctx.reply(Global_Dialogue.user_not_registered('addcoins'))
        elif check_vault(userID) is False:
            return await ctx.reply(Global_Dialogue.user_not_registered('addcoins', userID))

        md_balance(userID, "add", amount)
        if userID == ctx.author:
            return await ctx.reply(Economy_Essential_Dialogue.addcoins_success(amount))
        return await ctx.send(Economy_Essential_Dialogue.addcoins_success(amount, userID))                


# !balance OR !bal -- Take an optionnal arg: userID. Show the balance of the userID, 
# by default the author is the userID
    @commands.command(aliases=['bal'])
    async def balance(self, ctx, userID : discord.Member = None):
        # log the command
        print(Global_Log.command_has_been_used('balance', ctx.author))
        # check if author is getting his own informations or a user informations
        if userID == None:
            userID = ctx.author
        # call check_vault to check if user is registered
        if check_vault(userID) is False and userID == ctx.author:
            return await ctx.reply(Global_Dialogue.user_not_registered('balance'))
        elif check_vault(userID) is False:
            return await ctx.reply(Global_Dialogue.user_not_registered('balance', userID))
        
        # get_balance(userID)
        if userID == ctx.author:
            return await ctx.send(Economy_Essential_Dialogue.balance_success(get_balance(userID)))
        return await ctx.send(Economy_Essential_Dialogue.balance_success(get_balance(userID), userID))


# !balancetop OR !baltop -- Takes no args. Display all the accounts on the vault,
# ordered from richest to poorest (first to last).
    @commands.command(aliases=['baltop'])
    async def balancetop(self, ctx):
        # log the command
        print(Global_Log.command_has_been_used('balancetop', ctx.author))
        with open('./main/assets/vault.json') as vault:
            vault = json.load(vault)
            profiles = {}

            for profile in vault:
                bal = vault[profile]["balance"]
                profiles[profile] = bal
                baltop = sorted(profiles.items(), key=lambda x: x[1], reverse=True)

            await ctx.send(embed=Economy_Essential_Dialogue.balancetop_success(baltop))


# !pay -- Take 2 args, userID and amount. Transfer amount from the author balance to the userID balance.
    @commands.command()
    async def pay(self, ctx, userID : discord.Member, amount : int):
        # log the command
        print(Global_Log.command_has_been_used('pay', ctx.author))
        amount = abs(amount)
        
        if userID == ctx.author:
            return await ctx.reply(Economy_Essential_Dialogue.user_cant_pay_himself(ctx.author))

        if check_vault(ctx.author) is False:
            return await ctx.reply(Global_Dialogue.user_not_registered('pay'))

        if check_vault(userID) is False:
            return await ctx.reply(Global_Dialogue.user_not_registered('pay', userID))

        if check_pay(ctx.author, amount) is True:
            md_balance(ctx.author, "sub", amount)
            md_balance(userID, "add", amount)
            return await ctx.reply(Economy_Essential_Dialogue.pay_success(amount, userID))

        return await ctx.reply(Global_Dialogue.user_cant_pay('pay'))


#---------------------------------------------------------------------------------------#   ECONOMY ESSENTIALS ERRORS   #---------------------------------------------------------------------------------------#

# !addcoins error display
    @addcoins.error
    async def error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            print(Global_Log.command_has_been_used("addcoins", ctx.author))
            return await ctx.reply(Global_Dialogue.bad_arg('addcoins', ctx.author, '!addcoins <user> <amount>   --   <user> being an existing discord member and <amount> being a number.'))
        elif isinstance(error, commands.MissingRequiredArgument):
            print(Global_Log.command_has_been_used("addcoins", ctx.author))
            return await ctx.reply(Global_Dialogue.arg_missing('addcoins', ctx.author, '!addcoins <user> <amount>'))

# !balance error display
    @balance.error
    async def error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            print(Global_Log.command_has_been_used("balance", ctx.author))
            return await ctx.reply(Global_Dialogue.bad_arg('balance', ctx.author, '!balance <user>   --   <user> being an existing discord member.'))

# !pay error display
    @pay.error
    async def error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            print(Global_Log.command_has_been_used("pay", ctx.author))
            return await ctx.reply(Global_Dialogue.bad_arg('pay', ctx.author, '!pay <user> <amount>   --   <user> being an existing discord member and <amount> being a number.'))
        elif isinstance(error, commands.MissingRequiredArgument):
            print(Global_Log.command_has_been_used("pay", ctx.author))
            return await ctx.reply(Global_Dialogue.arg_missing('pay', ctx.author, '!pay <user> <amount>'))

#---------------------------------------------------------------------------------------#       ECONOMY GRIND       #---------------------------------------------------------------------------------------#

# Economy Grind will regroup all the commands related to grinding of {currency}.
class Economy_Grind(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f'\n{log_format.INFO}- Economy Grind from bank.py is loaded.{log_format.END}')

# display the help grind section
    async def help_grind(self,ctx):
        await ctx.author.send(Economy_Grind_Dialogue.help_grind_success(ctx.author))
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
                    return await ctx.author.send(Global_Dialogue.querry_exit('unknown_ID', 'grind help', ctx.author))
            # return if querry is not int
            except ValueError:
                return await ctx.author.send(Global_Dialogue.querry_exit('valueError_int', 'grind help', ctx.author))
            #return if querry successful
            return await ctx.author.send(Economy_Grind_Dialogue.help_grind_querry(int(querry.content), ctx.author))


# A 'bon toutou' is picked every 24 hours, it'll give the user perks like a 5% more income and 5% discounts...
    async def bon_toutou(self, userID: discord.Member):
        from cogs.essential import check_user_has_role
        from cogs.essential import check_user_is_bot
        from cogs.background_tasks import Bon_Toutou_Task
        guild = self.client.get_guild(774048252848111636)
        role_bon_toutou = guild.get_role(804849555094765598)
        role_hold_time = (60*60)*24

        if check_user_has_role(userID, 805897076437155861):
            print(Economy_Grind_Log.target_is_mauvais_toutou(userID))
            return await Bon_Toutou_Task.bon_toutou_assign(self)
        
        if check_user_is_bot(userID):
            print(Economy_Grind_Log.target_is_a_bot(userID))
            return await Bon_Toutou_Task.bon_toutou_assign(self)
        
        if check_vault(userID) is False:
            print(Economy_Grind_Log.target_is_not_registered(userID))
            return await Bon_Toutou_Task.bon_toutou_assign(self)
        
        if check_former_bon_toutou(userID):
            print(Economy_Grind_Log.target_is_former_bt(userID))
            return await Bon_Toutou_Task.bon_toutou_assign(self)

        md_bon_toutou_status(userID)
        await userID.send(Economy_Grind_Dialogue.bon_toutou_success(userID))
        await userID.add_roles(role_bon_toutou)

        await asyncio.sleep(role_hold_time)

        await userID.remove_roles(role_bon_toutou)



# !coinflip OR !cf -- Takes one arg. Amount. Expect an answer after first message.
# Either Head or Tail, a coin is tossed, if author wins, he double his bet. If author lose,
# he lose the double of his bet.
    @commands.command(aliases=['cf'])
    async def coinflip(self, ctx, amount : int):
        print(Global_Log.command_has_been_used('coinflip', ctx.author))
        from cogs.essential import check_user_has_role
        from cogs.essential import malus_rate
        from cogs.essential import bonus_rate

        amount = abs(amount)
        cf_prize = amount * 2
        coin_faces = ["head","tail"]

        if check_vault(ctx.author) is False:
            return await ctx.reply(Global_Dialogue.user_not_registered('coinflip'))

        if get_balance(ctx.author) < amount:
            return await ctx.reply(Global_Dialogue.user_cant_pay('coinflip'))
        
        # add malus rate to the prize if user is 'mauvais toutou'
        if check_user_has_role(ctx.author, 805897076437155861):
            cf_prize = cf_prize - cf_prize * malus_rate
            print(cf_prize)
        # add bonus rate to the prize if user is 'bon toutou'
        if check_user_has_role(ctx.author, 804849555094765598):
            cf_prize = cf_prize * bonus_rate
            print(cf_prize)

        await ctx.send(Economy_Grind_Dialogue.coinflip_success(amount, ctx.author, "cf_init"))
        print(Global_Log.bot_is_waiting_for_querry(ctx.author))

        def check(ans):
            return ans.channel == ctx.channel and ans.author == ctx.author

        ans = await self.client.wait_for('message', check=check)

        if ans.content.lower() != 'tail' and ans.content.lower() != 'head':
            return await ctx.reply(Economy_Grind_ErrorHandler.coinflip_error("fail_ans", ctx.author))

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
            md_balance(ctx.author, "sub", amount)
            return await ctx.send(Economy_Grind_Dialogue.coinflip_success(amount, ctx.author, "cf_lose"))
        
        md_balance(ctx.author, "add", cf_prize)
        return await ctx.send(Economy_Grind_Dialogue.coinflip_success(cf_prize, ctx.author, "cf_win"))


# # !facts OR !fa -- Takes no arg, but expect an answer. Send a fact to the context channel. 
# # First person to get the right answer to the fact will earn between 1 and 15 {currency}.
#     @commands.command(aliases=['fa'])
#     async def facts(self, ctx):
#         from cogs.essential import check_user_has_role
#         from cogs.essential import malus_rate
#         from cogs.essential import bonus_rate

#         client = discord.Client
#         channel = ctx.channel
#         random_fact = random.choice(fact_list)
#         fact_index = fact_list.index(random_fact)
#         prize = random.randint(1,15)

#         # add malus rate to the prize if user is 'mauvais toutou'
#         if check_user_has_role(ctx.author, 805897076437155861):
#             prize = prize - prize * malus_rate
#         # add bonus rate to the prize if user is 'bon toutou'
#         if check_user_has_role(ctx.author, 804849555094765598):
#             prize = prize * bonus_rate

#         await ctx.send(random_fact)

#         def check(ans):
#             return ans.content == answer_list[fact_index] and ans.channel == channel and ans.author != discord.Member.bot
        
#         if answer_list[fact_index] != "null":
#             answer = await client.wait_for(self.client, 'message', check=check, timeout=15)
            
#         if  check_vault(answer.author) != True:
#             return await answer.reply(facts_success("success_without_vault", prize))
            
#         md_balance(answer.author, "add", prize)
#         return await answer.reply(facts_success("success_with_vault", prize))

#---------------------------------------------------------------------------------------#   ECONOMY GRIND ERRORS   #---------------------------------------------------------------------------------------#

# !coinflip error display
    @coinflip.error
    async def error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            print(Global_Log.command_has_been_used('coinflip', ctx.author))
            await ctx.reply(Global_Dialogue.bad_arg('coinflip', ctx.author, '!coinflip <amount>   --   <amount> being a number!'))
        elif isinstance(error, commands.MissingRequiredArgument):
            print(Global_Log.command_has_been_used('coinflip', ctx.author))
            await ctx.reply(Global_Dialogue.arg_missing('coinflip', ctx.author, '!coinflip <amount>'))

#---------------------------------------------------------------------------------------#       ECONOMY REWARDS       #---------------------------------------------------------------------------------------#

class Economy_Reward(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f"\n{log_format.INFO}- Economy Rewards from bank.py is loaded.{log_format.END}")

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
                return Economy_Grind_Dialogue.daily_reward_success(userID, reward, "first_claim")

            if dlr_claim < date_now:
                vault[userID]["reward"]["daily_reward_claim_date"] = date_now
                vault[userID]["balance"] += reward
                edit_vault(vault)
                return Economy_Grind_Dialogue.daily_reward_success(userID, reward, "claim_success")

            return Economy_Grind_Dialogue.daily_reward_success(userID, reward)

#
    def passive_inc_reward(self, ctx):
        return

#---------------------------------------------------------------------------------------#       ECONOMY REWARDS COMMANDS      #---------------------------------------------------------------------------------------#

# !claim -- Takes an optionnal arg. Without arg, display the list of available rewards.
# With a reward name as a an arg, claim the specified reward if available.
    @commands.command()
    async def claim(self, ctx, reward_type : str = None):
        print(Global_Log.command_has_been_used('claim', ctx.author))
        
        if check_vault(ctx.author) == False:
            return await ctx.reply(Global_Dialogue.user_not_registered('claim'))
        
        # if reward_type == None:
        #     return await ctx.reply(claim_success())

        if reward_type == "daily":
            return await ctx.reply(self.daily_reward(ctx, ctx.author))
        
        # if reward_type == "":
        #     return self.passive_inc_reward(ctx)


#---------------------------------------------------------------------------------------#   ECONOMY REWARDS ERRORS   #---------------------------------------------------------------------------------------#



#---------------------------------------------------------------------------------------#       COGS SETUP      #---------------------------------------------------------------------------------------#

def setup(client):
    client.add_cog(Economy_Essentials(client))
    client.add_cog(Economy_Grind(client))
    client.add_cog(Economy_Reward(client))