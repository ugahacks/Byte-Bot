import discord
from discord.ext import commands, tasks
import imaplib
import email
from ..util.EmailUtil import EmailType, get_mail, EmailType
import datetime

class Emails(commands.Cog):

    EMAIL_CHANNEL = 676171302712901654
    LOG_CHANNEL = 676524139732795403

    def __init__(self, client):
        self.client = client
        self.get_emails.start()

    @tasks.loop(seconds=5.0)
    async def get_emails(self):
        mail_list = get_mail()
        for email in mail_list:
            if(email['type'] == EmailType.EMAIL):
                message_embed = discord.Embed(timestamp = datetime.datetime.now(), color=discord.Colour.red())
                message_embed.add_field(name='New Email!', value=f'**From:** {email["email_from"]} \n **Subject:** {email["subject"]} \n **Recieved by:** {email["email_to"]}')
                await self.client.get_channel(self.EMAIL_CHANNEL).send(embed=message_embed)
            elif(email['type'] == EmailType.TEXT):
                message_embed = discord.Embed(timestamp = datetime.datetime.now(), color=discord.Colour.red())
                message_embed.add_field(name='New Text Message!', value = f'**From:** {email["email_from"]} \n **Subject:** {email["subject"]} \n **Email Content:** {email["email_body"]} \n **Recieved by:** {email["email_to"]}')
                await self.client.get_channel(self.EMAIL_CHANNEL).send(embed=message_embed)
            elif(email['type'] == EmailType.ERROR):
                message_embed = discord.Embed(timestamp = datetime.datetime.now(), color=discord.Colour.red())
                message_embed.add_field(name='uh oh ERROR!!', value = f'{email["subject"]} \n {email["email_body"]}')
                await self.client.get_channel(self.LOG_CHANNEL).send(embed=message_embed)

    @get_emails.before_loop
    async def before_get_emails(self):
        print('waiting...')
        await self.client.wait_until_ready()

    @commands.command()
    async def check(self, ctx):
        mail_list = get_mail()
        await ctx.send(f'I have found {len(mail_list)} unread email(s)!!')
        for email in mail_list:
            if(email['type'] == EmailType.EMAIL):
                message_embed = discord.Embed(timestamp = datetime.datetime.now(), color=discord.Colour.red())
                message_embed.add_field(name='New Email!', value=f'From: {email["email_from"]} \n Subject: {email["subject"]} \n Recieved by: {email["email_to"]}')
                await self.client.get_channel(self.EMAIL_CHANNEL).send(embed=message_embed)
            elif(email['type'] == EmailType.TEXT):
                message_embed = discord.Embed(timestamp = datetime.datetime.now(), color=discord.Colour.red())
                message_embed.add_field(name='New Text Message!', value = f'From: {email["email_from"]} \n Subject: {email["subject"]} \n Email Content: {email["email_body"]} \n Recieved by: {email["email_to"]}')
                await self.client.get_channel(self.EMAIL_CHANNEL).send(embed=message_embed)
            elif(email['type'] == EmailType.ERROR):
                message_embed = discord.Embed(timestamp = datetime.datetime.now(), color=discord.Colour.red())
                message_embed.add_field(name='uh oh ERROR!!', value = f'{email["subject"]} \n {email["email_body"]}')
                await self.client.get_channel(self.LOG_CHANNEL).send(embed=message_embed)

def setup(client):
    client.add_cog(Emails(client))
