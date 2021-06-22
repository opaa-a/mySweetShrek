import discord
from dialogue.global_dialogue import *

class Item_Dialogue:
    # FUNCTION
    # item_a_la_niche function
    def item_a_la_niche_success(dialogue_ref: str, target: discord.Member):
        print(f'\t{log_format.FAIL} COMMAND use FAILED - DUE TO THE FOLLOWING ERROR: {dialogue_ref}.{log_format.END}')    
        if dialogue_ref == "target_already_in_chan":
            return (
                f'{dialogue_icon.fail}   Nope, **{target}** is already in ` \'La Niche\' `. Don\'t waste your item.'
                )
        if dialogue_ref == "target_not_connected":
            return (
                f'{dialogue_icon.fail}   Ohoh! You can\'t use this command if the target is not connected to a vocal channel.'
            )
        if dialogue_ref == "target_is_bot":
            return (
                f'{dialogue_icon.fail}   No no no, you can\'t use this command on bots!'
            )
    # item_shush function
    def item_shush_success(dialogue_ref: str, target: discord.Member):
        print(f'\t{log_format.FAIL} COMMAND use FAILED - DUE TO THE FOLLOWING ERROR: {dialogue_ref}.{log_format.END}')
        if dialogue_ref == "target_is_already_muted":
            return (
                f'{dialogue_icon.fail}   Nope, **{target}** is already muted!'
                )
        if dialogue_ref == "target_not_connected":
            return (
                f'{dialogue_icon.fail}   Ohoh! You can\'t use this command if the target is not connected to a vocal channel.'
                )
        if dialogue_ref == "target_is_bot":
            return (
                f'{dialogue_icon.fail}   No no no, you can\'t use this command on bots!'
            )
    # item_mauvais_toutou function
    def item_mauvais_toutou(dialogue_ref: str, target: discord.Member):
        print(f'\t{log_format.FAIL} COMMAND use FAILED - DUE TO THE FOLLOWING ERROR: {dialogue_ref}.{log_format.END}')
        if dialogue_ref == "target_already_has_role":
            return (
                f'{dialogue_icon.fail}   Nope, **{target}** is already \'Mauvais toutou\'!'
                )
        if dialogue_ref == "target_is_not_registered":
            return (
                f'{dialogue_icon.fail}   Ohoh! Looks like **{target}** is not registered to the vault. You can\'t target users that are not in the vault.'
                )
        if dialogue_ref == "target_is_bot":
            return (
                f'{dialogue_icon.fail}   No no no, you can\'t use this command on bots!'
                )