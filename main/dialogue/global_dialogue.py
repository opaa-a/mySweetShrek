import discord
from datetime import datetime

# Log message template
class log_format:
    now = datetime.now()
    DATE = now.strftime('%H:%M:%S | %m/%d/%Y')
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    INFO = '\033[96m[i] '
    ERROR = '\033[93;4;1m/!\ '
    FAIL = '\033[31;1m[-] '
    NOEXC = '\033[32;1m[+]'
    COM = '\033[35;1m[COM]'

# Dialogue default icons
class dialogue_icon:
    success = ':ballot_box_with_check:'
    error = ':exclamation:'
    fail = ':x:'
    dm = '📨'

# Global scope dialogues
class Global_Dialogue:
    # return if user is not allowed to perform a command
    def user_not_allowed(command:str, userID: discord.Member):
        print(f'\t{log_format.FAIL} COMMAND {command} FAILED - USER {userID} TRIED TO PERFORM THIS COMMAND WITHOUT NEEDED PERMISSIONS.{log_format.END}')
        return f'{dialogue_icon.fail}   Ohoh! Looks like you are not allowed to perform this command.'
    
    # return if a required argument is missing
    def arg_missing(command: str, userID: discord.Member, command_typo: str = None):
        print(f'\t{log_format.FAIL} COMMAND {command} FAILED - USER {userID} DID NOT SPECIFIED A REQUIRED ARGUMENT{log_format.END}')
        return (
            f'{dialogue_icon.fail}   Oh no! You missed one or multiple required arguments!'
            f'\n*Try again with this typo:  `{command_typo}`*'
            )

    # return if command is in dm
    def command_executed_in_dm(command: str, userID: discord.Member):
        print(f'\t{log_format.FAIL} COMMAND {command} FAILED - USER {userID} EXECUTED THIS COMMAND IN THE BOT DMs.{log_format.END}')
        return f'{dialogue_icon.fail}   Oops! You need to execute this command in a channel and not in my DMs!'

# Global scope logs
class Global_Log:
    # log everytime user use command    
    def command_has_been_used(command: str, userID: discord.Member):
        return f'\n{log_format.COM} COMMAND {command} has been used by {userID} at {log_format.DATE}{log_format.END}'
    def command_run_without_exception(command: str):
        return f'{log_format.NOEXC} {command} RAN WITHOUT EXCEPTION.{log_format.END}'