import discord
import random
import json
from discord.ext import tasks, commands

class Bon_Toutou_Task(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.bon_toutou_assign.start()
        print(f'\n- Bon Toutou Background Task from background_tasks.py is loaded.')

    @tasks.loop(hours=24)
    async def bon_toutou_assign(self):
        from cogs.economy import Economy_Grind
        guild = self.client.get_guild(774048252848111636)
        guild_member_list = []
        for member in guild.members:
            guild_member_list.append(member)

        random_userID = random.choice(guild_member_list)
        print(f'\n# BON TOUTOU -- {random_userID} is selected')
        return await Economy_Grind.bon_toutou(self, random_userID)


def setup(client):
    client.add_cog(Bon_Toutou_Task(client))