import discord
import json
from decouple import config
from discord.ext import commands

ADMIN_ROLE_ID = config('DISCORD_ADMIN_ROLE_ID') # DISCORD ADMIN ROLE IDENTIFIER


class Economy(commands.Cog):        # REGROUPS EVERY COMMANDS THAT ARE RELATED TO THE ECONOMY SYSTEM
    def __init__(self, client):
        self.client = client
        print(f"\n- Economy from bank is loaded.")

    global currency                 # DEFINE THE NAME OF THE SERVER CURRENCY
    currency = "pipi-coins"

    def vault_profile(self, user : discord.Member):        # FUNCTION TO LOOK IN THE VAULT FOR PROFILES
        with open('vault.json', 'r') as vault:
            vault = json.load(vault)
            user = str(user)
            global user_has_vault
            user_has_vault = False

            for vault_profile in vault['profile']:
                profile_id = str(vault_profile['userID'])
                if user == profile_id:
                    print('\nuserID found')
                    user_has_vault = True
                    return user_has_vault
                else:
                    print('\nno userID found')

    def check_admin(self, user : discord.Member):
        aID = int(ADMIN_ROLE_ID)
        userRoles = []
        global user_is_admin
        user_is_admin = False

        for role in user.roles:
            userRoles.append(role.id)
        if aID in userRoles:
            user_is_admin = True
            return user_is_admin

    @commands.command()             # !register -- REGISTER YOUR CURRENCY ACCOUNT
    async def register(self, ctx):
       
        def edit_vault(data, filename='vault.json'):
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
        
        author = str(ctx.author)

        with open('vault.json') as vault:
            vault = json.load(vault)
            registery = []
            
            for profile in vault['profile']:
                registery.append(profile['userID'])
                
            if  author in registery:
                await ctx.reply(f':x:   Oh Oh! Looks like you are already registered!')

            else:
                new_profile = {"userID": str(author), "balance": 0}
                vault['profile'].append(new_profile)
                await ctx.reply(
                    f'YES PAPAAAA!   :zany_face::zany_face:' 
                    f'\nYour account has been created,' 
                    f'\n:money_with_wings:   you can now earn {currency}!   :money_with_wings:'
                    )
        
        edit_vault(vault)

    @commands.command(aliases=['t'])
    async def coins_add(self, ctx, user : discord.Member, amount : int):
        self.check_admin(ctx.author)
        self.vault_profile(user)

        if user_is_admin == True and user_has_vault == True:
            await ctx.send(f'{amount} {currency} have been added to {user} vault.')



def setup(client):
    client.add_cog(Economy(client))