import discord
import json
from dialogue.global_dialogue import *

class Essential_Dialogue:
    # help command
    def help_command_success(userID: discord.Member):
        with open('main/assets/help.json') as help_index:
            help_index = json.load(help_index)
            index_list = list(help_index)
            preformat_index_list = []
            for theme in index_list:
                preformat_index_list.append(
                    f'\n> ` {index_list.index(theme)} `   :white_small_square:   **{theme}**'
                    )
            display_help_index = f'\n> '.join([i for i in preformat_index_list])

        print(Global_Log.command_has_been_used('help', userID),'\n',Global_Log.command_run_without_exception('help'))
        return (
            f':dividers:    **WELCOME TO THE HELP INDEX!**    :dividers:'
            f'\n\n> **Reply to this message with the number associated to the theme to get more informations about it!**'
            f'\n> **If there is a theme that is not referenced and you have a unanswered question, please contact an administrator.**'
            f'\n> '
            f'{display_help_index}'
            )

    # help_general function
    def help_general_function_success(userID: discord.Member):
        with open('main/assets/help.json') as help_index:
            help_general = json.load(help_index)
            help_general = help_general["General"]
            help_general_list = list(help_general)
            preformat_display_theme = []
            for theme in help_general:
                preformat_display_theme.append(
                    f'\n> ` {help_general_list.index(theme)} `   :white_small_square:   **{theme}**'
                    )
            display_help_general = f'\n> '.join([i for i in preformat_display_theme])
        
        print(Global_Log.querry_success('general help', userID))
        return (
            f':globe_with_meridians:    **WELCOME TO THE GENERAL HELP SECTION!**    :globe_with_meridians:'
            f'\n\n> **Reply to this message with the number associated to the theme to get more informations about it!**'
            f'\n> **If there is a theme that is not referenced and you have a unanswered question, please contact an administrator.**'
            f'\n> '
            f'{display_help_general}'
        )
    # help_general_querry function
    def help_general_querry(query : int, userID: discord.Member):
        with open('main/assets/help.json') as help_index:
            help_general = json.load(help_index)
            help_general = help_general["General"]
            help_general_list = list(help_general)
            help_general_exp_list = list(help_general.values())
            theme_index = query
       
        print(Global_Log.querry_success('general help', userID))
        return (
            f'> :question:    {help_general_list[theme_index]}'
            f'\n> '
            f'\n> :speech_left:    {help_general_exp_list[theme_index]}'
            )
