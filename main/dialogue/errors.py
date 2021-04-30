import discord
from discord.ext import commands
from .dialogue import *

#---------------------------------------------------------------------------------------#       GLOBAL ERRORS       #---------------------------------------------------------------------------------------#

# error message when user is not registered to the vault.
def error_user_has_no_vault(userID : discord.Member = None):
    if userID == None:
        return (
            f'\n:x:   Ohoh! Looks like you are not register into the vault!'
            f'\n\n:arrow_right:   Use ` !register ` to register to the vault.'
            )
    return (
        f':x:   Ohoh! Looks like {userID} is not registered into the vault.')

# error message when user does not have admin privileges
def error_user_is_not_admin(userID : discord.Member = None):
    if userID == None:
        return (
            f'\n:x:   Oh no no no... You don\'t have access to this command mate. :face_with_monocle:'
            )
    return (
        f':x:   {userID} does not have admin privileges... too bad. :hugging:'
        )

# error message when user tries to register while being already registered
def error_user_is_already_registered(userID : discord.Member = None):
    if userID == None:
        return (
            f':x:   Ohoh! Looks like you are already registered!'
            )
    return (
        f':x:   Ohoh! Looks like {userID} is already registered!'
        )
