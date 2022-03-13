
import asyncio
import os
import time
import traceback
from datetime import datetime, timezone

import discord
from discord.ext import commands

from mongo_files.Connect_Cluster import *
from mongo_files.DataObj import DataObj
from mongo_files.Dictionarify import dictionarify
from mongo_files.User import *

messages = []
TOKEN, GUILD = '', ''
client = None


def write_to_log():
    now = datetime.now()  # current date and time
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    time = now.strftime("%H:%M:%S")
    date_time = now.strftime("%m_%d_%Y-%H_%M_%S")
    try:
        log_path = './logs/'
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        with open(f'{log_path}{date_time}.txt', 'w') as f:
            for message in messages:
                f.write(f'{message}\n')
        log(f'Successfully wrote to {date_time}')
    except:
        raise Exception(f'Error writing to {log_path}{date_time}.txt')


def log(message, comment=''):
    now = datetime.now(timezone.utc)
    time = now.strftime("%H:%M:%S")
    messages.append(
        f'[{time}]\t-\t{f"[{comment}] " if comment else ""}{message}')


def read_token():
    global TOKEN, GUILD
    try:
        filename = './token'
        with open('token', 'r') as f:
            TOKEN, GUILD = f.readlines()
        f.close()
        log(f'Successfully read tokens from {filename}')
    except:
        raise Exception(f'Error opening {filename}')


if __name__ == '__main__':
    try:
        read_token()

        intents = discord.Intents.default()
        print(intents)
        intents.members = True
        print(intents.members)

        bot = commands.Bot(command_prefix='!', intents=intents)

        print(f'{bot} succesfully initialized')


        @bot.event
        async def on_voice_state_update(member, before, after):
            print(member)
            print(before.channel, after.channel)
            if not before.channel and after.channel:
                await member.send(content="hey there")

        @bot.command(name='notifyme')
        async def DM(ctx):
            member = ctx.message.author

            if ctx.message.mentions:
                print(f'ctx.message = {ctx.message.content}')
                target = ctx.message.mentions[0]
                command, member_object = ctx.message.content.split()
                member_id = int(member_object.strip('<@!>'))
                print(f'add {member.id} to {member_id}')

                await member.send(content=f'Added you to {target}\'s list!')

        @bot.command(name='removeme')
        async def DM(ctx):
            member = ctx.message.author

            if ctx.message.mentions:
                print(f'ctx.message = {ctx.message.content}')
                target = ctx.message.mentions[0]
                command, member_object = ctx.message.content.split()
                member_id = int(member_object.strip('<@!>'))
                print(f'remove {member.id} from {member_id}')

                await member.send(content=f'Removed you from {target}\'s list!')

        bot.run(TOKEN)

    except Exception as e:
        log(e, 'Run failed')
        print(f'\n\n{traceback.format_exc()}\n\n')
    finally:
        write_to_log()
        exit(0)
