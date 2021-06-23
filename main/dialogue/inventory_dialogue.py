import discord
import json
from dialogue.global_dialogue import *

class Inventory_Dialogue:
    # FUNCTIONS
    # help_inv function 
    def help_inv_success(userID: discord.Member):
        with open('main/assets/help.json') as help_index:
            help_inv = json.load(help_index)
            help_inv = help_inv["Inventory"]
            help_inv_list = list(help_inv)

            embed = discord.Embed(
                title= f":package:    WELCOME TO THE INVENTORY HELP SECTION    :package:",
                description=(
                    f"Reply to this message with the index of the theme to get more informations about it!"
                    f"\nIf there is a theme that is not referenced and you have a unanswered question, please contact an administrator."
                ),
                color= discord.Colour.random()
            )
            for theme in help_inv:
                embed.add_field(name=f"{theme}", value=f":id:   **{help_inv_list.index(theme)}**", inline=False)

        print(Global_Log.querry_success('inventory help', userID))
        return embed

    # help_inv_querry function
    def help_inv_querry(query : int, userID: discord.Member):
        with open('main/assets/help.json') as help_index:
            help_inv = json.load(help_index)
            help_inv = help_inv["Inventory"]
            help_inv_list = list(help_inv)
            help_inv_exp_list = list(help_inv.values())
        
        embed = discord.Embed(
           title= ":dividers:   HELP INDEX   :dividers:",
           color = discord.Colour.random()
            )
        embed.add_field(name=f":question: {help_inv_list[query]}", value=f"{help_inv_exp_list[query]}", inline=False)

        print(Global_Log.querry_success('inventory help', userID))
        return embed

    # discplay_inv function
    def display_inv_success(inventory):
        print(Global_Log.command_run_without_exception('inventory'))
        with open('main/assets/store_inv.json') as store_inv:
            store_inv = json.load(store_inv)
            
            if inventory == {}:
                embed = discord.Embed(
                    title=":package:   THIS IS YOUR INVENTORY   :package:",
                    description=(
                        f""
                        f":wind_blowing_face::leaves::wind_blowing_face:"
                        f"Ohoh! Looks like your inventory is empty!"
                    )
                )
                return embed
            
            embed = discord.Embed(
                title= ":package:   THIS IS YOUR INVENTORY   :package:",
                color= discord.Colour.random()
            )
            for item in inventory:
                icon = store_inv[item]['icon']
                desc = store_inv[item]['desc']
                amount = inventory[item]
                embed.add_field(name=f"**{icon} ` {item} ` x ` {amount} `**", value=f"*{desc}*", inline=False)
        return embed

    # COMMANDS
    # use command
    def use_success(dialogue_ref: str, target: discord.Member, item, author = None):
        # return if author don't have the item
        if dialogue_ref == "item_missing":
            print(f'\t{log_format.FAIL} COMMAND use FAILED - DUE TO THE FOLLOWING ERROR: {dialogue_ref}.{log_format.END}')
            return (
                f'{dialogue_icon.fail}   Nope, you can\'t use what you don\'t own.'
                f'\n:arrow_right:   You can buy items with the command: `!store buy`'
            )
            
        if dialogue_ref == "item_used":
            author = str(author)
            # get icons of items
            with open('main/assets/store_inv.json') as store_inv:
                store_inv = json.load(store_inv)
                icon = store_inv[item]['icon']
            # get author inv
            with open('main/assets/vault.json') as vault:
                vault = json.load(vault)
                item_amount = int(vault[author]['inventory'][item])
            
            print(Global_Log.command_run_without_exception('use'))
            return (
                f'{icon}   **You successfully used {item} on {target}!**'
                f'\n:package: You now have ` {item_amount} ` **x** ` {item} ` in your inventory.'
                )
class Inventory_Log:
    # FUNCTION
    # add_inventory & remove_inventory functions
    def md_inv_log(userID: discord.Member, method: str, item: str, amount: int):
        if method == 'add':
            return f'\t{log_format.NOEXC} add_item_to_inv HAS BEEN SUCCESSFULLY USED FOR {userID} WITH THE ITEM {item} FOR THIS AMOUNT: {amount}.{log_format.END}'
        if method == 'rm':
            return f'\t{log_format.NOEXC} remove_item_to_inv HAS BEEN SUCCESSFULLY USED FOR {userID} WITH THE ITEM {item} FOR THIS AMOUNT: {amount}.{log_format.END}'
