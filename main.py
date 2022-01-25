from asyncore import read
from discord.ext import commands
import discord
from datetime import datetime, timezone
import os


messages = []
TOKEN, GUILD = '', ''
bot = commands.Bot(command_prefix=';')

def write_to_log():
    now = datetime.now() # current date and time
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


def connect():
    try:
        client = discord.Client()

        @client.event
        async def on_ready():
            print(f'{client.user} has connected to Discord!')
        client.run(TOKEN)
        log(f'Successfully connected to Discord with User: {client.user}')

    except:
        raise Exception('Error in creating a discord client')


if __name__ == '__main__':
    try:
        read_token()
        connect()

        @bot.command(name='dm')
        async def dm(carrier):
            await carrier.create_dm()
            message = 'Facts'
            await carrier.dm_channel.send(message)

        bot.run(TOKEN)
    except Exception as e:
        log(e, 'Run failed')
        print(f'\n\ne\n\n')
    finally:
        write_to_log()
        exit(0)
