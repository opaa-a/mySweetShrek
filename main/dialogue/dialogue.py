import discord
from discord.ext import commands
from .errors import *

#---------------------------------------------------------------------------------------#       GLOBAL VARIABLES       #---------------------------------------------------------------------------------------#

# feedback depending on the reward chose to be claimed. (linked to !claim)
global claim_feedback
# currency used on the server.
global currency
currency = "pipi-coins"

#---------------------------------------------------------------------------------------#        GLOBAL INTERACTIONS       #---------------------------------------------------------------------------------------#

# message display when !register is successful
def register_success(userID : discord.Member = None):
    if userID == None:
        return (
            f':ballot_box_with_check:   YES PAPAAAA!   :zany_face::zany_face:'
            f'\n> You have been successfully registered.'
            f'\n> You can now earn {currency}!   :money_with_wings:'
            f'\n> *You can access all the commands related to the economy with* ` !economy `'
            )
    return (
        f':ballot_box_with_check:   YES PAPAAAA!   :zany_face::zany_face:'
        f'\n> {userID} Has been successfully registered!'
    )

# message display when !add_coins is successful
def add_coins_success(amount, userID : discord.Member = None):
    if userID == None:
        return (
            f':ballot_box_with_check:   MONEY MONEY MONEY   :money_with_wings::money_with_wings:'
            f'\n> **{amount}** {currency} have been added to your vault!'
            f'\n:money_with_wings::money_with_wings::money_with_wings:'
            )
    return (
        f':ballot_box_with_check:   MONEY MONEY MONEY   :money_with_wings::money_with_wings:'
        f'\n> **{amount}** {currency} have been added to {userID}\'s vault!'
        f'\n:money_with_wings::money_with_wings::money_with_wings:'
        )

# message display when !balance is successful
def balance_success(balance, userID : discord.Member = None):
    author = False
    if userID == None:
        author = True
    
    if balance >= 100000 and author:
        return (
            f':gem::gem::gem:   You got exactly **{balance}** {currency} on your vault account...'
            f'\n:rainbow:   Capitalistic cunt.'
            )
    if balance >= 100000:
        return (
            f':gem::gem::gem:   {userID} got exactly **{balance}** {currency} on his vault account...'
            f'\n:rainbow:   Capitalistic cunt.'
            )
    
    if balance >= 50000 and author:
        return (
            f':gem:   You got exactly **{balance}** {currency} on your vault account...'
            f'\n:sunny:   Playing coinflip to get to top balance is the peak of what you can achieve in life. Fucking Nerd.'
            )
    elif balance >= 50000:
        return (
            f':gem:   {userID} got exactly **{balance}** {currency} on his vault account...'
            f'\n:sunny:   Playing coinflip to get to top balance is the peak of what {userID} can achieve in his life. Fucking Nerd.'
            )

    if balance >= 30000 and author:
        return (
            f':moneybag:   You got exactly **{balance}** {currency} on your vault account...'
            f'\n:partly_sunny:   Booooouuuh, you are pooooor! Get ouuut! Boooooouhhh'
            )
    elif balance >= 30000 and author:
        return (
            f':moneybag:   {userID} got exactly **{balance}** {currency} on his vault account...'
            f'\n:partly_sunny:   Yikes {userID}, booooouuuuh look how poor he is. boouh, disgusting.'
            )

    if balance >= 10000 and author:
        return (
            f':coin:   You got exactly **{balance}** {currency} on your vault account...'
            f'\n:cloud:   Got enough to buy yourself a rope and a stool...'
            )
    elif balance >= 10000:
        return (
            f':coin:   {userID} got exactly **{balance}** {currency} on his vault account...'
            f'\n:cloud:   {userID} has just enough to buy himself a rope and a stool, what a lucky guy!'
            )

    if balance > 0 and author:
        return (
            f':coin:   You got exactly **{balance}** {currency} on your vault account...'
            f'\n:cloud_rain:   About to be homeless with that kind of money...'
            )
    elif balance > 0:
        return (
            f':coin:   {userID} got exactly **{balance}** {currency} on his vault account...'
            f'\n:cloud_rain:   About to be homeless with that kind of money...'
            )
    
    if balance <= 0 and author:
        return (
            f':coin:   You got exactly **{balance}** {currency} on your vault account...'
            f'\n:thunder_cloud_rain:   Sell a kidney.'
            )
    elif balance <= 0:
        return (
            f':coin:   {userID} got exactly **{balance}** {currency} on his vault account...'
            f':thunder_cloud_rain:   {userID} gotta sell a kidney.'
            )


# message display when !balancetop is successfull
def balancetop_success(baltop):
    pre_format_baltop = []
    index = 0
    
    for i in baltop:
        if index == 0:
            pre_format_baltop.append(f':crown: **{i[0]}** : **{i[1]}** {currency}')
        elif index == 1:
            pre_format_baltop.append(f'> :second_place: **{i[0]}** : **{i[1]}** {currency}')
        elif index == 2:
            pre_format_baltop.append(f'> :third_place: **{i[0]}** : **{i[1]}** {currency}')
        else:
            pre_format_baltop.append(f'> :hot_face: **{i[0]}** : **{i[1]}** {currency}')
        index += 1
    
    formated_baltop = f'\n\n'.join([i for i in pre_format_baltop])
    return (
        f':gem:   **Remember that y\'all are poor if I want to.**   :gem:'
        f'\n\n> {formated_baltop}'
        )