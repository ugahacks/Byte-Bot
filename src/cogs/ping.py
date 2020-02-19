import discord
import datetime
from discord.ext import commands

class Ping(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(':ping_pong: Pong! {0} ms'.format(round(self.client.latency * 1000)))

def setup(client):
    client.add_cog(Ping(client))
