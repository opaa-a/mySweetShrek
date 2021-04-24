import discord
import json
import random
from decouple import config
from discord.ext import commands
from facts_dic import *

ADMIN_ROLE_ID = config('DISCORD_ADMIN_ROLE_ID') # DISCORD ADMIN ROLE IDENTIFIER


class Economy(commands.Cog):        # REGROUPS EVERY COMMANDS THAT ARE RELATED TO THE ECONOMY SYSTEM
    def __init__(self, client):
        self.client = client
        print(f"\n- Economy from bank is loaded.")

    global currency                 # DEFINE THE NAME OF THE SERVER CURRENCY
    currency = "pipi-coins"


    def vault_profile(self, userID : discord.Member):        # FUNCTION TO LOOK IN THE VAULT FOR PROFILES
        with open('vault.json', 'r') as vault:
            vault = json.load(vault)
            userID = str(userID)
            global user_has_vault
            user_has_vault = False

            for profile in vault:
                if userID == profile:
                    #print('\nuserID found')
                    user_has_vault = True
                    return user_has_vault
                else:
                    #print('\nno userID found')
                    pass


    def check_admin(self, userID : discord.Member):          # FUNCTION TO CHECK IF SPECIFIED USER IS ADMIN
        aID = int(ADMIN_ROLE_ID)
        userRoles = []
        global user_is_admin
        user_is_admin = False

        for role in userID.roles:
            userRoles.append(role.id)
        if aID in userRoles:
            user_is_admin = True
            return user_is_admin


    def md_balance(self, userID : discord.Member, md_method : str, amount : int):      # ADD, SUBSTRACT OR RESET COINS FROM A SPECIFIED USER ACCOUNT
        # md_method are : <add> <sub> <reset>
       
        def edit_vault(data, filename='vault.json'):
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
                
        with open('vault.json') as vault:
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

    def get_balance(self, userID):
        with open('vault.json') as vault:
            vault = json.load(vault)
            userID = str(userID)

            global balance
            balance = 0

            for profile in vault:
                if profile == userID:
                    balance = vault[userID]["balance"]
                    return balance


    @commands.command()             # !register -- REGISTER YOUR CURRENCY ACCOUNT
    async def register(self, ctx):
       
        def edit_vault(data, filename='vault.json'):
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
        
        author = str(ctx.author)

        with open('vault.json') as vault:
            vault = json.load(vault)
            registery = []

            for profile in vault:
                registery.append(profile)
                
            if  author in registery:
                await ctx.reply(f':x:   Oh Oh! Looks like you are already registered!')

            else:
                vault[author] = {"balance": 0}
                await ctx.reply(
                    f'YES PAPAAAA!   :zany_face::zany_face:' 
                    f'\nYour account has been created,' 
                    f'\n:money_with_wings:   you can now earn {currency}!   :money_with_wings:'
                    )
        
        edit_vault(vault)


    @commands.command()
    async def add_coins(self, ctx, userID : discord.Member, amount : int):    # !add_coins <userID> <amount> -- ADD AMOUT OF COINS TO SPECIFIED USER
        self.check_admin(ctx.author)
        self.vault_profile(userID)

        if user_is_admin == True and user_has_vault == True:
            
            self.md_balance(userID, "add", amount)
            
            await ctx.send(
                f'YES PAPAAAA!   :zany_face::zany_face:' 
                f'\n{amount} {currency} have been added to {userID}\'s vault.'
                f'\n:money_with_wings::money_with_wings::money_with_wings:'
                )
        elif user_has_vault is not True:
            await ctx.reply(f':x:   {userID} has not registered an account yet!')
        elif user_is_admin is not True:
            await ctx.reply(f':x:   Oh Oh! Looks like you are not allowed to perform this command.')

    @add_coins.error
    async def error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            print('\nERROR -- add_coins -- BAD ARGUMENT')
            await ctx.reply(f':x:   Oops! Looks like one or multiple arguments given are not valid!')
        elif isinstance(error, commands.MissingRequiredArgument):
            print('\nERROR -- add_coins -- MISSING ARGUMENT')
            await ctx.reply(
                f':x:   Oops! You need to provide the user and the amount!'
                f'\n- !add_coins <user> <amount>'
                )


    @commands.command(aliases=['bal'])
    async def balance(self, ctx, userID : discord.Member=None):     # !balance OR !bal -- GIVE THE BALANCE OF A USER VAULT
        if userID == None:
            userID = ctx.author
        
        self.vault_profile(userID)
        
        if user_has_vault == True:
            self.get_balance(userID)

            if balance <= 500:
                await ctx.send(
                    f'{userID} has **{balance}** {currency} in the vault!'
                    f'\n\nAbout to be homeless with that kind of money. :100::money_with_wings:'
                    )
            elif balance >= 500 and balance <= 5000:
                await ctx.send(
                    f'{userID} has **{balance}** {currency} in the vault!'
                    f'\n\nBet you can\'t even buy a yatch :100::money_with_wings::money_with_wings:'
                    )
            elif balance >= 5000 and balance <= 10000:
                await ctx.send(
                    f'{userID} has **{balance}** {currency} in the vault!'
                    f'\n\nWell, I guess you are not that far from the yatch... :100::money_with_wings::money_with_wings::money_with_wings:'
                    )
            elif balance >= 10000 and balance <= 100000:
                await ctx.send(
                    f'{userID} has **{balance}** {currency} in the vault!'
                    f'\n\nFuckin\' hell, give me some bro :100::money_with_wings::money_with_wings::money_with_wings::moneybag::moneybag:'
                    )
            elif balance >= 100000:
                await ctx.send(
                    f'{userID} has **{balance}** {currency} in the vault!'
                    f'\n\nFuck off, you can\'t have that much...'
                    f'\n:money_with_wings::moneybag::money_with_wings::moneybag::money_with_wings::moneybag:'
                    )
        else:
            await ctx.reply(f':x:   Oh Oh! Looks like {userID} is not registered in the vault yet!')

    @balance.error
    async def error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            print('\nERROR -- balance -- BAD ARGUMENT')
            await ctx.reply(f':x:   Oops! Looks like the user specified don\'t exist :pensive:')


    @commands.command(aliases=['fa'])
    async def facts(self, ctx):

        client = discord.Client
        channel = ctx.channel
        random_fact = random.choice(fact_list)
        fact_index = fact_list.index(random_fact)
        prize = random.randint(1,15)

        await ctx.send(random_fact)

        def check(ans):
            if ans.content == answer_list[fact_index] and ans.channel == channel:
                return ans.content, ans.channel
        
        if answer_list[fact_index] is not "null":
            answer = await client.wait_for(self.client, 'message', check=check, timeout=15)
            self.vault_profile(answer.author)            
            
            if  user_has_vault == True:
                self.md_balance(answer.author, "add", prize)
                await answer.reply(
                    f'Got it! :joy::ok_hand:'
                    f'\n*You earned {prize} {currency}!*'
                    )
            else:
                await answer.reply(
                    f'Got it! :joy::ok_hand:'
                    f'\n*You won nothing cuz you ain\'t registered, you fucking nerd.*'
                )
        
        else:
            print('\n!facts ; break ; no answer needed.')


    @commands.command(aliases=['baltop'])
    async def balancetop(self, ctx):
        
        def get_bal(d, profile):
            return d.get(profile)
        
        with open('vault.json') as vault:
            vault = json.load(vault)
            d = {}

            for profile in vault:
                pb = vault[profile]["balance"]
                d[profile] = int(pb)





def setup(client):
    client.add_cog(Economy(client))