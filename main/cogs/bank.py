import discord
import json
from discord.ext import commands

class Economy(commands.Cog):        # REGROUPS EVERY COMMANDS THAT ARE RELATED TO THE ECONOMY SYSTEM
    
    global currency                 # DEFINE THE NAME OF THE SERVER CURRENCY
    currency = "pipi-coins"

    def __init__(self, client):
        self.client = client
        print(f"\n- Economy from bank is loaded.")

    def vault_profile(user):        # FUNCTION TO LOOK IN THE VAULT FOR PROFILES
        with open('vault.json', 'r') as vault:
            vault = json.load(vault)
            
            user = str(userID)
            global vault_profile

            for vault_profile in vault['profile']:
                profile_id = str(vault_profile['userID'])
                
                if user == profile_id:
                    print('\nuserID found')
                    return(vault_profile)
                
                else:
                    print('\nno userID found')


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



def setup(client):
    client.add_cog(Economy(client))