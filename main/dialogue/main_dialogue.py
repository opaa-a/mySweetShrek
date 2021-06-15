import discord
from main_rev3_0 import log_format, dialogue_icon

class Main_Dialogue:
    # load
    def load_command_success(cog: str):
        return f'{dialogue_icon.success}   You successfully loaded **{cog}**!'
    def load_command_fail(cog: str):
        return f'{dialogue_icon.fail}   Ohoh'

class Main_Log:
    # init_cog
    init_cog_success = f'\n{log_format.INFO} FUNCTION [init_cog] has been executed successfully.{log_format.END}'
    init_cog_empty_cogs = f'\n{log_format.FAIL} FUNCTION  init_cog  FROM  main.py  had no cogs to load{log_format.END}'
    # load
    load = f'\n{log_format.INFO}'