import discord
import json
from dialogue.global_dialogue import *

class Essential_Dialogue:
    # help command
    def help_command_success(userID: discord.Member):
        with open('main/assets/help.json') as help_index:
            help_index = json.load(help_index)
            index_list = list(help_index)
            
            embed = discord.Embed(
                title= ":dividers:   WELCOME TO THE HELP INDEX   :dividers:",
                description=(
                    f"Reply to this message with the index of the theme to get more informations about it!"
                    f"\nIf there is a theme that is not referenced and you have a unanswered question, please contact an administrator."
                ),
                color= discord.Colour.random()
            )
            
            for theme in index_list:
                embed.add_field(name=f"{theme}", value=f":id:   **{index_list.index(theme)}**", inline=False)

        print(Global_Log.command_has_been_used('help', userID),'\n',Global_Log.command_run_without_exception('help'))
        
        return embed

    # help_general function
    def help_general_function_success(userID: discord.Member):
        with open('main/assets/help.json') as help_index:
            help_general = json.load(help_index)
            help_general = help_general["General"]
            help_general_list = list(help_general)
            
            embed = discord.Embed(
                title= f":globe_with_meridians:    WELCOME TO THE GENERAL HELP SECTION    :globe_with_meridians:",
                description=(
                    f"Reply to this message with the index of the theme to get more informations about it!"
                    f"\nIf there is a theme that is not referenced and you have a unanswered question, please contact an administrator."
                ),
                color= discord.Colour.random()
            )

            for theme in help_general:
                embed.add_field(name=f"{theme}", value=f":id:   **{help_general_list.index(theme)}**", inline=False)

        print(Global_Log.querry_success('general help', userID))
        return embed

    # help_general_querry function
    def help_general_querry(query : int, userID: discord.Member):
        # create embed
        embed = discord.Embed(
            title= ":globe_with_meridians:   GENERAL   :globe_with_meridians:",
            color = discord.Colour.random()
                )
        # load data
        with open('main/assets/help.json') as help_index:
            help_general = json.load(help_index)
            help_general = help_general["General"]
            help_general_list = list(help_general)
            help_general_exp_list = list(help_general.values())
            # embed field value
            default_embed_value = f"{help_general_exp_list[query]}"
            
            # if theme is a list, unroll and add to embed field value.
            if help_general_list[query].startswith("List"):
                # create two temp list
                command_list = []
                command_list_perm = []
                # unroll the list
                for command in help_general_exp_list[query]:
                    com = help_general_exp_list[query][command]
                    # if command doesn't need perm it goes through this statement
                    if com['permission'] == "NONE":
                        command_list.append(
                            f"\n> **{command}**"
                            f"\n> Use with `{com['syntax']}`"
                            f"\n> Parameter required: `{com['parameters']}`"
                            f"\n> Permissions required: `{com['permission']}`"
                            f"\n> ***{com['desc']}***"
                        )
                    else:
                        command_list_perm.append(
                            f"\n> **{command}**"
                            f"\n> Use with `{com['syntax']}`"
                            f"\n> Parameter required: `{com['parameters']}`"
                            f"\n> Permissions required: `{com['permission']}`"
                            f"\n> ***{com['desc']}***"
                        )
                # embed values
                embed_value_perm = ("\n----------------------".join([i for i in command_list_perm]))        
                embed_value = ("\n----------------------".join([i for i in command_list]))

                # check that no empty value is passed & add embed values
                if len(command_list_perm) > 0:
                    embed.add_field(
                        name=
                        f"\nCommands below requires certain permissions to be used.", 
                        value=embed_value_perm, 
                        inline=False)
                
                embed.add_field(
                    name=
                    f"\n----------------------"
                    f"\n"
                    f"\n{help_general_list[query]}"
                    f"\n"
                    f"\n----------------------",
                    value=embed_value, 
                    inline=False)
            else:
                # if no list to unroll, return default embed.
                embed.add_field(name=f"{help_general_list[query]}", value=default_embed_value, inline=False)
        # log
        print(Global_Log.querry_success('general help', userID))
        return embed