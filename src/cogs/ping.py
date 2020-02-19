import discord
import datetime
from discord.ext import commands, tasks
import urllib.request

class Ping(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(':ping_pong: Pong! {0} ms'.format(round(self.client.latency * 1000)))

    @tasks.loop(minutes=1.0)
    async def ping_ugahacks(self):
        code = urllib.request.urlopen('https://ugahacks.com').getcode()
        if(code != 200):
            message_embed = discord.Embed(timestamp = datetime.datetime.now(), color=discord.Colour.red())
            message_embed.add_field(name='URGENT: Website may be down', value = f'@here UGAHacks status checker has detected that the website may be down. \n Use `-pause-ping` to pause the pings. Please turn it back on with `-resume-ping` when the problem is resolved.')
            await self.client.get_channel(self.LOG_CHANNEL).send(embed=message_embed)

    @ping_ugahacks.before_loop
    async def before_get_emails(self):
        print('waiting...')
        await self.client.wait_until_ready()

    @commands.command(name='pause-ping')
    async def pause_ping(self, ctx):
        self.ping_ugahacks.stop()
        await ctx.send('Server status pings have been paused. It will take up to a minute for the ping to fully stop')

    @commands.command(name='resume-ping')
    async def resume_ping(self, ctx):
        try:
            self.ping_ugahacks.start()
            await ctx.send('Server status pinging has been resumed.')
        except:
            await ctx.send('Server status pinging is already running.')

    @commands.command(name='ping-ugahacks')
    async def manual_ping_ugahacks(self, ctx):
        code = urllib.request.urlopen('https://ugahacks.com').getcode()
        await ctx.send(f'Return Code: {code}')

def setup(client):
    client.add_cog(Ping(client))
