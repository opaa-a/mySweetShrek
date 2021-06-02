import discord
import json
from discord.ext import commands
from dialogue.errors import *
from cogs.economy import *
from cogs.essential import *
from cogs.store import *


#---------------------------------------------------------------------------------------#       GLOBAL VARIABLES       #---------------------------------------------------------------------------------------#

# feedback depending on the reward chose to be claimed. (linked to !claim)
global claim_feedback
# currency used on the server.
global currency
currency = "pipi-coins"
# name used for the store.
global storeName
storeName = "Pipi-Store"

#---------------------------------------------------------------------------------------#        GLOBAL ECONOMY COG INTERACTIONS       #---------------------------------------------------------------------------------------#

# message display when !register is successful
def register_success(userID : discord.Member = None):
    if userID == None:
        return (
            f':ballot_box_with_check:   YES PAPAAAA!   :zany_face::zany_face:'
            f'\n> You have been successfully registered.'
            f'\n> You can now earn {currency}!   :money_with_wings:'
            f'\n> *You can access all the commands related to the economy with* ` !help economy `'
            )
    return (
        f':ballot_box_with_check:   YES PAPAAAA!   :zany_face::zany_face:'
        f'\n> {userID} Has been successfully registered!'
    )

# message display when !addcoins is successful
def addcoins_success(amount, userID : discord.Member = None):
    if userID == None:
        return (
            f':money_with_wings:   MONEY MONEY MONEY   :money_with_wings:'
            f'\n> **{amount}** {currency} have been added to your vault!'
            )
    return (
        f':money_with_wings:   MONEY MONEY MONEY   :money_with_wings:'
        f'\n> **{amount}** {currency} have been added to {userID.mention}\'s vault!'
        )

# message display when !balance is successful
def balance_success(balance, userID : discord.Member = None):
    author = False
    if userID == None:
        author = True
    
    if balance >= 100000 and author:
        return (
            f':gem::gem::gem:   You got exactly **{balance}** {currency} on your vault account...'
            f'\n:rainbow::rainbow::rainbow:   Capitalistic cunt.'
            )
    if balance >= 100000:
        return (
            f':gem::gem::gem:   {userID} got exactly **{balance}** {currency} on his vault account...'
            f'\n:rainbow::rainbow::rainbow:   Capitalistic cunt.'
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
            f'\n:thunder_cloud_rain:   {userID} gotta sell a kidney.'
            )


# message display when !balancetop is successful
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


# message display when !pay is successful
def pay_success(amount : int, userID : discord.Member):
    return (
        f':money_with_wings:   You successfully sent {amount} {currency} to {userID}   :money_with_wings:'
        )

# message display when !coinflip is successful
def coinflip_success(amount: int, author, dialogue_ref: str):
    if dialogue_ref == "cf_init":
        return (
        f':coin: **{author}** is in a playful mood, {amount} {currency} have been bet!'
        f'\n:arrow_right:Pick **HEAD** or **TAIL**'
        f'\n> *You got to write it down, like with your keyboard...*'
        )
    elif dialogue_ref == "cf_win":
        return (
            f':+1:   Well played to **{author}** who won **{amount}** {currency}   :confetti_ball:'
            f'\n> ` !cf <amount> ` to play again!'
            )
    elif dialogue_ref == "cf_lose":
        return (
            f':-1:   Congratulations! **{author}** lost **{amount}** {currency}   :joy::ok_hand:'
            f'\n> ` !cf <amount> ` to play again!'
            )

# message display when !facts is successful
def facts_success(dialogue_ref: str, amount: int):
    if dialogue_ref == "success_with_vault":
        return (
            f':scroll:   Got it!   :joy::ok_hand:'
            f'\n\n:coin:   **You earned {amount} {currency}.**'
            )
    elif dialogue_ref == "success_without_vault":
        return (
            f':scroll:   Got it!   :joy::ok_hand:'
            f'\n\n:hot_face:   **You won nothing though. You are not registered.**'
            f'\n:arrow_right:   ` !register ` to register'
            )

# message display when the daily reward is successful
def daily_reward_success(author, amount, dialogue_ref: str = None):    
    if dialogue_ref == "first_claim":
        return (
            f':partying_face:   **{author} is claiming his daily reward for the very first time!**'
            f'\n:coin:   *{author} got {amount} {currency} from his daily reward!*'
            f'\n:arrow_right:   ` !claim daily ` *to get your own daily reward*'
            )
    elif dialogue_ref == "claim_success":
        return (
            f':calendar:   {author} has claim his daily reward!'
            f'\n:coin:   *{author} got {amount} {currency} from his daily reward!*'
            f'\n:arrow_right:   ` !claim daily ` *to get your own daily reward*'
            )
    return (
        f':x:   Looks like you already claimed that reward today!'
        f'\n:calendar:   Come back tomorrow!'
        )

# message display when !claim is successful
def claim_success():
    return (
        f':gift:   Here is the list of the rewards waiting to be claimed:'
        f'\n> -'
        )


#---------------------------------------------------------------------------------------#        GLOBAL ESSENTIAL COG INTERACTIONS       #---------------------------------------------------------------------------------------#

# message display when !help is successful
# display the help section
def help_index_success():
    with open('main/assets/help.json') as help_index:
        help_index = json.load(help_index)
        index_list = list(help_index)
        preformat_index_list = []
        for theme in index_list:
            preformat_index_list.append(
                f'\n> ` {index_list.index(theme)} `   :white_small_square:   **{theme}**'
                )
        display_help_index = f'\n> '.join([i for i in preformat_index_list])

    return (
        f':globe_with_meridians:    **WELCOME TO THE HELP SECTION!**    :globe_with_meridians:'
        f'\n\n> **Reply to this message with the number associated to the theme to get more informations about it!**'
        f'\n> **If there is a theme that is not referenced and you have a unanswered question, please contact an administrator.**'
        f'\n> '
        f'{display_help_index}'
        )

def help_index_querry(querry : int):
    if querry == 0:
        return (f'general')
    if querry == 1:
        return (f'economy')
    if querry == 2:
        return (f'grind')
    if querry == 3:
        return (f'store')
    if querry == 4:
        return (f'inv')

# message display when a querry is not successful in the !help index section
def help_index_querry_exit():
    return (
        f'> *This theme ID does not exist!*'
        f'\n> *You exited the help querry*'
        )

#---------------------------------------------------------------------------------------#        GLOBAL STORE COG INTERACTIONS       #---------------------------------------------------------------------------------------#

# message display when !store help or !store is successful
# display the Q&A section
def help_store_success():
    with open('main/assets/help.json') as help_index:
        help_store = json.load(help_index)
        help_store = help_store["Store"]
        help_store_list = list(help_store)
        preformat_display_theme = []
        for theme in help_store:
            preformat_display_theme.append(
                f'\n> ` {help_store_list.index(theme)} `   :white_small_square:   **{theme}**'
                )
        display_help_store = f'\n> '.join([i for i in preformat_display_theme])

    return (
        f':bulb:    **WELCOME TO THE {storeName.upper()} HELP SECTION!**    :bulb:'
        f'\n\n> **Reply to this message with the number associated to the them to get more informations about it!**'
        f'\n> **If there is a theme that is not referenced and you have a unanswered question, please contact an administrator.**'
        f'\n> '
        f'{display_help_store}'
        )

# message display when a querry is successful in the !store help section
def help_store_querry(querry : int):
    with open('main/assets/help.json') as help_index:
        help_store = json.load(help_index)
        help_store = help_store["Store"]
        help_store_list = list(help_store)
        help_store_exp_list = list(help_store.values())
        theme_index = querry
    return (
        f'> :question:    {help_store_list[theme_index]}'
        f'\n> '
        f'\n> :speech_left:    *{help_store_exp_list[theme_index]}*'
        )   
        
# message display when a querry is not successful in the !store help section
def help_store_querry_exit():
    return (
        f'> *This theme ID does not exist!*'
        f'\n> *You exited the help querry*'
        )

# message display when !store showcase is successful
# display the list of all available commands to buy
def store_showcase_success():
    with open('main/assets/store_inv.json') as store_inv:
        store_inv = json.load(store_inv)
        preformat_store_inv = []
        for item in store_inv:
            preformat_store_inv.append(
                f'\n> ` {item} `   :   **{store_inv[item]["price"]} {currency} :coin:**'
                f'\n>   *{store_inv[item]["desc"]}*'
                ) 
        store_inv_showcase = f'\n> '.join([i for i in preformat_store_inv])
    return (
        f':shopping_bags:   **WELCOME TO THE {storeName.upper()}!**    :shopping_bags:'
        f'\n\n> **Here are displayed all the currently available-to-purchase commands!**'
        f'\n> '
        f'{store_inv_showcase}'
        ) 

