import discord
#---------------------------------------------------------------------------------------#       LOG ERRORS       #---------------------------------------------------------------------------------------#

def log_error_bad_arg(target: str):
    return (
        f'# ERROR -- {target} -- Bad Argument(s) declared!'
        )

def log_error_missing_arg(target: str):
    return (
        f'# ERROR -- {target} -- Missing Required Argument(s)!'
    )

def unknown_error():
    return (
        f'**:exclamation: Unknown error, please contact the administrator.**'
        )

# message display when a querry is not successful in the !help section
def querry_exit(exit_type: str, querry_type: str):
    if exit_type == "unknown_ID":
        return (
            f'> *This ID does not exist!*'
            f'\n> *You exited the {querry_type} querry*'
            )
    if exit_type == "valueError_int":
        return (
            f'> *Your querry must be a number!*'
            f'\n> *You exited the {querry_type} querry*'
        )
    if exit_type == "valueError_str":
        return (
            f'> *Your querry must be a word!*'
            f'\n> *You exited the {querry_type} querry*'
        )
    # return unknown_error()
#---------------------------------------------------------------------------------------#       GLOBAL ECONOMY COG FUNCTIONS ERRORS       #---------------------------------------------------------------------------------------#

# error message when user is not registered to the vault.
def error_user_has_no_vault(userID : discord.Member = None):
    if userID == None:
        return (
            f'\n:x:   Ohoh! Looks like you are not register into the vault!'
            f'\n\n:arrow_right:   Use ` !register ` to register to the vault.'
            )
    return (
        f':x:   Ohoh! Looks like {userID} is not registered into the vault.')

# error message when user tries to register while being already registered
def error_user_is_already_registered(userID : discord.Member = None):
    if userID == None:
        return (
            f':x:   Ohoh! Looks like you are already registered!'
            )
    return (
        f':x:   Ohoh! Looks like {userID} is already registered!'
        )

# error message when user can't pay
# def error_user_cant_pay(userID : discord.Member = None):
#     if userID == None:
#         return (
#             f':x:   Nope, looks like your broke ass don\'t have enough money.'
#             f'\n:arrow_right:   Use ` !balance ` to check your balance.'
#             )
#     return (
#         f':x:   Nope, looks like {userID} is broke and can\'t afford this transaction.'
#         )

# error message when user tries to pay himself
def error_user_cant_pay_himself():
    return (
        f':x:   Dude, paying yourself, with your own money ins\'t going to do shit.'
        f'\n:arrow_right:   Try paying an other user; ` !pay <user> <amount> `'
        )


#---------------------------------------------------------------------------------------#       GLOBAL ECONOMY COG COMMANDS ERRORS       #---------------------------------------------------------------------------------------#

# error message when !addcoins fails to execute.
def error_addcoins(error_type : str):
    if error_type == "bad_arg":
        return (
            f':x:   Oops! Looks like one or multiple arguments specified are not valid.'
            f'\n:arrow_right:   ` !addcoins <amount> <userID> `' 
            f'\n> *<amount> is a number, <userID>, if not specified is yourself.*'
            )
    elif error_type == "missing_arg":
        return (
            f':x:   Oops! You need to provide at least the amount.'
            f'\n:arrow_right:   ` !addcoins <amount> <userID> `'
            f'\n> *<amount> is a number and must be declared.*'
            f'\n> *<userID> is optional, default is yourself.*'
            )
    return print("# UNKNOWN ERROR -- !addcoins FAILED TO SPECIFY ERROR TYPE")

# error message when !balance fails to execute.
def error_balance(error_type : str):
    if error_type == "bad_arg":    
        return (
            f':x:   Oops! Looks like the user you specified doesn\'t exist. :pensive:'
            )
    return print("# UNKNOWN ERROR -- !balance FAILED TO SPECIFY ERROR TYPE")

# error message when !pay fails to execute
def error_pay(error_type: str):
    if error_type == "bad_arg":
        return (
            f':x:   Oops! Looks like one or multiple arguments specified are not valid.'
            f'\n:arrow_right:   ` !pay <user> <amount> `'
            f'\n> *<user> must be specified and must be an existing user on the server*'
            f'\n> *<amount> must be specified and must be a number*'
            )
    elif error_type == "missing_arg":
        return (
            f':x:   Oops! Looks like you forgot to specify one or multiple arguments.'
            f'\n:arrow_right:   ` !pay <user> <amount> `'
            f'\n> *Both <user> and <amount> must be specified!*'
            )
    return print("# UNKNOWN ERROR -- !pay FAILED TO SPECIFY ERROR TYPE")

# error message when !coinflip fails to execute
def error_coinflip(error_type: str):
    if error_type == "fail_ans":
        return (
            f':x:   You failed answering a simple "head or tail" question, no doubt that\'s why your life sucks.'
            f'\n:arrow_right: ` !cf <amount> ` to try again.'
            )
    elif error_type == "bad_arg":
        return (
            f':x:   Ohoh! Looks like you don\'t know what a fucking number is!'
            f'\n> ` !cf <amount> ` (amount being a number...)'
            )
    elif error_type == "missing_arg":
        return (
            f':x:   Ohoh! Looks like you forgot to specify the amount!'
            f'\n> ` !cf <amount> `'
            )
    return print("# UNKNOWN ERROR -- !coinflip FAILED TO SPECIFY ERROR TYPE")


#---------------------------------------------------------------------------------------#       GLOBAL ESSENTIAL COG COMMANDS ERRORS       #---------------------------------------------------------------------------------------#

def error_help(error_type: str):
    if error_type == "bad_arg":
        return (
            f':x:   Oops! The theme you\'re looking for doesn\'t exist.'
            f'\n*To access a theme, you must reply to the bot with the number associated to the theme.*'
            )
    return print("# UNKNOWN ERROR -- !store FAILED TO SPECIFY ERROR TYPE")

#---------------------------------------------------------------------------------------#       GLOBAL STORE COG COMMANDS ERRORS       #---------------------------------------------------------------------------------------#

# error message when !store fails to execute
def error_store(error_type: str):
    if error_type == "bad_arg":
        return (
            f':x:   Oops! The parameter of store you specified doesn\'t exist.'
            f'\n:arrow_right: ` !store help `'
            )
    return print("# UNKNOWN ERROR -- !store FAILED TO SPECIFY ERROR TYPE")


#---------------------------------------------------------------------------------------#       GLOBAL INVENTORY COG COMMANDS ERRORS       #---------------------------------------------------------------------------------------#

# error message when !use fails to execute
def error_use(error_type: str):
    if error_type == "bad_arg":
        return (
            f':x:   Oops! Looks like one or multiple arguments specified are not valid.'
            f'\n:arrow_right:   ` !use <target> <item> `'
            f'\n> *<target> must be specified and must be an existing AND CONNECTED user on the server*'
            f'\n> *<item> must be specified and must be available in your inventory*'
        )
    if error_type == "missing_arg":
        return (
            f':x:   Oops! You need to specify a target and an item to use.'
            f'\n:arrow_right:   ` !use <target> <item> `'
        )
    return print("# UNKNOWN ERROR -- !use FAILED TO SPECIFY ERROR TYPE")
