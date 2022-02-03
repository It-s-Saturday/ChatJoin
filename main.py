
from discord.ext import commands
import discord
from datetime import datetime, timezone
import os
import time
from mongo_files.DataObj import DataObj
from mongo_files.Connect_Cluster import *
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

        client = discord.Client()
        bot = commands.Bot(command_prefix='!')

        @bot.command(name='dm')
        async def DM(ctx, message=None):
            user = ctx.message.author
            message = message or "Success"
            await user.send(f"{message}")
            log(f'{message} -> {user}')

        """
        - Add command to designate which channel the bot should watch (server-wide)
        - Add listener onto said channel 
        - On join event, grab x_member
            - Cycle y_members in x_member.notify
            - Send dm to each y_member 
        
        - Add command in format !notifyme discorduser
            - add invoker to discorduser's notify attribute

        1) User designates channel
        2) Add listener to channel
        3) on user join, cycle list and notify each
        """

        bot.run(TOKEN)

    except Exception as e:
        log(e, 'Run failed')
        print(f'\n\n{e}\n\n')
    finally:
        write_to_log()
        exit(0)
