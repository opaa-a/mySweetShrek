import discord
import json
from dialogue.global_dialogue import *

class Store_Dialogue:
    # FUNCTION
    # help_store function
    def help_store_success(userID: discord.Member):
        with open('main/assets/help.json') as help_index:
            help_store = json.load(help_index)
            help_store = help_store["Store"]
            help_store_list = list(help_store)
            preformat_display_theme = []
            for theme in help_store:
                preformat_display_theme.append(
                    f'\n> ` {help_store_list.index(theme)} `   :white_small_square:   **{theme}**'
                    )
            display_help_store = f'\n> '.join([i for i in preformat_display_theme])
        
        print(Global_Log.querry_success('store help', userID))
        return (
            f':department_store:    **WELCOME TO THE {global_dialogue_var.storeName.upper()} HELP SECTION!**    :department_store:'
            f'\n\n> **Reply to this message with the number associated to the them to get more informations about it!**'
            f'\n> **If there is a theme that is not referenced and you have a unanswered question, please contact an administrator.**'
            f'\n> '
            f'{display_help_store}'
            )
    # help_store_querry function
    def help_store_querry(query : int, userID: discord.Member):
        with open('main/assets/help.json') as help_index:
            help_store = json.load(help_index)
            help_store = help_store["Store"]
            help_store_list = list(help_store)
            help_store_exp_list = list(help_store.values())
            theme_index = query
        
        print(Global_Log.querry_success('store help', userID))
        return (
            f'> :question:    {help_store_list[theme_index]}'
            f'\n> '
            f'\n> :speech_left:    {help_store_exp_list[theme_index]}'
            )  
    # store_purchase function
    def store_purchase_complete(item_name : str):
        print(Global_Log.command_run_without_exception('store buy'))
        return (
            f':package:   **You successfully purchased {item_name}**   :package:'
            f'\n> *Your item has been placed in your inventory.*'
            f'\n> *Learn more about the inventory in with the* ` !help ` *command.*'
            )
    # COMMAND
    # store showcase command
    def store_showcase_success():
        print(Global_Log.command_run_without_exception('store showcase'))
        with open('main/assets/store_inv.json') as store_inv:
            store_inv = json.load(store_inv)
            preformat_store_inv = []
            for item in store_inv:
                preformat_store_inv.append(
                    f'\n> {store_inv[item]["icon"]} ` {item} `   :   **{store_inv[item]["price"]} {global_dialogue_var.currency} :coin:**'
                    f'\n>   *{store_inv[item]["desc"]}*'
                    ) 
            store_inv_showcase = f'\n> '.join([i for i in preformat_store_inv])
        return (
            f':shopping_bags:   **WELCOME TO THE {global_dialogue_var.storeName.upper()}!**   :shopping_bags:'
            f'\n\n> **Here are displayed all the currently available-to-purchase commands!**'
            f'\n> '
            f'{store_inv_showcase}'
            )
    # store buy command
    def store_buy_success():
        return(
            f':shopping_bags:   **WELCOME TO THE {global_dialogue_var.storeName.upper()}!**   :shopping_bags:'
            f'\n\n> **Reply to this message with the name of the item you want to purchase**'
            f'\n> **To get the list of all the items in the store ` !store showcase `**'
            )

class Store_ErrorHandler:
    def error_store(error_type: str):
        print(f'\t{log_format.FAIL} COMMAND store FAILED - USER DID NOT PASS A VALID PARAMETER')
        if error_type == "bad_arg":
            return (
                f'{dialogue_icon.fail}   Oops! The parameter of store you specified doesn\'t exist.'
                f'\n:arrow_right: `!store help`'
                )