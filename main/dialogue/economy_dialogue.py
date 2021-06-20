import discord
import json
from dialogue.global_dialogue import *

# ---------------------------------------------- # ESSENTIAL dialogue # ---------------------------------------------- #
class Economy_Essential_Dialogue:
    # FUNCTION
    # help_economy function
    def help_economy_function_success(userID: discord.Member):
        with open('main/assets/help.json') as help_index:
            help_economy = json.load(help_index)
            help_economy = help_economy["Economy"]
            help_economy_list = list(help_economy)
            preformat_display_theme = []
            for theme in help_economy:
                preformat_display_theme.append(
                    f'\n> ` {help_economy_list.index(theme)} `   :white_small_square:   **{theme}**'
                    )
            display_help_economy = f'\n> '.join([i for i in preformat_display_theme])

        print(Global_Log.querry_success('economy help', userID))
        return (
            f':bank:    **WELCOME TO THE ECONOMY HELP SECTION!**    :bank:'
            f'\n\n> **Reply to this message with the number associated to the theme to get more informations about it!**'
            f'\n> **If there is a theme that is not referenced and you have a unanswered question, please contact an administrator.**'
            f'\n> '
            f'{display_help_economy}'
        )
    # help_economy_querry function
    def help_economy_querry(query : int, userID: discord.Member):
        with open('main/assets/help.json') as help_index:
            help_economy = json.load(help_index)
            help_economy = help_economy["Economy"]
            help_economy_list = list(help_economy)
            help_economy_exp_list = list(help_economy.values())
            theme_index = query
        
        print(Global_Log.querry_success('economy help', userID))
        return (
            f'> :question:    {help_economy_list[theme_index]}'
            f'\n> '
            f'\n> :speech_left:    {help_economy_exp_list[theme_index]}'
            )
    # user_cant_pay_himself function
    def user_cant_pay_himself(userID: discord.Member):
        print(f'\t{log_format.FAIL} COMMAND pay FAILED - USER {userID} TRIED TO PAY HIMSELF.{log_format.END}')
        return (
        f'{dialogue_icon.fail}   Dude, paying yourself, with your own money ins\'t going to work.'
        f'\n*Try paying an other user `!pay <user> <amount>`*'
        )

    # COMMAND
    # register command 
    def register_success(userID : discord.Member = None):
        print(Global_Log.command_run_without_exception('register'))
        if userID == None:
            return (
                f':ballot_box_with_check:   YES PAPAAAA!   :zany_face::zany_face:'
                f'\n> You have been successfully registered.'
                f'\n> You can now earn {global_dialogue_var.currency}!   :money_with_wings:'
                f'\n> *You can access all the commands related to the economy with* ` !help economy `'
                )
        return (
            f':ballot_box_with_check:   YES PAPAAAA!   :zany_face::zany_face:'
            f'\n> {userID} Has been successfully registered!'
        )
    # reloadVAULT command
    def reloadVAULT_success(dump_content: str):
        print(Global_Log.command_run_without_exception('reloadVAULT'))
        print(f'\t{log_format.INFO} DUMP: {dump_content}')
        return (
            f'{dialogue_icon.success}   **reloadVAULT has been successful.**'
            f'\n**DUMP CONTENT:**   `{dump_content}`'
            )
    # addcoins command
    def addcoins_success(amount, userID : discord.Member = None):
        print(Global_Log.command_run_without_exception('addcoins'))
        if userID == None:
            return (
                f':money_with_wings:   MONEY MONEY MONEY   :money_with_wings:'
                f'\n> **{amount}** {global_dialogue_var.currency} have been added to your vault!'
                )
        return (
            f':money_with_wings:   MONEY MONEY MONEY   :money_with_wings:'
            f'\n> **{amount}** {global_dialogue_var.currency} have been added to {userID.mention}\'s vault!'
            )
    # balance success
    def balance_success(balance, userID : discord.Member = None):
        print(Global_Log.command_run_without_exception('balance'))
        author = False
        if userID == None:
            author = True
        
        if balance >= 100000 and author:
            return (
                f':gem::gem::gem:   You got exactly **{balance}** {global_dialogue_var.currency} on your vault account...'
                f'\n:rainbow::rainbow::rainbow:   Capitalistic cunt.'
                )
        if balance >= 100000:
            return (
                f':gem::gem::gem:   {userID} got exactly **{balance}** {global_dialogue_var.currency} on his vault account...'
                f'\n:rainbow::rainbow::rainbow:   Capitalistic cunt.'
                )
        
        if balance >= 50000 and author:
            return (
                f':gem:   You got exactly **{balance}** {global_dialogue_var.currency} on your vault account...'
                f'\n:sunny:   Playing coinflip to get to top balance is the peak of what you can achieve in life. Fucking Nerd.'
                )
        elif balance >= 50000:
            return (
                f':gem:   {userID} got exactly **{balance}** {global_dialogue_var.currency} on his vault account...'
                f'\n:sunny:   Playing coinflip to get to top balance is the peak of what {userID} can achieve in his life. Fucking Nerd.'
                )

        if balance >= 30000 and author:
            return (
                f':moneybag:   You got exactly **{balance}** {global_dialogue_var.currency} on your vault account...'
                f'\n:partly_sunny:   Booooouuuh, you are pooooor! Get ouuut! Boooooouhhh'
                )
        elif balance >= 30000 and author:
            return (
                f':moneybag:   {userID} got exactly **{balance}** {global_dialogue_var.currency} on his vault account...'
                f'\n:partly_sunny:   Yikes {userID}, booooouuuuh look how poor he is. boouh, disgusting.'
                )

        if balance >= 10000 and author:
            return (
                f':coin:   You got exactly **{balance}** {global_dialogue_var.currency} on your vault account...'
                f'\n:cloud:   Got enough to buy yourself a rope and a stool...'
                )
        elif balance >= 10000:
            return (
                f':coin:   {userID} got exactly **{balance}** {global_dialogue_var.currency} on his vault account...'
                f'\n:cloud:   {userID} has just enough to buy himself a rope and a stool, what a lucky guy!'
                )

        if balance > 0 and author:
            return (
                f':coin:   You got exactly **{balance}** {global_dialogue_var.currency} on your vault account...'
                f'\n:cloud_rain:   About to be homeless with that kind of money...'
                )
        elif balance > 0:
            return (
                f':coin:   {userID} got exactly **{balance}** {global_dialogue_var.currency} on his vault account...'
                f'\n:cloud_rain:   About to be homeless with that kind of money...'
                )
        
        if balance <= 0 and author:
            return (
                f':coin:   You got exactly **{balance}** {global_dialogue_var.currency} on your vault account...'
                f'\n:thunder_cloud_rain:   Sell a kidney.'
                )
        elif balance <= 0:
            return (
                f':coin:   {userID} got exactly **{balance}** {global_dialogue_var.currency} on his vault account...'
                f'\n:thunder_cloud_rain:   {userID} gotta sell a kidney.'
                )
    # balancetop command
    def balancetop_success(baltop):
        print(Global_Log.command_run_without_exception('balancetop'))
        pre_format_baltop = []
        index = 0
        # get the top 3 and append special icons.
        for i in baltop:
            if index == 0:
                pre_format_baltop.append(f':crown: **{i[0]}** : **{i[1]}** {global_dialogue_var.currency}')
            elif index == 1:
                pre_format_baltop.append(f':second_place: **{i[0]}** : **{i[1]}** {global_dialogue_var.currency}')
            elif index == 2:
                pre_format_baltop.append(f':third_place: **{i[0]}** : **{i[1]}** {global_dialogue_var.currency}')
            else:
                pre_format_baltop.append(f':hot_face: **{i[0]}** : **{i[1]}** {global_dialogue_var.currency}')
            index += 1
        
        formated_baltop = f'\n\n'.join([i for i in pre_format_baltop])
        # create and return an embed
        embed = discord.Embed(title=":gem:   BALANCE TOP   :gem:", description= f'{formated_baltop}', color=discord.Colour.random())
        return embed
    # pay command
    def pay_success(amount : int, userID : discord.Member):
        print(Global_Log.command_run_without_exception('pay'))
        return (
            f':money_with_wings:   You successfully sent {amount} {global_dialogue_var.currency} to {userID}   :money_with_wings:'
            )

# ---------------------------------------------- # ESSENTIAL log # ---------------------------------------------- #
class Economy_Essential_Log:
    # FUNCTION
    # md_balance function
    def md_balance_log(userID: discord.Member, method: str, amount: int):
        return f'\t{log_format.NOEXC} md_balance HAS BEEN SUCCESSFULLY USED FOR {userID} WITH THE METHOD {method} FOR THIS AMOUNT: {amount}.{log_format.END}'

# ---------------------------------------------- # ESSENTIAL error # ---------------------------------------------- #
class Economy_Essential_ErrorHandler:
    def user_already_registered(userID: discord.Member = None):
        print(f'\t{log_format.FAIL} COMMAND register FAILED - USER IS ALREADY REGISTERED')
        if userID == None:
            return (
                f':x:   Ohoh! Looks like you are already registered!'
                )
        return (
            f':x:   Ohoh! Looks like {userID} is already registered!'
            )

# ---------------------------------------------- # GRIND DIALOGUE # ---------------------------------------------- #
class Economy_Grind_Dialogue:
    # FUNCTION
    # help_grind function
    def help_grind_success(userID: discord.Member):
        with open('main/assets/help.json') as help_index:
            help_grind = json.load(help_index)
            help_grind = help_grind["Grind"]
            help_grind_list = list(help_grind)
            preformat_display_theme = []
            for theme in help_grind:
                preformat_display_theme.append(
                    f'\n> ` {help_grind_list.index(theme)} `   :white_small_square:   **{theme}**'
                    )
            display_help_grind = f'\n> '.join([i for i in preformat_display_theme])
        
        print(Global_Log.querry_success('grind help', userID))
        return (
            f':money_mouth:    **WELCOME TO THE GRIND HELP SECTION!**    :money_mouth:'
            f'\n\n> **Reply to this message with the number associated to the theme to get more informations about it!**'
            f'\n> **If there is a theme that is not referenced and you have a unanswered question, please contact an administrator.**'
            f'\n> '
            f'{display_help_grind}'
        )
    # help_grind_querry function
    def help_grind_querry(query : int, userID: discord.Member):
        with open('main/assets/help.json') as help_index:
            help_grind = json.load(help_index)
            help_grind = help_grind["Grind"]
            help_grind_list = list(help_grind)
            help_grind_exp_list = list(help_grind.values())
            theme_index = query
        print(Global_Log.querry_success('grind help', userID))
        return (
            f'> :question:    {help_grind_list[theme_index]}'
            f'\n> '
            f'\n> :speech_left:    {help_grind_exp_list[theme_index]}'
            ) 
    # bon_toutou function
    def bon_toutou_success(userID: discord.Member):
        print(f'\t{log_format.NOEXC} {userID} HAS BEEN SUCCESSFULLY ASSGINED THE ROLE OF bon toutou.{log_format.END}')
        return (
            f':bone:   *Yay! You have been assigned the role of bon toutou!*   :bone:'
            f'\n*This role will grant you 10% off items on the shop and 10% more earnings from every sources for 24 hours!*'
            )
    
    # COMMAND
    # claim daily command
    def daily_reward_success(author, amount, dialogue_ref: str = None):    
        print(Global_Log.command_run_without_exception('claim daily'))
        if dialogue_ref == "first_claim":
            return (
                f':partying_face:   **{author} is claiming his daily reward for the very first time!**'
                f'\n:coin:   *{author} got {amount} {global_dialogue_var.currency} from his daily reward!*'
                f'\n:arrow_right:   ` !claim daily ` *to get your own daily reward*'
                )
        elif dialogue_ref == "claim_success":
            return (
                f':calendar:   {author} has claim his daily reward!'
                f'\n:coin:   *{author} got {amount} {global_dialogue_var.currency} from his daily reward!*'
                f'\n:arrow_right:   ` !claim daily ` *to get your own daily reward*'
                )
        return (
            f'{dialogue_icon.fail}   Looks like you already claimed that reward today!'
            f'\n:calendar:   Come back tomorrow!'
            )
    # coinflip command
    def coinflip_success(amount: int, author, dialogue_ref: str):
        if dialogue_ref == "cf_init":
            return (
            f':coin: **{author}** is in a playful mood, {amount} {global_dialogue_var.currency} have been bet!'
            f'\n:arrow_right:Pick **HEAD** or **TAIL**'
            f'\n*You got to write it down, like with your keyboard...*'
            )
        print(Global_Log.command_run_without_exception('coinflip'))
        if dialogue_ref == "cf_win":
            return (
                f':+1:   Well played to **{author}** who won **{amount}** {global_dialogue_var.currency}   :confetti_ball:'
                f'\n*`!cf <amount>` to play again!*'
                )
        if dialogue_ref == "cf_lose":
            return (
                f':-1:   Congratulations! **{author}** lost **{amount}** {global_dialogue_var.currency}   :joy::ok_hand:'
                f'\n*`!cf <amount>` to play again!*'
                )

# ---------------------------------------------- # GRIND log # ---------------------------------------------- #
class Economy_Grind_Log:
    # return if target is mauvais toutou
    def target_is_mauvais_toutou(userID: discord.Member):
        return f'\t{log_format.FAIL} {userID} HAS BEEN SELECTED AS THE bon toutou BUT IS ALREADY mauvais toutou.{log_format.END} '
    # return if target is a bot
    def target_is_a_bot(userID: discord.Member):
        return f'\t{log_format.FAIL} {userID} HAS BEEN SELECTED AS THE bon toutou BUT IS A BOT.{log_format.END}'
    # return if target is not registered
    def target_is_not_registered(userID: discord.Member):
        return f'\t{log_format.FAIL} {userID} HAS BEEN SELECTED AS THE bon toutou BUT IS NOT REGISTERED.{log_format.END}'
    # return if target is not fomer bon toutou
    def target_is_former_bt(userID: discord.Member):
        return f'\t{log_format.FAIL} {userID} HAS BEEN SELECTED AS THE bon toutou BUT WAS THE PREVIOUS bon toutou.{log_format.END}'

# ---------------------------------------------- # GRIND error # ---------------------------------------------- #
class Economy_Grind_ErrorHandler:
    # coinflip_error
    def coinflip_error(error_type: str, userID: discord.Member):
        print(f'\t{log_format.FAIL} QUERRY coinflip HAS BEEN EXITED BY {userID}.{log_format.END}')
        if error_type == "fail_ans":
            return (
                f'{dialogue_icon.fail}   You failed answering a simple "head or tail" question, no doubt that\'s why your life sucks.'
                f'\n*`!cf <amount>` to try again.*'
                )
        elif error_type == "bad_arg":
            return (
                f'{dialogue_icon.fail}   Ohoh! Looks like you don\'t know what a fucking number is!'
                f'\n*`!cf <amount>`   --   <amount> being a number.*'
                )
        elif error_type == "missing_arg":
            return (
                f'{dialogue_icon.fail}   Ohoh! Looks like you forgot to specify the amount!'
                f'\n*`!cf <amount>`*'
                )