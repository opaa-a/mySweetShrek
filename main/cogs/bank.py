import discord
from discord.ext import commands
from vault import *

class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client
        print(f"\n- Economy from bank is loaded.")

    