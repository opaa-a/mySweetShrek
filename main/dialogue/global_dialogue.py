import discord
from main_rev3_0 import dialogue_icon
from main_rev3_0 import log_format

class Global_Dialogue:
    # return if user is not allowed to perform a command
    def user_not_allowed(userID: discord.Member = None):
        if userID == None:
            return f'{dialogue_icon.fail}   Ohoh! Looks like you are not allowed to perform this command.'

class Global_Log:
    # log if user is not allowed to perform a command
    def user_not_allowed(command: str, userID: discord.Member):
        return f'{log_format.FAIL} COMMAND {command} FAILED - USER {userID} TRIED TO PERFORM THIS COMMAND WITHOUT NEEDED PERMISSIONS.'