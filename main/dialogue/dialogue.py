import discord
import json
from discord.ext import commands


#---------------------------------------------------------------------------------------#       GLOBAL VARIABLES       #---------------------------------------------------------------------------------------#

# feedback depending on the reward chose to be claimed. (linked to !claim)
global claim_feedback
# currency used on the server.
global currency
currency = "pipi-coins"
# name used for the store.
global storeName
storeName = "Pipi-Store"

#---------------------------------------------------------------------------------------#       GLOBAL FUNCTIONS       #---------------------------------------------------------------------------------------#



#---------------------------------------------------------------------------------------#        GLOBAL ECONOMY COG INTERACTIONS       #---------------------------------------------------------------------------------------#

# display the economy help section
# def help_economy_success():
#     with open('main/assets/help.json') as help_index:
#         help_economy = json.load(help_index)
#         help_economy = help_economy["Economy"]
#         help_economy_list = list(help_economy)
#         preformat_display_theme = []
#         for theme in help_economy:
#             preformat_display_theme.append(
#                 f'\n> ` {help_economy_list.index(theme)} `   :white_small_square:   **{theme}**'
#                 )
#         display_help_economy = f'\n> '.join([i for i in preformat_display_theme])
    
#     return (
#         f':bank:    **WELCOME TO THE ECONOMY HELP SECTION!**    :bank:'
#         f'\n\n> **Reply to this message with the number associated to the theme to get more informations about it!**'
#         f'\n> **If there is a theme that is not referenced and you have a unanswered question, please contact an administrator.**'
#         f'\n> '
#         f'{display_help_economy}'
#     )
# display the economy help theme section
# def help_economy_querry(querry : int):
#     with open('main/assets/help.json') as help_index:
#         help_economy = json.load(help_index)
#         help_economy = help_economy["Economy"]
#         help_economy_list = list(help_economy)
#         help_economy_exp_list = list(help_economy.values())
#         theme_index = querry
#     return (
#         f'> :question:    {help_economy_list[theme_index]}'
#         f'\n> '
#         f'\n> :speech_left:    {help_economy_exp_list[theme_index]}'
#         )
# display the grind help section
# def help_grind_success():
#     with open('main/assets/help.json') as help_index:
#         help_grind = json.load(help_index)
#         help_grind = help_grind["Grind"]
#         help_grind_list = list(help_grind)
#         preformat_display_theme = []
#         for theme in help_grind:
#             preformat_display_theme.append(
#                 f'\n> ` {help_grind_list.index(theme)} `   :white_small_square:   **{theme}**'
#                 )
#         display_help_grind = f'\n> '.join([i for i in preformat_display_theme])
    
#     return (
#         f':money_mouth:    **WELCOME TO THE GRIND HELP SECTION!**    :money_mouth:'
#         f'\n\n> **Reply to this message with the number associated to the theme to get more informations about it!**'
#         f'\n> **If there is a theme that is not referenced and you have a unanswered question, please contact an administrator.**'
#         f'\n> '
#         f'{display_help_grind}'
#     )
# display the grind theme help section
# def help_grind_querry(querry : int):
#     with open('main/assets/help.json') as help_index:
#         help_grind = json.load(help_index)
#         help_grind = help_grind["Grind"]
#         help_grind_list = list(help_grind)
#         help_grind_exp_list = list(help_grind.values())
#         theme_index = querry
#     return (
#         f'> :question:    {help_grind_list[theme_index]}'
#         f'\n> '
#         f'\n> :speech_left:    {help_grind_exp_list[theme_index]}'
#         ) 
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

# # message display when !help is successful
# # display the help section
# def help_index_success():
#     with open('main/assets/help.json') as help_index:
#         help_index = json.load(help_index)
#         index_list = list(help_index)
#         preformat_index_list = []
#         for theme in index_list:
#             preformat_index_list.append(
#                 f'\n> ` {index_list.index(theme)} `   :white_small_square:   **{theme}**'
#                 )
#         display_help_index = f'\n> '.join([i for i in preformat_index_list])

#     return (
#         f':dividers:    **WELCOME TO THE HELP INDEX!**    :dividers:'
#         f'\n\n> **Reply to this message with the number associated to the theme to get more informations about it!**'
#         f'\n> **If there is a theme that is not referenced and you have a unanswered question, please contact an administrator.**'
#         f'\n> '
#         f'{display_help_index}'
#         )

# # display the general help section
# def help_general_success():
#     with open('main/assets/help.json') as help_index:
#         help_general = json.load(help_index)
#         help_general = help_general["General"]
#         help_general_list = list(help_general)
#         preformat_display_theme = []
#         for theme in help_general:
#             preformat_display_theme.append(
#                 f'\n> ` {help_general_list.index(theme)} `   :white_small_square:   **{theme}**'
#                 )
#         display_help_general = f'\n> '.join([i for i in preformat_display_theme])
    
#     return (
#         f':globe_with_meridians:    **WELCOME TO THE GENERAL HELP SECTION!**    :globe_with_meridians:'
#         f'\n\n> **Reply to this message with the number associated to the theme to get more informations about it!**'
#         f'\n> **If there is a theme that is not referenced and you have a unanswered question, please contact an administrator.**'
#         f'\n> '
#         f'{display_help_general}'
#     )

# # display the general theme help section
# def help_general_querry(querry : int):
#     with open('main/assets/help.json') as help_index:
#         help_general = json.load(help_index)
#         help_general = help_general["General"]
#         help_general_list = list(help_general)
#         help_general_exp_list = list(help_general.values())
#         theme_index = querry
#     return (
#         f'> :question:    {help_general_list[theme_index]}'
#         f'\n> '
#         f'\n> :speech_left:    {help_general_exp_list[theme_index]}'
#         )

#---------------------------------------------------------------------------------------#        GLOBAL STORE COG INTERACTIONS       #---------------------------------------------------------------------------------------#

# message display when !store help or !store is successful
# display the Q&A section
# def help_store_success():
#     with open('main/assets/help.json') as help_index:
#         help_store = json.load(help_index)
#         help_store = help_store["Store"]
#         help_store_list = list(help_store)
#         preformat_display_theme = []
#         for theme in help_store:
#             preformat_display_theme.append(
#                 f'\n> ` {help_store_list.index(theme)} `   :white_small_square:   **{theme}**'
#                 )
#         display_help_store = f'\n> '.join([i for i in preformat_display_theme])

#     return (
#         f':department_store:    **WELCOME TO THE {storeName.upper()} HELP SECTION!**    :department_store:'
#         f'\n\n> **Reply to this message with the number associated to the them to get more informations about it!**'
#         f'\n> **If there is a theme that is not referenced and you have a unanswered question, please contact an administrator.**'
#         f'\n> '
#         f'{display_help_store}'
#         )

# message display when a querry is successful in the !store help section
# def help_store_querry(querry : int):
#     with open('main/assets/help.json') as help_index:
#         help_store = json.load(help_index)
#         help_store = help_store["Store"]
#         help_store_list = list(help_store)
#         help_store_exp_list = list(help_store.values())
#         theme_index = querry
#     return (
#         f'> :question:    {help_store_list[theme_index]}'
#         f'\n> '
#         f'\n> :speech_left:    {help_store_exp_list[theme_index]}'
#         )   
        
# message display when !store showcase is successful
# display the list of all available commands to buy
def store_showcase_success():
    with open('main/assets/store_inv.json') as store_inv:
        store_inv = json.load(store_inv)
        preformat_store_inv = []
        for item in store_inv:
            preformat_store_inv.append(
                f'\n> {store_inv[item]["icon"]} ` {item} `   :   **{store_inv[item]["price"]} {currency} :coin:**'
                f'\n>   *{store_inv[item]["desc"]}*'
                ) 
        store_inv_showcase = f'\n> '.join([i for i in preformat_store_inv])
    return (
        f':shopping_bags:   **WELCOME TO THE {storeName.upper()}!**   :shopping_bags:'
        f'\n\n> **Here are displayed all the currently available-to-purchase commands!**'
        f'\n> '
        f'{store_inv_showcase}'
        ) 

# message display when !store buy is successful
def store_buy_success():
    return(
        f':shopping_bags:   **WELCOME TO THE {storeName.upper()}!**   :shopping_bags:'
        f'\n\n> **Reply to this message with the name of the item you want to purchase**'
        f'\n> **To get the list of all the items in the store ` !store showcase `**'
        )

def store_purchase_complete(item_name : str):
    return (
        f':package:   **You successfully purchased {item_name}**   :package:'
        f'\n> *Your item has been placed in your inventory.*'
        f'\n> *Learn more about the inventory in with the* ` !help ` *command.*'
        )

#---------------------------------------------------------------------------------------#        GLOBAL INVENTORY COG INTERACTIONS       #---------------------------------------------------------------------------------------#

# display the inventory help section
def help_inv_success():
    with open('main/assets/help.json') as help_index:
        help_inv = json.load(help_index)
        help_inv = help_inv["Inventory"]
        help_inv_list = list(help_inv)
        preformat_display_theme = []
        for theme in help_inv:
            preformat_display_theme.append(
                f'\n> ` {help_inv_list.index(theme)} `   :white_small_square:   **{theme}**'
                )
        display_help_inv = f'\n> '.join([i for i in preformat_display_theme])

    return (
        f':package:    **WELCOME TO THE INVENTORY HELP SECTION!**    :package:'
        f'\n\n> **Reply to this message with the number associated to the them to get more informations about it!**'
        f'\n> **If there is a theme that is not referenced and you have a unanswered question, please contact an administrator.**'
        f'\n> '
        f'{display_help_inv}'
        )

# display the general theme help section
def help_inv_querry(querry : int):
    with open('main/assets/help.json') as help_index:
        help_inv = json.load(help_index)
        help_inv = help_inv["Inventory"]
        help_inv_list = list(help_inv)
        help_inv_exp_list = list(help_inv.values())
        theme_index = querry
    return (
        f'> :question:    {help_inv_list[theme_index]}'
        f'\n> '
        f'\n> :speech_left:    {help_inv_exp_list[theme_index]}'
        )

# display the userID inventory
def display_inv_success(inventory):
    with open('main/assets/store_inv.json') as store_inv:
        store_inv = json.load(store_inv)
        preformat_display_inventory = []
        if inventory == {}:
            return (
            f':package:   **THIS IS YOUR INVENTORY**   :package:'
            f'\n> '
            f'\n> :wind_blowing_face::leaves::wind_blowing_face:'
            f'\n> **Ohoh! Looks like your inventory is empty**'
                )
        for item in inventory:
            icon = store_inv[item]['icon']
            desc = store_inv[item]['desc']
            amount = inventory[item]
            preformat_display_inventory.append(
                f'\n> **{icon} ` {item} ` x ` {amount} `**'
                f'\n> *{desc}*'
                )
            display_inventory = f'\n> '.join([i for i in preformat_display_inventory])

    return (
        f':package:   **THIS IS YOUR INVENTORY**   :package:'
        f'\n> '
        f'{display_inventory}'
        )

# message display when !use is successful
def use_success(dialogue_ref: str, target: discord.Member, item, author = None):
    # return if author don't have the item
    if dialogue_ref == "item_missing":
        return (
            f':x:   Nope, you can\'t use what you don\'t own.'
            f'\n:arrow_right:   You can buy items with the command: ` !store buy `'
        )
    if dialogue_ref == "command_in_dm":
        return (
            f':x:   You can\'t use the command ` !use ` in my DMs!'
            f'\n:arrow_right:   ` !use <target> <item> `'
        )
    if dialogue_ref == "":
        return (
            f':x:   The target you specified is already in t'
        )
    # return if use is successful
    if dialogue_ref == "item_used":
        author = str(author)
        # get icons of items
        with open('main/assets/store_inv.json') as store_inv:
            store_inv = json.load(store_inv)
            icon = store_inv[item]['icon']
        # get author inv
        with open('main/assets/vault.json') as vault:
            vault = json.load(vault)
            item_amount = int(vault[author]['inventory'][item])
        
        return (
            f'{icon}   **You successfully used {item} on {target}!**'
            f'\n:package: You now have ` {item_amount} ` **x** ` {item} ` in your inventory.'
            )

def item_a_la_niche_success(dialogue_ref: str, target: discord.Member):
    if dialogue_ref == "target_already_in_chan":
        return (
            f':x:   Nope, **{target}** is already in ` \'La Niche\' `. Don\'t waste your item.'
            )
    if dialogue_ref == "target_not_connected":
        return (
            f':x:   Ohoh! You can\'t use this command if the target is not connected to a vocal channel.'
        )
    if dialogue_ref == "target_is_bot":
        return (
            f':x:   No no no, you can\'t use this command on bots!'
        )

def item_shush_success(dialogue_ref: str, target: discord.Member):
    if dialogue_ref == "target_is_already_muted":
        return (
            f':x:   Nope, **{target}** is already muted!'
            )
    if dialogue_ref == "target_not_connected":
        return (
            f':x:   Ohoh! You can\'t use this command if the target is not connected to a vocal channel.'
            )
    if dialogue_ref == "target_is_bot":
        return (
            f':x:   No no no, you can\'t use this command on bots!'
        )

def item_mauvais_toutou(dialogue_ref: str, target: discord.Member):
    if dialogue_ref == "target_already_has_role":
        return (
            f':x:   Nope, **{target}** is already \'Mauvais toutou\'!'
            )
    if dialogue_ref == "target_is_not_registered":
        return (
            f':x:   Ohoh! Looks like **{target}** is not registered to the vault. You can\'t target users that are not in the vault.'
            )
    if dialogue_ref == "target_is_bot":
        return (
            f':x:   No no no, you can\'t use this command on bots!'
            )