import discord
import json
from dialogue.global_dialogue import *

class Economy_Essential_Dialogue:
    # help_economy function
    def help_economy_function_success(userID: discord.Member):
        with open('main/assets/help.json') as help_index:
            help_economy = json.load(help_index)
            help_economy = help_economy["Economy"]
            help_economy_list = list(help_economy)
            preformat_display_theme = []
            for theme in help_economy:
                preformat_display_theme.append(
                    f'\n> ` {help_economy_list.index(theme)} `   :white_small_square:   **{theme}**'
                    )
            display_help_economy = f'\n> '.join([i for i in preformat_display_theme])

        print(Global_Log.querry_success('economy help', userID))
        return (
            f':bank:    **WELCOME TO THE ECONOMY HELP SECTION!**    :bank:'
            f'\n\n> **Reply to this message with the number associated to the theme to get more informations about it!**'
            f'\n> **If there is a theme that is not referenced and you have a unanswered question, please contact an administrator.**'
            f'\n> '
            f'{display_help_economy}'
        )
    # help_economy_querry function
    def help_economy_querry(querry : int, userID: discord.Member):
        with open('main/assets/help.json') as help_index:
            help_economy = json.load(help_index)
            help_economy = help_economy["Economy"]
            help_economy_list = list(help_economy)
            help_economy_exp_list = list(help_economy.values())
            theme_index = querry
        
        print(Global_Log.querry_success('economy help', userID))
        return (
            f'> :question:    {help_economy_list[theme_index]}'
            f'\n> '
            f'\n> :speech_left:    {help_economy_exp_list[theme_index]}'
            )
    # register command 
    def register_success(userID : discord.Member = None):
        if userID == None:
            return (
                f':ballot_box_with_check:   YES PAPAAAA!   :zany_face::zany_face:'
                f'\n> You have been successfully registered.'
                f'\n> You can now earn {global_dialogue_var.currency}!   :money_with_wings:'
                f'\n> *You can access all the commands related to the economy with* ` !help economy `'
                )
        return (
            f':ballot_box_with_check:   YES PAPAAAA!   :zany_face::zany_face:'
            f'\n> {userID} Has been successfully registered!'
        )

class Economy_Grind_Dialogue:
    # help_grind function
    def help_grind_success(userID: discord.Member):
        with open('main/assets/help.json') as help_index:
            help_grind = json.load(help_index)
            help_grind = help_grind["Grind"]
            help_grind_list = list(help_grind)
            preformat_display_theme = []
            for theme in help_grind:
                preformat_display_theme.append(
                    f'\n> ` {help_grind_list.index(theme)} `   :white_small_square:   **{theme}**'
                    )
            display_help_grind = f'\n> '.join([i for i in preformat_display_theme])
        
        print(Global_Log.querry_success('grind help', userID))
        return (
            f':money_mouth:    **WELCOME TO THE GRIND HELP SECTION!**    :money_mouth:'
            f'\n\n> **Reply to this message with the number associated to the theme to get more informations about it!**'
            f'\n> **If there is a theme that is not referenced and you have a unanswered question, please contact an administrator.**'
            f'\n> '
            f'{display_help_grind}'
        )
    # help_grind_querry function
    def help_grind_querry(querry : int, userID: discord.Member):
        with open('main/assets/help.json') as help_index:
            help_grind = json.load(help_index)
            help_grind = help_grind["Grind"]
            help_grind_list = list(help_grind)
            help_grind_exp_list = list(help_grind.values())
            theme_index = querry
        print(Global_Log.querry_success('grind help', userID))
        return (
            f'> :question:    {help_grind_list[theme_index]}'
            f'\n> '
            f'\n> :speech_left:    {help_grind_exp_list[theme_index]}'
            ) 