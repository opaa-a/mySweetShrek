import discord
import json
import random
from cogs.economy import Economy_Reward
from dialogue.global_dialogue import *
from discord.ext import tasks, commands


#---------------------------------------------------------------------------------------#        TASKS       #---------------------------------------------------------------------------------------#

class Bon_Toutou_Task(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.bon_toutou_assign.start()
        print(f'\n{log_format.INFO}- Bon Toutou Background Task from background_tasks.py is loaded.{log_format.END}')

    @tasks.loop(hours=24)
    async def bon_toutou_assign(self):
        from cogs.economy import Economy_Grind
        guild = self.client.get_guild(774048252848111636)
        guild_member_list = []
        for member in guild.members:
            guild_member_list.append(member)

        random_userID = random.choice(guild_member_list)
        print(f'{log_format.INFO} BON TOUTOU HAS ASIGN {random_userID}.{log_format.END}')
        return await Economy_Grind.bon_toutou(self, random_userID)

class Who_Is_Vocal(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.who_is_vocal.start()
        print(f'\n{log_format.INFO}- Who is Vocal from background_tasks.py is loaded.{log_format.END}')

    @tasks.loop(seconds=30)
    async def who_is_vocal(self):
        guild = self.client.get_guild(774048252848111636)
        user_on_vocal = []
        for voice_channel in guild.voice_channels:
            for i in voice_channel.voice_states:
                userID = self.client.get_user(i)
                user_on_vocal.append(userID)
        return Economy_Reward.who_is_vocal(user_on_vocal)

def setup(client):
    client.add_cog(Bon_Toutou_Task(client))
    client.add_cog(Who_Is_Vocal(client))