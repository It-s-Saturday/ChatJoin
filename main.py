import os
import traceback
from datetime import datetime, timezone

import discord
from discord.ext import commands

from mongo_files.Connect_Cluster import *
from notify import Notify

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
            print(before.channel, after.channel)
            if not before.channel and after.channel:
                member_ids = {member.id for member in after.channel.members} # a set containing the ids of everyone in the channel
                instance = Notify(member.id, member.guild.id)
                server_name = member.guild.name
                channel_name = after.channel
                for user in instance.get_targets():
                    # if user is already in channel, then continue
                    if int(user) in member_ids:
                        continue
                    user_object = await bot.fetch_user(int(user))
                    await user_object.send(content=f'{member} joined channel {channel_name} in server {server_name}!')

        @bot.command(name='notifyme')
        async def DM(ctx):
            caller = ctx.message.author
    
            if ctx.message.mentions:
                print(f'ctx.message = {ctx.message.content}')
                target = ctx.message.mentions[0]
                message_content = ctx.message.content.split()

                # if message_content > 2 then use third arg as guild_id
                if len(message_content) == 3:
                    command, target_object, guild = message_content
                elif len(message_content) == 2:
                    command, target_object = message_content
                    guild = str(ctx.message.guild.id)

                target_id = int(target_object.strip('<@!>'))
                print(f'add {caller.id} to {target_id}')

                client = Connect_Cluster(guild)
                client.add_user_to_target(caller.id, target_id)
                client.cluster.close()

                await caller.send(content=f'Added you to {target}\'s list!')

        @bot.command(name='removeme')
        async def DM(ctx):
            caller = ctx.message.author

            if ctx.message.mentions:
                print(f'ctx.message = {ctx.message.content}')
                target = ctx.message.mentions[0]
                command, target_object = ctx.message.content.split()
                target_id = int(target_object.strip('<@!>'))
                print(f'remove {caller.id} from {target_id}')

                client = Connect_Cluster(str(ctx.message.guild.id))
                client.remove_user_from_target(str(caller.id), str(target_id))
                client.cluster.close()

                await caller.send(content=f'Removed you from {target}\'s list!')

        bot.run(TOKEN)

    except Exception as e:
        log(e, 'Run failed')
        print(f'\n\n{traceback.format_exc()}\n\n')

    finally:
        write_to_log()
        exit(0)
