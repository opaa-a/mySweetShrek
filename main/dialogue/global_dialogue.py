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
    NOEXC = '\033[32;1m[+] '
    COM = '\033[35;1m[COM] '
    WAIT = '\033[35m[...] '

# Dialogue default icons
class dialogue_icon:
    success = ':ballot_box_with_check:'
    error = ':exclamation:'
    fail = ':x:'
    dm = '📨'

# Dialogue global variables
class global_dialogue_var:
    # currency used on the server.
    currency = "pipi-coins"
    # name used for the store.
    storeName = "Pipi-Store"

# Global scope dialogues
class Global_Dialogue:
    # return if user is not allowed to perform a command
    def user_not_allowed(command: str, userID: discord.Member):
        print(f'\t{log_format.FAIL} COMMAND {command} FAILED - USER {userID} TRIED TO PERFORM THIS COMMAND WITHOUT NEEDED PERMISSIONS.{log_format.END}')
        return f'{dialogue_icon.fail}   Ohoh! Looks like you are not allowed to perform this command.'
    
    # return if a required argument is missing
    def arg_missing(command: str, userID: discord.Member, command_typo: str = None):
        print(f'\t{log_format.FAIL} COMMAND {command} FAILED - USER {userID} DID NOT SPECIFIED A REQUIRED ARGUMENT.{log_format.END}')
        return (
            f'{dialogue_icon.fail}   Oh no! You missed one or multiple required arguments!'
            f'\n*Try again with this typo:  `{command_typo}`*'
            )
    def bad_arg(command: str, userID: discord.Member, command_typo: str = None):
        print(f'\t{log_format.FAIL} COMMAND {command} FAILED - USER {userID} SPECIFIED A WRONG ARGUMENT.{log_format.END}')
        return (
            f'{dialogue_icon.fail}   Ohoh! Looks like one or multiple arguments you mentioned are incorrect.'
            f'\n*Try again with this typo:  `{command_typo}`*'
            )
    # return if user is not registered
    def user_not_registered(command: str, userID : discord.Member = None):
        print(f'\t{log_format.FAIL} COMMAND {command} FAILED - USER IS NOT REGISTERED TO THE VAULT.{log_format.END}')
        if userID == None:
            return (
                f'\n{dialogue_icon.fail}   Ohoh! Looks like you are not register into the vault!'
                f'\n*Use `!register` to register to the vault.*'
                )
        return (
            f'{dialogue_icon.fail}   Ohoh! Looks like {userID} is not registered into the vault.')
    # return if user can't pay something
    def user_cant_pay(command: str, userID : discord.Member = None):
        if userID == None:
            print(f'\t{log_format.FAIL} COMMAND {command} FAILED - AUTHOR CAN\'T AFFORD THIS TRANSACTION')
            return (
                f'{dialogue_icon.fail}   Nope, looks like your broke ass don\'t have enough money.'
                f'\n*Use `!balance` to check your balance.*'
                )
        print(f'\t{log_format.FAIL} COMMAND {command} FAILED - USER {userID} CAN\'T AFFORD THIS TRANSACTION')
        return (
            f'{dialogue_icon.fail}   Nope, looks like {userID} is broke and can\'t afford this transaction.'
            )
    # return if command is in dm
    def command_executed_in_dm(command: str, userID: discord.Member):
        print(f'\t{log_format.FAIL} COMMAND {command} FAILED - USER {userID} EXECUTED THIS COMMAND IN THE BOT DMs.{log_format.END}')
        return f'{dialogue_icon.fail}   Oops! You need to execute this command in a channel and not in my DMs!'

    # return if query is exited by an error
    def query_exit(error: str, querry_type: str, userID: discord.Member):
        print(f'\t{log_format.FAIL} QUERRY {querry_type} HAS BEEN EXITED BY {userID} DUE TO FOLLOWING ERROR {error}.{log_format.END}')
        
        if error == 'unknown_ID':            
            return (
                f'> *This ID does not exist!*'
                f'\n> *You exited the {querry_type} query*'
                )
        if error == 'valueError_int':
            return (
                f'> *Your query must be a number!*'
                f'\n> *You exited the {querry_type} query*'
            )
        if error == 'valueError_str':
            return (
                f'> *Your query must be a word!*'
                f'\n> *You exited the {querry_type} query*'
            )

# Global scope logs
class Global_Log:
    # log everytime user use command    
    def command_has_been_used(command: str, userID: discord.Member):
        return f'\n{log_format.COM} COMMAND {command} has been used by {userID} at {log_format.DATE}{log_format.END}'
    # log everytime command is run without exception
    def command_run_without_exception(command: str):
        return f'\t{log_format.NOEXC} {command} RAN WITHOUT EXCEPTION.{log_format.END}'
    # log when bot is waiting for a query
    def bot_is_waiting_for_querry(userID: discord.Member):
        return f'\t{log_format.WAIT} BOT IS WAITING FOR QUERRY FROM {userID}.{log_format.END}'
    # return when query is successful
    def querry_success(querry_type: str, userID: discord.Member):
        return f'\t{log_format.NOEXC} {querry_type} QUERRY REQUEST HAS BEEN SUCCESSFULLY USED BY {userID}.{log_format.END}'