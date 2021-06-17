import discord
import json
from dialogue.global_dialogue import *

class Store_Dialogue:
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
    def help_store_querry(querry : int, userID: discord.Member):
        with open('main/assets/help.json') as help_index:
            help_store = json.load(help_index)
            help_store = help_store["Store"]
            help_store_list = list(help_store)
            help_store_exp_list = list(help_store.values())
            theme_index = querry
        
        print(Global_Log.querry_success('store help', userID))
        return (
            f'> :question:    {help_store_list[theme_index]}'
            f'\n> '
            f'\n> :speech_left:    {help_store_exp_list[theme_index]}'
            )  