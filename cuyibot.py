# -*- coding: utf-8 -*-
'''
Created on 04.04.2021
Version 1.0.0 (04.04.21)
@author: Creki
'''

import discord
from discord.ext import commands
import os
from pathlib import Path
from dotenv import load_dotenv

#loading .env
load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

#bot settings
intents = discord.Intents.default()
intents.members = True
cuyibot = commands.Bot(command_prefix = 'c!', intents=intents)

#Constants
BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_CHANNEL_ID = int(os.getenv('BOT_CHANNEL_ID'))
ADMIN_ID = int(os.getenv('ADMIN_ID'))


#Bot doing things
@cuyibot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(cuyibot))
    

@cuyibot.command()
async def modifyroles(ctx, *args):
    if ctx.message.channel.id == BOT_CHANNEL_ID:
        if ctx.author.id == ADMIN_ID:
            if len(args) == 2:
                if args[0].lower() == 'add':
                    already_in_list = False
                    with open('roles.txt', 'r') as roles_file:
                        lines = roles_file.readlines()
                        for line in lines:
                            if line.strip("\n") == args[1]:
                                already_in_list = True
                    if already_in_list == False:
                        with open('roles.txt', 'a') as roles_file:
                            roles_file.write('\n')
                            roles_file.write(args[1])
                        await ctx.send('Role added to the list. Make sure the Role is available on the Server!')
                    else:
                        await ctx.send('Role is already available.')
                    
                elif args[0].lower() == 'remove':
                    with open('roles.txt', 'r') as roles_file:
                        lines = roles_file.readlines()
                    with open('roles.txt', 'w') as roles_file:
                        for line in lines:
                            if line.strip("\n") != args[1]:
                                roles_file.write(line)
                else:
                    await ctx.send('Please use \'add \"role\"\' or \'remove \"role\"\' to add/remove Roles. Please make sure to also add them to the Server via Server settings.')
            else:
                await ctx.send('Please use \'add \"role\"\' or \'remove \"role\"\' to add/remove Roles. Please make sure to also add them to the Server via Server settings.')
        else:
            await ctx.send('Not authorized to change Role List')
    
@cuyibot.command()
async def addrole(ctx, *args):
    if ctx.message.channel.id == BOT_CHANNEL_ID:
        if len(args) == 1:
            available = 0
            with open('roles.txt', 'r') as roles_file:
                lines = roles_file.readlines()
                for line in lines:
                    if line.strip("\n") == args[0]:
                        available = 1
            if available == 1:
                guild = discord.utils.find(lambda g: g.id == ctx.guild.id, cuyibot.guilds)
                role = discord.utils.get(guild.roles, name=args[0])
                if (role is not None):
                    await ctx.author.add_roles(role)
                    await ctx.send('Role {} added'.format(args[0]))
            else:
                await ctx.send('Role not available.')
        else:
            await ctx.send('Please choose a role.')
            
@cuyibot.command()
async def removerole(ctx, *args):
    if ctx.message.channel.id == BOT_CHANNEL_ID:
        if len(args) == 1:
            available = False
            with open('roles.txt', 'r') as roles_file:
                lines = roles_file.readlines()
                for line in lines:
                    if line.strip("\n") == args[0]:
                        available = True
            if available == True:
                guild = discord.utils.find(lambda g: g.id == ctx.guild.id, cuyibot.guilds)
                role = discord.utils.get(guild.roles, name=args[0])
                if (role is not None):
                    await ctx.author.remove_roles(role)
                    await ctx.send('Role {} removed'.format(args[0]))
            else:
                await ctx.send('Role not available.')
        else:
            await ctx.send('Please choose a role.')
            
@cuyibot.command()
async def listroles(ctx):
    if ctx.message.channel.id != BOT_CHANNEL_ID:
        return
    
    embed = discord.Embed(title="Available Roles", color=0xff5d50)
    with open("roles.txt", "r") as roles_file:       
        lines = roles_file.readlines()
        values = ''
        for line in lines:
            values = values + line
        if values != '':
            embed.add_field(name='Roles', value=values, inline=True)
    await ctx.send(embed=embed)

@cuyibot.command()
async def cuyihelp(ctx):
    if ctx.message.channel.id != BOT_CHANNEL_ID:
        return
    embed = discord.Embed(title="Available Commands", color=0xff5d50)
    embed.set_thumbnail(url=cuyibot.user.avatar_url)
    embed.add_field(name='c!modifyroles', value='To add/remove Roles to the Bot. Only available for Admin', inline=True)
    embed.add_field(name='c!listroles', value='List all available roles', inline=False)
    embed.add_field(name='c!addrole', value='Add role', inline=False)
    embed.add_field(name='c!removerole', value='Remove role', inline=False)
    await ctx.send(embed=embed)
    
@cuyibot.event
async def on_message(message):
    if message.author == cuyibot.user:
        return
                
    await cuyibot.process_commands(message)  #to activate commands for messages

cuyibot.run(BOT_TOKEN)


