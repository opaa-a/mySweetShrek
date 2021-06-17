import discord
from dialogue.global_dialogue import Global_Log, log_format, dialogue_icon

class Main_Dialogue:
    # load command
    def load_command_success(cog: str, userID: discord.Member):
        print(Global_Log.command_has_been_used('load', userID),'\n\t',Global_Log.command_run_without_exception('load'))
        return f'{dialogue_icon.success}   You successfully loaded **{cog}**!'
    
    # unload command
    def unload_command_success(cog: str, userID: discord.Member):
        print(Global_Log.command_has_been_used('unload', userID),'\n\t',Global_Log.command_run_without_exception('unload'))
        return f'{dialogue_icon.success}   You successfully unloaded **{cog}**!'
    
    # reload command
    def reload_command_success(cog: str, userID: discord.Member):
        print(Global_Log.command_has_been_used('reload', userID),'\n\t',Global_Log.command_run_without_exception('reload'))
        return f'{dialogue_icon.success}   You successfully reloaded **{cog}**!'

    # coglist command
    def cl_command_success(userID: discord.Member):
        return print(Global_Log.command_has_been_used('coglist', userID), '\n\t',Global_Log.command_run_without_exception('coglist'))

class Main_Log:
    # init_cog function
    init_cog_success = f'\n{log_format.INFO} FUNCTION init_cog has been executed successfully.{log_format.END}'
    init_cog_empty_cogs = f'\n{log_format.FAIL} FUNCTION  init_cog  FROM  main.py  had no cogs to load.{log_format.END}'


class Main_ErrorHandler:
    # --------------------- # load command # --------------------- #
    def load_error_cog_already_loaded(cog: str, userID: discord.Member):
        print(Global_Log.command_has_been_used('load', userID),'\n\t',f'{log_format.FAIL} {cog} WAS NOT LOADED DUE TO IT BEING ALREADY LOADED.{log_format.END}')
        return f'{dialogue_icon.fail}   Oops! You can\'t load **{cog}** since it is already loaded!'
    
    def load_error_cog_doesnt_exist(cog: str, userID: discord.Member):
        print(Global_Log.command_has_been_used('load', userID),'\n\t',f'{log_format.FAIL} {cog} COG IS NOT RECOGNIZED THEREFORE LOAD COMMAND FAILED TO EXECUTE.{log_format.END}')
        return f'{dialogue_icon.fail}   Ohoh! Looks like the cog you specified **{cog}** does not exist.'
    
    # --------------------- # unload command # --------------------- #
    def unload_error_cog_already_unloaded(cog: str, userID: discord.Member):
        print(Global_Log.command_has_been_used('unload', userID),'\n\t',f'{log_format.FAIL} {cog} WAS NOT UNLOADED DUE TO IT BEING ALREADY UNLOADED.{log_format.END}')
        return f'{dialogue_icon.fail}   Oops! You can\'t unload **{cog}** since it is already unloaded!'

    def unload_error_cog_doesnt_exist(cog: str, userID: discord.Member):
        print(Global_Log.command_has_been_used('unload', userID),'\n\t',f'{log_format.FAIL} {cog} COG IS NOT RECOGNIZED THEREFORE UNLOAD COMMAND FAILED TO EXECUTE.{log_format.END}')
        return f'{dialogue_icon.fail}   Ohoh! Looks like the cog you specified **{cog}** does not exist.'

    # --------------------- # reload command # --------------------- #
    def reload_error_cog_is_unloaded(cog: str, userID: discord.Member):
        print(Global_Log.command_has_been_used('reload', userID),'\n\t',f'{log_format.FAIL} {cog} WAS NOT RELOADED DUE TO IT BEING UNLOADED.{log_format.END}')
        return f'{dialogue_icon.fail}   Oops! You can\'t reload **{cog}** since it is unloaded!'

    def reload_error_cog_doesnt_exist(cog: str, userID: discord.Member):
        print(Global_Log.command_has_been_used('reload', userID),'\n\t',f'{log_format.FAIL} {cog} COG IS NOT RECOGNIZED THEREFORE RELOAD COMMAND FAILED TO EXECUTE.{log_format.END}')
        return f'{dialogue_icon.fail}   Ohoh! Looks like the cog you specified **{cog}** does not exist.'