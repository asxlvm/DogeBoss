import asyncio
import datetime
import inspect
import json
import locale
import os
import random
import re
import string
import subprocess
import time
from datetime import datetime

import aiohttp
import dogehouse
import requests
from bs4 import BeautifulSoup
from covid import Covid
from dogehouse import DogeClient, command, event
from dogehouse.entities import BaseUser, Context, Message, User, UserPreview

from keep_alive import keep_alive

DOGETOKEN = os.getenv('DOGEHOUSE_TOKEN')
DOGEREFRESHTOKEN = os.getenv('DOGEHOUSE_REFRESH_TOKEN')
ownerid = "de27447e-a633-484d-afaa-8377887dda7b"
launch_time = datetime.utcnow()  # this is for the uptime command
print(launch_time)


class Client(DogeClient):
    @event
    async def on_ready(self):
        try:
            keep_alive()
            print("Keep Alive initiated")
            print(f"Successfully connected as {self.user}")
            await self.join_room("87d9cc48-370f-47e7-9d15-6449557cfcf2")
        except Exception as e:
            print(e)

    async def bot_info_get(self):
        with open("botinfo.json", "r") as f:
            botinfo = json.load(f)
        return botinfo

    @command
    async def botinfo(self, ctx: Context):
        await self.send(dogehouse.__version__)

    @event
    async def on_room_join(self, _):
        botinfogotten = await self.bot_info_get()
        botinfogotten["botinfo"] = {}
        botinfogotten["botinfo"]["botroomurl"] = f"https://dogehouse.tv/room/{self.room.id}"
        botinfogotten["botinfo"]["botroomname"] = f"{self.room.name}"
        botinfogotten["botinfo"]["botroomcount"] = f"{self.room.count}"
        botinfogotten["botinfo"]["botroomdescription"] = f"{self.room.description}"

        with open("botinfo.json", "w") as f:
            json.dump(botinfogotten, f)

    @command
    async def setstar(self, ctx: Message):
        """Sets a message to be 'starred'. The current starred message can be accessed using the 'starred' command."""
        global msg  # making the variables global so we can access them from any command
        global msgauthor
        global starred
        global starredauthor
        starred = msg
        starredauthor = msgauthor
        await self.send(f"Starred message was set! You may access it with {self.prefix}starred")

    @command
    async def starred(self, ctx: Message):
        """Reads the current starred message"""
        global starred
        global starredauthor
        await self.send(
            f"Starred Message: {starred}ㅤ|ㅤMessage Creator: @{starredauthor}")

    @command
    async def owoify(self, ctx: Message, *, owome: str = None):
        """OwO-ifies a string"""
        if owome == None:
            return await self.send(f"{ctx.author.mention} Missing Required Argument - Usage: {self.prefix}owoify <message> • Example: {self.prefix}owoify dont hurt me!")
        else:
            owome = owome.replace("r", "w")
            owome = owome.replace("l", "w")
            owome = owome.replace("g", "w")
            owome = owome.replace("R", "W")
            owome = owome.replace("L", "W")
            owome = owome.replace("G", "W")
            owome = owome.replace("ove", "uv")

            replacing_words = 'aeiou'
            upperreplacing_words = 'AEIOU'
            replacewithuwu = '!?/_.+'

            uwufaces = [
                "ᓀ˵▾˵ᓂ", ">_<", "＾▽＾", "❛ ᴗ ❛", "UwU", "OwO", "QwQ", "≧▽≦"
            ]
            for i in owome:
                if i in replacewithuwu:
                    owo_final = owome.replace(i, random.choice(uwufaces))

            for i in owome:
                if i in upperreplacing_words:
                    owo_final = owome.replace(i, f"Y{i}")

            for i in owome:
                if i in replacing_words:
                    owo_final = owome.replace(i, f"y{i}")

            await self.send(f"{owo_final}ㅤㅤ• {ctx.author.mention}")

    @command
    async def github(self, ctx: Message):
        await self.send(f"{ctx.author.mention} I'm open-source! You can look at my source code here! https://github.com/asxlvm/DogeBoss :GitHub:")

    @command
    async def battle(self, ctx: Context, *, user: BaseUser):
        """Starts a battle with the user you mentioned :hyperHammer:"""
        currenthpauth = 100
        moves = 0
        currenthpuser = 100
        players = []
        if players != [] or currenthpuser != 100 or currenthpauth != 100 or moves != 0:
            return await self.send(f"{ctx.author.mention} a game is going on right now, you may not start another one.", whisper=[ctx.author.id])
        if user == None:
            return await self.send(message=f"{ctx.author.mention} Missing Required Argument - Usage: d!battle <user> • Example: d!fight @hudson", whisper=[ctx.author.id])
        if user.id == ctx.author.id:
            return await self.send(message=f"{ctx.author.mention} Bad Argument (You cannot battle yourself) - Usage: d!battle <user> • Example: d!fight @hudson", whisper=[ctx.author.id])
        else:
            try:
                users = await self.get_settings_data()
                fightDecline = users[str(user.id)]["autoRejectFights"]
                if fightDecline == True:
                    await self.send(f"{ctx.author.mention} you can't fight that user as he has enabled autoRejectFights.", whisper=[ctx.author.id])
                    return False
            except Exception as e:
                return print(e)
            await self.send(f"{user.mention} do you accept {ctx.author.mention} 's fight request? OPTIONS: Yes / No", whisper=[user.id])
            adwaitfor = await self.wait_for('message', check=lambda message: message.author.id == user.id)
            if adwaitfor.content.lower() == "yes":
                await asyncio.sleep(2)
                await self.send(f"{user.mention} has accepted the fight request, 3, 2, 1, FIGHT!", whisper=[ctx.author.id, user.id])
                await asyncio.sleep(2)
                True
            elif adwaitfor.content.lower() == "no":
                await asyncio.sleep(2)
                await self.send(f"{user.mention} has declined the fight request.", whisper=[ctx.author.id])
                return False
            print("true")
            m_author_id = ctx.author.id
            m_user_id = user.id
            m_author_mention = ctx.author.mention
            m_user_mention = user.mention
            turn = random.choice([m_author_id, m_user_id])
            players = [m_author_id, m_user_id]
            print(m_author_id)
            print(m_user_id)
            print(turn)
            print(players)
            print(moves)
            try:
                while True:
                    if turn == m_author_id:
                        currentturnid = m_author_id
                        currentturnmention = m_author_mention
                        currentturnhp = currenthpauth
                        notturnid = m_user_id
                        notturnmention = m_user_mention
                        notturnhp = currenthpuser
                    else:
                        currentturnid = m_user_id
                        currentturnmention = m_user_mention
                        currentturnhp = currenthpuser
                        notturnid = m_author_id
                        notturnmention = m_author_mention
                        notturnhp = currenthpauth
                    print(currentturnmention)
                    print(notturnmention)
                    await asyncio.sleep(2)
                    currentturnlist = [currentturnid]
                    if currenthpauth <= 0 or currenthpuser <= 0:
                        if currenthpauth > currenthpuser:
                            await self.send(f"{m_author_mention} has won against {m_user_mention} in {moves} moves! His remaining HP was {currenthpauth} HP.")
                            players = []
                            moves = 0
                            currenthpuser = 100
                            currenthpauth = 100
                            return False
                        elif currenthpuser > currenthpauth:
                            await self.send(f"{m_user_mention} has won against {m_author_mention} in {moves} moves! His remaining HP was {currenthpuser} HP.")
                            players = []
                            moves = 0
                            currenthpuser = 100
                            currenthpauth = 100
                            return False
                    await self.send(f"{currentturnmention}, what will you do now? • OPTIONS: Fight, Defense, Surrender • Your HP: {currentturnhp} HP, Your opponent's HP: {notturnhp} HP", whisper=currentturnlist)
                    msg = await self.wait_for(event='message', check=lambda message: message.author.id == currentturnid, timeout=30)

                    msgcont = msg.content.lower()
                    if msgcont == 'fight':
                        damage = random.randint(1, 35)
                        if damage == 35:
                            damage = random.randint(35, 75)
                            dmgtext = f"{currentturnmention} made a critical hit of {damage} HP! :Pog:"
                        else:
                            dmgtext = f"{currentturnmention} chose violence. Damage of {damage} HP was given to {notturnmention}!"
                        notturnhp = notturnhp - damage
                        await self.send(message=dmgtext, whisper=players)
                        moves += 1
                        if turn == m_author_id:
                            currenthpauth = currentturnhp
                            currenthpuser = notturnhp
                            turn = m_user_id
                            True
                        else:
                            currenthpuser = currentturnhp
                            currenthpauth = notturnhp
                            turn = m_author_id
                            True

                    elif msgcont == 'defense':
                        healedhp = random.randint(5, 20)
                        currentturnhp += healedhp
                        if currentturnhp >= 100:
                            currentturnhp = 100
                        deftext = f"{currentturnmention} healed himself for {healedhp} HP!"
                        await self.send(message=deftext, whisper=players)
                        if turn == m_author_id:
                            currenthpauth = currentturnhp
                            currenthpuser = notturnhp
                            turn = m_user_id
                            True
                        else:
                            currenthpuser = currentturnhp
                            currenthpauth = notturnhp
                            turn = m_author_id
                            True
                    elif msgcont == 'surrender':
                        await self.send(message=f"{currentturnmention} surrendered S :OMEGALUL:  BAD", whisper=players)
                        moves = 0
                        players = []
                        currenthpauth = 100
                        currenthpuser = 100
                        return False

            except asyncio.TimeoutError:
                await self.send(f"{currentturnmention} did not respond in 30 seconds, fight ended.", whisper=players)
                players = []
                currenthpauth = 100
                currenthpuser = 100
                moves = 0
                return False

    @command
    async def waitfor(self, ctx: Message):
        waitedmsg = await self.wait_for(
            event='message',
            timeout=10,
            check=lambda message: message.author.id == ctx.author.id)
        await self.send(f"{waitedmsg.content}")

    def is_owner(self, authorid):
        if authorid == ownerid:
            return True
        if authorid != ownerid:
            return False

    @command
    async def evaluate(self, ctx: Context, *, evalThis):
        ownercheck = self.is_owner(ctx.author.id)
        if ownercheck == False:
            return await self.send('Owner-Only Command', whisper=[ctx.author.id])
        res = eval(evalThis)
        if inspect.isawaitable(res):
            await self.send(await res, whisper=[ctx.author.id])
        else:
            await self.send(res, whisper=[ctx.author.id])

    @command
    async def shell(self, ctx: Context, *, shellCmd):
        ownercheck = self.is_owner(ctx.author.id)
        if ownercheck == False:
            return await self.send('Owner-Only Command', whisper=[ctx.author.id])
        proc = subprocess.Popen(shellCmd, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        stdout_value = proc.stdout.read() + proc.stderr.read()
        realval = str(stdout_value).replace("\n", " ")
        await self.send(f"{realval}", whisper=[ctx.author.id])

    @command
    async def reboot(self, ctx: Message):
        if ctx.author.id == ownerid:
            is_owner = True
        else:
            is_owner = False

        if is_owner == True:
            await self.send("Rebooting the bot, I'll be back in 5 seconds!")
            await self.close()
            await asyncio.sleep(4)
            client = DogeClient(DOGETOKEN,
                                DOGEREFRESHTOKEN,
                                prefix="{self.prefix}",
                                reconnect_voice=True)
            client.run()
            await asyncio.sleep(1)
            await self.send("I'm back online")
        else:
            return await self.send(
                f"{ctx.author.mention} You are not the owner of the bot so you may not reboot it!"
            )

    async def open_settings(self, userid, username):
        users = await self.get_settings_data()
        if str(userid) in users:
            usernamedata = users[str(userid)]["username"]
            if usernamedata != username:
                users[str(userid)]["username"] = username
                with open("settings.json", "w") as f:
                    json.dump(users, f)
            return False
        else:
            users[str(userid)] = {}
            users[str(userid)]["allowMentions"] = True
            users[str(userid)]["autoRejectFights"] = False
            users[str(userid)]["passiveMode"] = False
            users[str(userid)]["lastPassive"] = "2020-03-31 08:48:57.747975"
            users[str(userid)]["whisperEconomy"] = True
            users[str(userid)]["onJoinMsg"] = True
            users[str(userid)]["allowUserInteraction"] = True
            users[str(userid)]["username"] = username
        with open("settings.json", "w") as f:
            json.dump(users, f)
        return True

    async def get_settings_data(self):
        with open("settings.json", "r") as f:
            users = json.load(f)
        return users

    @command
    async def settings(self, ctx: Context):
        """Shows your current settings"""
        try:
            await self.open_settings(ctx.author.id, ctx.author.username)
            userid = ctx.author.id
            users = await self.get_settings_data()
            allowMentions = users[str(userid)]["allowMentions"]
            autoRejectFights = users[str(userid)]["autoRejectFights"]
            passiveMode = users[str(userid)]["passiveMode"]
            allowUserInteraction = users[str(userid)]["allowUserInteraction"]
            whisperEconomy = users[str(userid)]["whisperEconomy"]
            onJoinMsg = users[str(userid)]["onJoinMsg"]
            lastPassive = users[str(userid)]["lastPassive"]
            await self.send(f"Your settings:ㅤㅤAllow Mentions: {allowMentions} (If False, the bot will say your username instead of mentioning you) • Auto-Reject Fights: {autoRejectFights} (If True, you can't accept fight requests as it will decline them automatically) • Passive Mode: {passiveMode} (If True, you can't rob/deposit/withdraw with economy but you also can't get robbed) • Allow User Interaction: {allowUserInteraction} (If True, users can't get information for you, ex. {self.prefix}balance, {self.prefix}stats, {self.prefix}userinfo etc.)", whisper=[ctx.author.id])
        except Exception as e:
            print(e)

    @command
    async def change(self, ctx: Context):
        """Changes your settings"""
        await self.send(f"If you wish to see your settings, go on our site: https://asxlvm.github.io/#/settings • If you already saw your settings and wish to change them. What do you want to change?", whisper=[ctx.author.id])
        await asyncio.sleep(2)
        await self.send(f"Options: allowMentions [bool] • autoRejectFights [bool] • passiveMode [bool] • whisperEconomy [bool]• onJoinMsg [bool] • allowUserInteraction [bool] | [bool] = True / False", whisper=[ctx.author.id])
        waitforevent = await self.wait_for('message', check=lambda message: ctx.author.id == message.author.id)
        wfcl = waitforevent.content.lower()
        users = await self.get_settings_data()
        userid = ctx.author.id
        if wfcl == "allowmentions true":
            await self.open_settings(userid, ctx.author.username)
            users[str(userid)]["allowMentions"] = True
            with open("settings.json", "w") as f:
                json.dump(users, f)
            await asyncio.sleep(2)
            return await self.send(f"{ctx.author.mention} I have changed allowMentions to True for you.", whisper=[ctx.author.id])
        elif wfcl == "allowmentions false":
            await self.open_settings(userid, ctx.author.username)
            users[str(userid)]["allowMentions"] = False
            with open("settings.json", "w") as f:
                json.dump(users, f)
            await asyncio.sleep(2)
            return await self.send(f"{ctx.author.mention} I have changed allowMentions to False for you.", whisper=[ctx.author.id])
        elif wfcl == "autorejectfights true":
            await self.open_settings(userid, ctx.author.username)
            users[str(userid)]["autoRejectFights"] = True
            with open("settings.json", "w") as f:
                json.dump(users, f)
            await asyncio.sleep(2)
            return await self.send(f"{ctx.author.mention} I have changed autoRejectFights to True for you.", whisper=[ctx.author.id])
        elif wfcl == "autorejectfights false":
            await self.open_settings(userid, ctx.author.username)
            users[str(userid)]["autoRejectFights"] = False
            with open("settings.json", "w") as f:
                json.dump(users, f)
            await asyncio.sleep(2)
            return await self.send(f"{ctx.author.mention} I have changed autoRejectFights to False for you.", whisper=[ctx.author.id])
        elif wfcl == "passivemode true":
            await asyncio.sleep(2)
            return await self.send(f"{ctx.author.mention} as there isn't economy right now, you may not change this setting.", whisper=[ctx.author.id])
        elif wfcl == "passivemode false":
            await asyncio.sleep(2)
            return await self.send(f"{ctx.author.mention} as there isn't economy right now, you may not change this setting.", whisper=[ctx.author.id])
        elif wfcl == "whispereconomy true":
            await asyncio.sleep(2)
            return await self.send(f"{ctx.author.mention} as there isn't economy right now, you may not change this setting.")
        elif wfcl == "whispereconomy false":
            await asyncio.sleep(2)
            return await self.send(f"{ctx.author.mention} as there isn't economy right now, you may not change this setting.")
        elif wfcl == "onjoinmsg true":
            await self.open_settings(userid, ctx.author.username)
            users[str(userid)]["onJoinMsg"] = True
            with open("settings.json", "w") as f:
                json.dump(users, f)
            await asyncio.sleep(2)
            return await self.send(f"{ctx.author.mention} I have changed onJoinMsg to True for you.", whisper=[ctx.author.id])
        elif wfcl == "onjoinmsg false":
            await self.open_settings(userid, ctx.author.username)
            users[str(userid)]["onJoinMsg"] = False
            with open("settings.json", "w") as f:
                json.dump(users, f)
            await asyncio.sleep(2)
            return await self.send(f"{ctx.author.mention} I have changed onJoinMsg to False for you.", whisper=[ctx.author.id])
        elif wfcl == "allowuserinteraction true":
            await self.open_settings(userid, ctx.author.username)
            users[str(userid)]["allowUserInteraction"] = True
            with open("settings.json", "w") as f:
                json.dump(users, f)
            await asyncio.sleep(2)
            return await self.send(f"{ctx.author.mention} I have changed allowUserInteraction to True for you.", whisper=[ctx.author.id])
        elif wfcl == "allowuserinteraction false":
            await self.open_settings(userid, ctx.author.username)
            users[str(userid)]["allowUserInteraction"] = True
            with open("settings.json", "w") as f:
                json.dump(users, f)
            await asyncio.sleep(2)
            return await self.send(f"{ctx.author.mention} I have changed allowUserInteraction to True for you.", whisper=[ctx.author.id])
        elif wfcl == "allowmentions":
            await asyncio.sleep(2)
            return await self.send(f"{ctx.author.mention} you didn't supply a boolean, run the command again.", whisper=[ctx.author.id])

        elif wfcl == "autorejectfights":
            await asyncio.sleep(2)
            return await self.send(f"{ctx.author.mention} you didn't supply a boolean, run the command again.", whisper=[ctx.author.id])
        elif wfcl == "passivemode":
            await asyncio.sleep(2)
            return await self.send(f"{ctx.author.mention} you didn't supply a boolean, run the command again.", whisper=[ctx.author.id])
        elif wfcl == "whispereconomy":
            await asyncio.sleep(2)
            return await self.send(f"{ctx.author.mention} you didn't supply a boolean, run the command again.", whisper=[ctx.author.id])
        elif wfcl == "onjoinmsg":
            await asyncio.sleep(2)
            return await self.send(f"{ctx.author.mention} you didn't supply a boolean, run the command again.", whisper=[ctx.author.id])
        elif wfcl == "allowuserinteraction":
            await asyncio.sleep(2)
            return await self.send(f"{ctx.author.mention} you didn't supply a boolean, run the command again.", whisper=[ctx.author.id])
        else:
            await asyncio.sleep(2)
            return await self.send(f"{ctx.author.mention} I believe that is an incorrect argument, try running the command again.", whisper=[ctx.author.id])

    # Statistics

    @event
    async def on_message(self, message: Message):
        if message.content.startswith(
                "{self.prefix}") and not message.content.startswith("{self.prefix}stats"):
            await self.open_account(message.author.id, message.author.username)
            userid = message.author.id
            users = await self.get_stats_data()

            users[str(userid)]["rancmd"] += 1

            with open("statistics.json", "w") as f:
                json.dump(users, f)
        else:
            if not message.content.startswith(
                "{self.prefix}") or not message.content.startswith(
                    "v!") or not message.content.startswith(
                    "!") or not message.content.startswith(
                    ".") or not message.content.startswith(
                    "h!") or not message.content.startswith("$"):
                global msg
                global msgauthor
                msg = message.content
                msgauthor = message.author.username
                await self.open_account(message.author.id,
                                        message.author.username)
                userid = message.author.id
                users = await self.get_stats_data()

                randxp = random.randrange(1, 3)
                users[str(userid)]["xp"] += randxp
                users[str(userid)]["sentmsgs"] += 1

                with open("statistics.json", "w") as f:
                    json.dump(users, f)
                    return

    @command
    async def stats(self, ctx: Message):
        await self.open_account(ctx.author.id, ctx.author.username)
        userid = ctx.author.id
        users = await self.get_stats_data()

        rancmds = users[str(userid)]["rancmd"]
        xp = users[str(userid)]["xp"]
        msgs = users[str(userid)]["sentmsgs"]
        whisperto = [ctx.author.id]
        await self.send(message=f"{ctx.author.mention} Here are your stats! • Ran {rancmds} DogeBoss commands • XP: {xp} • Sent {msgs} messages", whisper=whisperto)

    async def open_account(self, userid, username):
        users = await self.get_stats_data()

        if str(userid) in users:
            return False
        else:
            users[str(userid)] = {}
            users[str(userid)]["username"] = username
            users[str(userid)]["rancmd"] = 0
            users[str(userid)]["xp"] = 0
            users[str(userid)]["sentmsgs"] = 0

        with open("statistics.json", "w") as f:
            json.dump(users, f)
        return True

    async def get_stats_data(self):
        with open("statistics.json", "r") as f:
            users = json.load(f)

        return users

    @command
    async def leaderboard(self, ctx: Context, category: str = "rancmd"):
        """Views the leaderboard"""
        users = await self.get_stats_data()
        leader_board = {}
        total = []
        x = 5
        for user in users:
            name = str(user)
            username = users[user]["username"]
            total_amount = users[user][category]
            leader_board[total_amount] = name
            total.append(total_amount)

        total = sorted(total, reverse=True)
        index = 1
        messages = []
        for amt in total:
            id_ = leader_board[amt]
            userGetName = await self.get_stats_data()
            name = userGetName[id_]["username"]
            messages.append(f"{x}. {name} - {amt}")
            if index == x:
                break
            else:
                index += 1

        await self.send(f"{' • '.join(messages[:5])}", whisper=[ctx.author.id])

    async def update_stats(self, userid, change=0, mode="rancmd"):
        users = await self.get_stats_data()

        users[str(userid)][mode] += change

        with open("statistics.json", "w") as f:
            json.dump(users, f)

        stats = [users[str(userid)]["rancmd"], users[str(userid)]["xp"]]
        return stats

    @command
    async def whoami(self, ctx: Message):
        """Gets info about yourself"""
        await self.userinfo(self, ctx)

    @command
    async def whereami(self, ctx: Message):
        """Gets info about the room you're in"""
        await self.send(f"Name: {self.room.name} • Description: {self.room.description} • ID: {self.room.id} • Member Count: {self.room.count} • Created at: {self.room.created_at} • Is Private?: {self.room.is_private}")

    @command
    async def slots(self, ctx: Message):
        """Plays a slot machine :slot_machine:"""
        final = []
        for i in range(5):
            a = random.choice([":redDogeHouse:", ":OrangeDogeHouse:",
                               ":PurpleDogeHouse:", ":CyanDogeHouse:", ":CoolHouse:"])
            final.append(a)

        final_set = set(final)

        # Checks if they are all the same
        if len(final_set) == 1:
            return await self.send(f"{ctx.author.mention} Triple! You won!ㅤ •ㅤ {' | '.join(final)}")
        # Checks if at least 2 are the same
        elif len(final) != len(final_set):
            return await self.send(f"{ctx.author.mention} You won!ㅤ •ㅤ {' | '.join(final)}")
        else:
            return await self.send(f"{ctx.author.mention} You lost!ㅤ •ㅤ {' | '.join(final)}")

    @command
    async def crypto(self, ctx: Message, currency: str):
        """Returns stats for the specified cryptocurrency :CryptoDOGE:"""

        # Get the current currency symbol name to get the right price for that currency
        curr_symbol = locale.localeconv()['int_curr_symbol'].lower()

        req = requests.get(
            f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={curr_symbol}&ids={currency}").json()
        if req == []:
            return await self.send(f"I couldn't find any results for the cryptocurrency: {currency} • Example: {self.prefix}crypto bitcoin")
        rejson = req[0]

        name = rejson["name"]
        symbol = rejson["symbol"].upper()
        price = locale.currency(rejson["current_price"])  # Format as currency
        ranked = rejson["market_cap_rank"]
        twenty_high = rejson["high_24h"]
        twenty_low = rejson["low_24h"]
        twenty_change = rejson["price_change_24h"]
        twenty_perc = rejson["price_change_percentage_24h"]
        updated = rejson["last_updated"]
        ath = rejson["ath"]
        ath_change_perc = rejson["ath_change_percentage"]
        ath_date1 = rejson["ath_date"]
        ath_date = ath_date1[:-14]
        atl = rejson["atl"]
        atl_change_perc = rejson["atl_change_percentage"]
        atl_date1 = rejson["atl_date"]
        atl_date = atl_date1[:-14]
        lupdt = updated[:-14]

        # just for the ranked 2 last characters
        if ranked == 1:
            rankedsym = "st"
        elif ranked == 2:
            rankedsym = "nd"
        elif ranked == 3:
            rankedsym = "rd"
        else:
            rankedsym = "th"

        await self.send(f"Crypto data for: {name} ({symbol}) • Current Price: {price} • Ranked: {ranked}{rankedsym} • Last 24h stats: Highest: {twenty_high}, Lowest: {twenty_low}, Change: {twenty_change}, Change in %: {twenty_perc}% • All Time High (ATH): {ath}, ATH Change in %: {ath_change_perc}%, ATH at: {ath_date} • All Time Low (ATL): {atl}, ATL Change in %: {atl_change_perc}%, ATL at: {atl_date} • Last update at {lupdt}")

    # RonaRage/iCrazyBlaze's commands (DogeBoss' Brother)
    @command
    async def dog(self, ctx: Message):
        """Returns a random image of a dog :dog:"""
        image_url = requests.get("https://api.thedogapi.com/v1/images/search", headers={
                                 "x-api-key": "d0558cf8-f941-42f7-8daa-6741a67c5a2e"}).json()[0]["url"]
        await self.send(image_url)

    @command
    async def cat(self, ctx: Message):
        """Returns a random image of a cat :cat:"""
        image_url = requests.get("https://api.thecatapi.com/v1/images/search", headers={
                                 "x-api-key": "37b77c23-9000-46c8-b808-a224a26f2d2a"}).json()[0]["url"]
        await self.send(image_url)

    @command
    async def shibe(self, ctx: Message):
        """Returns a random image of a Shibe :dogeCool:"""
        image_url = requests.get(
            "https://shibe.online/api/shibes?count=1").json()[0]
        await self.send(image_url)

    @command
    async def fortune(self, ctx: Message):
        """Returns a random fortune"""
        req = requests.get("http://yerkee.com/api/fortune").json()["fortune"]
        line = req.replace('\n', '').replace('\t', '')
        await self.send(line)

    @command
    async def joke(self, ctx: Message):
        """Tells a joke"""
        req = requests.get(
            "https://v2.jokeapi.dev/joke/Any?type=single").json()["joke"]
        line = " ".join(req.splitlines())
        await self.send(line)

    @command
    async def insult(self, ctx: Message, *, other_user: User = ctx.author):
        """Insults the user you mentioned"""
        req = requests.get("https://insult.mattbas.org/api/insult")
        html = req.content.decode("utf-8")
        await self.send(f"{other_user}, {req.content}.")

    @command
    async def compliment(self, ctx: Message, *, other_user: User = ctx.author):
        """Compliments the user you mentioned"""
        req = requests.get("http://www.madsci.org/cgi-bin/lynn/jardin/SCG")
        html = req.content
        soup = BeautifulSoup(html, "html.parser")
        await self.send(f"{other_user}, {soup.h2.string.strip()}")

    @command
    async def choose(self, ctx: Message, *, message):
        """Chooses a random option (separated by comma)"""
        await self.send(random.choice(message.replace(", ", ",").split(",")))

    @command
    async def roll(self, ctx: Message, *, sides: int):
        """Rolls a dice"""
        await self.send("You rolled ... " + str(random.randint(1, sides)))

    @command
    async def gh(self, ctx: Message, *, query: str):
        """Searches for a GitHub repo :GitHub:"""
        repo = requests.get(
            "https://api.github.com/search/repositories?q=" + query).json()
        await self.send("Best match: " + repo["items"][0]["html_url"])

    @command
    async def funfact(self, ctx: Message):
        res = requests.get(
            "https://uselessfacts.jsph.pl/random.json?language=en")
        funfactt = res.json()
        textfun = funfactt["text"]
        whisperto = [ctx.author.id]
        await self.send(message=textfun, whisper=whisperto)

    @command
    async def define(self, ctx: Message, *, term: str):
        """Searches for the specified term on Urban Dictionary"""
        api = "http://api.urbandictionary.com/v0/define"
        # Send request to the Urban Dictionary API and grab info
        response = requests.get(api, params=[("term", term)]).json()
        # Get results
        result_list = response["list"][0]

        if result_list == []:
            await self.send(f"Couldn't find any results for {term} on Urban Dictionary")
            return

        defin = result_list["definition"]
        example = result_list["example"]

        if "2." in defin:  # If there is a second definition splits data
            defin = result_list["definition"].split("2.")  # Splits data
            defin = defin[0]  # Sets defin as first definition

        if "2." in example:  # If there is a second example splits data
            example = result_list["example"].split("2.")  # Splits data
            example = example[0]  # Sets defin as first example

        if len(example) > 250 or len(defin) > 250:   # Sets a 250 character limit
            example = example[:250]
            defin = defin[:250]

        await self.send((f"Results for '{term}' on Urban Dictionary: • Definition: {defin} • Example: {example}"))

    @command
    async def covid(self, ctx: Message, *, country=None):
        """Sends COVID stats for the specified country :coronaS:"""
        country = string.capwords(country)
        if "Of" in country:
            country = country.replace("Of", "of")
            print(country)

        if country == None:
            active = covid.get_total_active_cases()
            confirmed = covid.get_total_confirmed_cases()
            deaths = covid.get_total_deaths()
            recovered = covid.get_total_recovered()
            whisperto = [ctx.author.id]
            await self.send(
                message=f"Worldwide COVID stats • Confirmed Cases: {confirmed} • Active Cases: {active} • Deaths: {deaths} • Recovered: {recovered} • If you wanna get stats on a specific country: {self.prefix}covid <country>",
                whisper=whisperto)
            return

        cases = Covid().get_status_by_country_name(country.lower())

        region = cases["country"]
        confirmed = cases["confirmed"]
        active = cases["active"]
        deaths = cases["deaths"]
        recovered = cases["recovered"]
        whisperto = [ctx.author.id]
        await self.send(
            f"COVID stats for {region} • Confirmed Cases: {confirmed} • Active Cases: {active} • Deaths: {deaths} • Recovered: {recovered}",
            whisper=whisperto)

    @event
    async def on_user_leave(self, user: User):
        botinfogotten = await self.bot_info_get()
        botinfogotten["botinfo"]["botroomname"] = f"{self.room.name}"
        botinfogotten["botinfo"]["botroomcount"] = f"{self.room.count}"
        botinfogotten["botinfo"]["botroomdescription"] = f"{self.room.description}"
        with open("botinfo.json", "w") as f:
            json.dump(botinfogotten, f)

    @event
    async def on_user_join(self, user: User):
        joined = [user.id]
        botinfogotten = await self.bot_info_get()
        botinfogotten["botinfo"]["botroomname"] = f"{self.room.name}"
        botinfogotten["botinfo"]["botroomcount"] = f"{self.room.count}"
        botinfogotten["botinfo"]["botroomdescription"] = f"{self.room.description}"
        with open("botinfo.json", "w") as f:
            json.dump(botinfogotten, f)
        await self.open_settings(user.id, user.username)
        users = await self.get_settings_data()
        onJoinMsg = users[str(user.id)]["onJoinMsg"]
        if onJoinMsg == True:
            await self.send(
                message=f"Welcome {user.mention}\u200B! Hey, my name is DogeBoss! I'm a multi-purpose chatbot, to see my features, type: {self.prefix}help",
                whisper=joined)
        elif onJoinMsg == False:
            return

    @command
    async def uptime(self, ctx: Message):
        """Shows for how long the bot has been online"""
        delta_uptime = datetime.utcnow() - launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        await self.send(f"I've been online for {days} day(s), {hours} hour(s), {minutes} minute(s), and {seconds} second(s)")

    @command
    async def math(self, ctx: Message, *, expression: str = None):
        """Returns the results for a mathematical example :5Head:"""
        if expression == None:
            return await self.send(
                f"{ctx.author.mention} Missing Required Argument - Usage: {self.prefix}math <math-problem> • Example: {self.prefix}math 69+420*1337"
            )

        else:
            try:
                filtering = re.search(
                    "[a-zA-Z]", expression
                )  # regex filter so we make sure that no character from the alphabet gets eval'd (thanks Erlend)
                text = expression
                d = dict.fromkeys(text, 0)
                for c in text:
                    d[c] += 1
                if '**' in expression:
                    if d['**'] <= 1:
                        pass
                    else:
                        return await self.send("That was a good try!")

                whisperto = [ctx.author.id]
                if filtering == None:  # filtering is None when the user passes the regex check
                    calculation = eval(expression)
                    print(calculation)  # evaluates the math example
                    await self.send(
                        message=f'Math: {expression}ㅤㅤ•ㅤㅤAnswer: {calculation}',
                        whisper=whisperto)
                else:
                    await self.send(
                        'You can type only numbers and operators (0-9, *, -, +, /, .)'
                    )
            except Exception as e:
                print(e)
                await self.send(f"Error: {e}")

    @command
    async def echo(self, ctx: Message, *, msg: str = None):
        """Repeats what you said"""
        if msg == None:
            return await self.send(
                f"{ctx.author.mention} Missing Required Argument - Usage: {self.prefix}echo <message> • Example: {self.prefix}echo wow cool. mush doge."
            )
        elif msg.startswith("$") or msg.startswith("!") or msg.startswith({self.prefix}) or msg.startswith("v!"):
            return await self.send(
                f"{ctx.author.mention} You can't use bot commands with echo!")
        else:
            await self.send(msg)
            await asyncio.sleep(5)

    @command
    async def pp(self, ctx: Message, *, user: User):
        """Shows the tagged user's PP :gachiHYPER:"""

        pp_length = random.randrange(-1, 16)

        if pp_length == -1:
            pprnd = "girl moment :SillyChamp:"
        else:
            pprnd = "8" + "=" * pp_length + "D"

        await self.send(f"{user}'s PP: ㅤㅤㅤ{pprnd}")

    @command
    async def userinfo(self, ctx: Message, user: User = ctx.author):
        """Gets info about the user you mentioned, or you if no user is specified"""
        await self.send(f"Username: {user.mention}  •  Display Name: {user.displayname}  •  ID: {user.id}")

    def split_list(self, a_list):
        half = len(a_list)//2
        return a_list[:half], a_list[half:]

    @command
    async def help(self, ctx: Message):
        """Teaches you what different commands do"""
        user = [ctx.author.id]

        helparray = []
        this = self.__class__
        for key in this.__dict__:
            if hasattr(this.__dict__[key], '__call__'):
                function = this.__dict__[key]

                # Functions that have no doc should be excluded
                if function.__doc__ == None:
                    return

                # Get argument names and surround them with <>
                varnames = inspect.getfullargspec(function).args
                varnames.remove("self")
                varnames_formatted = ' '.join(
                    '<' + item + '>' for item in varnames)

                helpstring = f"{self.prefix}{function.__name__} {varnames_formatted}  -  {function.__doc__}"
                helparray.append(helpstring)

        # Split the help page into 2 messages
        help1, help2 = self.split_list(helparray)
        await self.send("Hey, these are my commands right now! • " + ' • '.join(help1), whisper=user)
        await asyncio.sleep(1.5)
        await self.send(' • '.join(help2), whisper=user)


if __name__ == "__main__":
    Client(DOGETOKEN, DOGEREFRESHTOKEN,
           prefix="d!", reconnect_voice=True).run()
