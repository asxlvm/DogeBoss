from dogehouse import DogeClient, event, command
from dogehouse.entities import User, Message, UserPreview, BaseUser, Context
import dogehouse


from typing import Union
import os
import requests
import aiohttp
import random
import string
import datetime, time
from datetime import datetime
import asyncio
import re
from inspect import getdoc
import inspect
import sys
import psutil
import subprocess
import json
from covid import Covid
from bs4 import BeautifulSoup
from keep_alive import keep_alive

DOGETOKEN = os.getenv('DOGEHOUSE_TOKEN')
DOGEREFRESHTOKEN = os.getenv('DOGEHOUSE_REFRESH_TOKEN')
ownerid = "de27447e-a633-484d-afaa-8377887dda7b"
launch_time = datetime.utcnow()  #this is for the uptime command
print(launch_time)


class Client(DogeClient):
	@event
	async def on_ready(self):
		try:
			keep_alive()
			print("Keep Alive initiated")
			print(f"Successfully connected as {self.user}")
				#await self.create_room("testingbruh")
			await self.join_room("3daf5a80-5b0a-4dde-9527-9db1f7f13755")
			#await self.join_room("49f98ecb-fd8c-4013-a642-14463f6da784")
		except Exception as e:
			print(e)
	
	@command
	async def help(self, ctx: Context, *, cmd: str = None):
		"""
		The main help menu! Arguments: cmd = an optional argument which specifies a command, so that you can see the command description.
		"""
		if cmd is None:
			sentmsg = f"Hello, my prefix is `{self.prefix}` , to see info about a specific command, type {self.prefix}help <command name> , my commands are: " + " • ".join(self.commands.keys())
		else:
			cmd = cmd.lower()
			try:
				sentmsg = f"`{cmd}` : {getdoc(self.commands[cmd][0])}"
			except:
				sentmsg = f"Could not find `{cmd}` ! Use `{self.prefix}help` to see all commands!"
		await self.send(sentmsg, whisper=[ctx.author.id])



	async def bot_info_get(self):
		with open("botinfo.json", "r") as f:
			botinfo = json.load(f)
		return botinfo
	
	async def convertuser(self, base_user_id):
		try:
			for user in self.room.users:
				if base_user_id == user.id:
					return user
					break
				else:
					continue
		except:
			pass



	@command
	async def altcheck(self, ctx: Context):
		"""Checks for any alternative accounts in the room | Currently doesn't work"""
		authormsg = ctx.author
		#authormsg = await self.convertuser(ctx.author.id)
		if authormsg.id == ownerid:
			pass
		elif authormsg.room_permissions.is_mod or authormsg.room_permissions.is_admin == True:
			pass
		else:
			return await self.send("You don't have permission to do that.", whisper=[ctx.author.id])
		await self.send("This may take a while, be patient.", whisper=[ctx.author.id])
		users = []
		print("before for loop")
		for user in self.room.users:
			userdata = await self.returnavinfo(user)
			if userdata['message'] == "Twitter":
				continue
			else:
				if "Marked as spam" in userdata['message']:
					users.append(userdata['message'])
					continue
				dtm = userdata['crdate']
				rntime = datetime.now()
				d = datetime.fromisoformat(dtm[:-1])
				d.strftime('%Y-%m-%d %H:%M:%S.%f')
				timedeltuh = rntime - d
				if timedeltuh.days >= 14:
					appusdata = userdata['message'] + f"- {timedeltuh} • "
					users.append(appusdata)
				else:
					continue
		
		print("before lencheck")
		userssend = "".join(users)
		print(userssend)
		print(len(userssend))
		try:
			if len(userssend) >= 520:
				strround = round(len(userssend))
				strlen = round(strround) / 2
				first_half = userssend[:int(strlen)]
				second_half = userssend[int(strlen):]
				await self.send(first_half, whisper=[ctx.author.id])
				await asyncio.sleep(2)
				await self.send(second_half, whisper=[ctx.author.id])
				return
			print("done")
			await self.send(userssend, whisper=[ctx.author.id])
		except Exception as e:
			print(e)


	@command
	async def execlang(self, ctx: Context):
		f"""Shows all the available languages for `{self.prefix}execute`"""
		requrl = "https://emkc.org/api/v1/piston/versions"
		req = requests.get(requrl)
		names = []
		reqjson = req.json()
		namenum = 0
		for re in range(39):
			names.append(f"{reqjson[re]['name']} - ")
			namenum += 1
			if namenum == 39:
				break
		namestr = "".join(names)
		await self.send(namestr, whisper=[ctx.author.id])



	@command
	async def execute(self, ctx: Context, lang, *, src):
		f"""Executes a script with any of the languages listed in `{self.prefix}execlang` | `/new` is used for new lines, `/ind` is used for an indent | Arguments: language = The chosen language to run the script with • script = The specified code to run"""
		requrl = "https://emkc.org/api/v1/piston/execute"
		srce = src.replace("/ind ", "  ")
		reqdata = {
			'language': lang, 'source': srce.replace("/new ", "\n"), 'args': "", 'stdin': "", 'log': 0
		}
		req = requests.post(requrl, data=json.dumps(reqdata))
		reqjson = req.json()
		#if "output" not in reqjson:
			#try:
				#return await self.send(reqjson['message'], whisper=[ctx.author.id])
			#except Exception as e:
				#return await self.send(e, whisper=[ctx.author.id])
		output = reqjson['output']
		await self.send(output, whisper=[ctx.author.id])

	@command
	async def sysinfo(self, ctx: Context):
		"""Gives you client system info"""
		start = time.perf_counter()
		end = time.perf_counter()
		duration = (end - start) * 1000
		cpuavg = psutil.cpu_percent(interval=None)
		mem = psutil.virtual_memory()[2]
		durround = round(duration, 3)
		osun = os.uname()
		await self.send(f"System Info | CPU: {cpuavg}% | RAM: {mem}% | Latency: {durround * 1000}ms | OS: {sys.platform}", whisper=[ctx.author.id])

	#RonaRage's commands <3
	
	@command
	async def dog(self, ctx: Message):
		"""Returns a random image of a dog"""
		image_url = requests.get("https://api.thedogapi.com/v1/images/search", headers={"x-api-key": "d0558cf8-f941-42f7-8daa-6741a67c5a2e"}).json()[0]["url"]
		await self.send(image_url, whisper=[ctx.author.id])
	
	@command
	async def cat(self, ctx: Message):
		"""Returns a random image of a cat"""
		image_url = requests.get("https://api.thecatapi.com/v1/images/search", headers={"x-api-key": "37b77c23-9000-46c8-b808-a224a26f2d2a"}).json()[0]["url"]
		await self.send(image_url, whisper=[ctx.author.id])
	
	@command
	async def shibe(self, ctx: Message):
		"""Returns a random image of a Shibe"""
		image_url = requests.get("https://shibe.online/api/shibes?count=1").json()[0]
		await self.send(image_url, whisper=[ctx.author.id])
	
	@command
	async def fortune(self, ctx: Message):
		"""Returns a random fortune"""
		req = requests.get("http://yerkee.com/api/fortune").json()["fortune"]
		line = req.replace('\n', '').replace('\t', '')
		await self.send(line, whisper=[ctx.author.id])
	
	@command
	async def joke(self, ctx: Message):
		"""Tells a joke"""
		req = requests.get("https://v2.jokeapi.dev/joke/Any?type=single").json()["joke"]
		line = " ".join(req.splitlines())
		await self.send(line, whisper=[ctx.author.id])
	
	@command
	async def insult(self, ctx: Message, *, other_user: User = None):
		"""Insults the user you mentioned"""
		if other_user == None:
			other_user = ctx.author.mention
		req = requests.get("https://insult.mattbas.org/api/insult")
		html = req.content.decode("utf-8")
		await self.send(f"{other_user}, {req.content}.")
	
	@command
	async def compliment(self, ctx: Message, *, other_user: User = None):
		"""Compliments the user you mentioned"""
		if other_user == None:
			other_user = ctx.author.mention
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
		await self.send("You rolled ... " + str(random.randint(1, sides)), whisper=[ctx.author.id])
	
	@command
	async def gh(self, ctx: Message, *, query: str):
		"""Searches for a GitHub repo :GitHub:"""
		repo = requests.get("https://api.github.com/search/repositories?q=" + query).json()
		await self.send("Best match: " + repo["items"][0]["html_url"])

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
			
	#@event
	#async def on_ready(self):
  	#print(f"Successfully connected as {self.user}!")
		#await self.create_room("Testing dogehouse.py!") 
    #await self.join_room("d6046f84-28f2-4442-b6a1-28b53b3a6952")
		#await self.join_room("755293bc-3a54-415e-99a0-bb1d7ef07bbe")
		#await self.join_room("aa2e15e1-b1da-42cd-a802-6789d7ddf6ec")

		#await self.send(f"Hey! My name is DogeBoss! I'm a multi-purpose chatbot, to see my features, type:ㅤㅤ d!help"

# Starboard command

	@command
	async def setstar(self, ctx: Message):
		f"""Sets the latest message as starred, you can access starred messages with `{self.prefix}starred`"""
		global msg #making the variables global so we can access them from any command
		global msgauthor
		global starred
		global starredauthor
		starred = msg
		starredauthor = msgauthor
		await self.send(f"Starred message was set! You may access it with d!starred")

	@command
	async def starred(self, ctx: Message):
		"""Shows you the starred message"""
		global starred
		global starredauthor
		await self.send(
		    f"Starred Message: {starred}ㅤ|ㅤMessage Creator: @{starredauthor}")

	@command
	async def owoify(self, ctx: Message, *, owome: str = None):
		"""Owoifies your message UwU"""
		if owome == None:
			return await self.send(
			    f"{ctx.author.mention} Missing Required Argument - Usage: d!owoify <message> • Example: d!owoify dont hurt me!"
			)
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
					owomee = owome.replace(i, random.choice(uwufaces))

			for i in owome:
				if i in upperreplacing_words:
					owomee = owome.replace(i, f"Y{i}")

			for i in owome:
				if i in replacing_words:
					owomee = owome.replace(i, f"y{i}")

			await self.send(f"{owomee}ㅤㅤ• {ctx.author.mention}")
	
	@command
	async def github(self, ctx: Message):
		"""Sends you the DogeBoss repository"""
		await self.send(
		    f"{ctx.author.mention} ㅤㅤ I'm open-source! You can look at my source code here!ㅤ https://github.com/asxlvm/DogeBoss :GitHub:"
		)
	
	@command
	async def battle(self, ctx: Context, *, user: BaseUser):
		"""Makes you fight with the specified user | Arguments: user = The user you will be fighting against"""
		print("here")
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
				msg = await self.wait_for(event='message', check=lambda message: message.author.id == currentturnid, timeout = 30)

				msgcont = msg.content.lower()
				if msgcont == 'fight':
					damage = random.randint(1,35)
					if damage == 35:
						damage = random.randint(35,75)
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
			
		#	if currenthpauth <= 0 or currenthpuser <= 0:
			#	if currenthpauth > currenthpuser:
		#			await self.send(f"{m_author_mention} has won against {m_user_mention} in {moves}! His remaining HP was {currenthpauth} HP.")
		#			return False
		#		elif currenthpuser > currenthpauth:
		#			await self.send(f"{m_user_mention} has won against {m_author_mention} in {moves}! His remaining HP was {currenthpuser} HP.")
	#				return False


		except asyncio.TimeoutError:
			await self.send(f"{currentturnmention} did not respond in 30 seconds, fight ended.", whisper=players)
			players = []
			currenthpauth = 100
			currenthpuser = 100
			moves = 0
			return False
			


# Battleeeee ;O


	def owner_check(self, authorid):
		if authorid == ownerid:
			return True
		if authorid != ownerid:
			return False
	
	@command
	async def evaluate(self, ctx: Context, *, evalThis):
		"""Owner-only command for executing code"""
		ownercheck = self.owner_check(ctx.author.id)
		if ownercheck == False:
			return await self.send('Owner-Only Command', whisper=[ctx.author.id])
		res = eval(evalThis)
		if inspect.isawaitable(res):
			await self.send(await res, whisper=[ctx.author.id])
		else:
			await self.send(res, whisper=[ctx.author.id])
	
	@command
	async def shell(self, ctx: Context, *, shellCmd):
		"""Owner-only command for executing commands to the Linux shell"""
		ownercheck = self.owner_check(ctx.author.id)
		if ownercheck == False:
			return await self.send('Owner-Only Command', whisper=[ctx.author.id])
		proc = subprocess.Popen(shellCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		stdout_value = proc.stdout.read() + proc.stderr.read()
		realval = str(stdout_value).replace("\n", " ")
		await self.send(f"{realval}", whisper=[ctx.author.id])


	@command
	async def reboot(self, ctx: Message):
		"""Owner-only command for rebooting the bot"""
		if ctx.author.id == ownerid:
			owner_check = True
		else:
			owner_check = False

		if owner_check == True:
			await self.send("Rebooting the bot, I'll be back in 5 seconds!")
			await self.close()
			await asyncio.sleep(4)
			client = DogeClient(DOGETOKEN,
			                    DOGEREFRESHTOKEN,
			                    prefix="d!",
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
		"""Command for seeing your settings"""
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
			await self.send(f"Your settings:ㅤㅤAllow Mentions: {allowMentions} (If False, bot will send your username instead of mentioning) • Auto-Reject Fights: {autoRejectFights} (If True, you can't accept fight requests as it will decline them automatically) • Passive Mode: {passiveMode} (If True, you can't rob/deposit/withdraw with economy but you also can't get robbed) • Allow User Interaction: {allowUserInteraction} (If True, users can't get information for you, ex. d!balance, d!stats, d!userinfo etc.)", whisper=[ctx.author.id])
		except Exception as e:
			print(e)
	
	@command
	async def change(self, ctx: Context):
		"""Command for changing your settings"""
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
		    "d!") and not message.content.startswith("d!stats"):
			await self.open_account(message.author.id, message.author.username)
			userid = message.author.id
			users = await self.get_stats_data()

			users[str(userid)]["rancmd"] += 1

			with open("statistics.json", "w") as f:
				json.dump(users, f)
		else:
			if not message.content.startswith(
			    "d!") or not message.content.startswith(
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
		"""Command to see your statistics"""
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

	#@command
	#async def leaderboard(self, ctx: Message, cattype: str = None, x: int = 3):
	# users = await get_bank_data()
	# leader_board = {}
	# total = []
	#for user in users:
	# iduser = str(user)
	# print(iduser)
	#  nameuser = users[user]["username"]
	#  print(nameuser)
	# total_amount = users[user]["wallet"] + users[user]["bank"]
	# print(total_amount)
	# leader_board[total_amount] = iduser
	#  print(leader_board[total_amount])
	#total.append(total_amount)

	#  total = sorted(total,reverse=True)

	# text = f"Top {x} people in the category {cattype}"
	#  index = 1
	# for amt in total:
	#   id_ = leader_board[amt]
	#  name = nameuser
	# toptext = "" += f"{index}. {name} • {amt} {cattext}"
	# if index == x:
	#   break
	# else:
	#   index += 1
	
	@command
	async def leaderboard(self, ctx: Context, category: str = "rancmd"):
		"""You're able to see the leaderboards with this command | Arguments: category = (Optional) This changes the category of the leaderboards"""
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
		
		total = sorted(total,reverse=True)
		index = 1
		mesge = []
		for amt in total:
			id_ = leader_board[amt]
			userGetName = await self.get_stats_data()
			name = userGetName[id_]["username"]
			mesge.append(f"{x}. {name} - {amt}")
			if index == x:
				break
			else:
				index += 1
		
		await self.send(f"{mesge[0]} • {mesge[1]} • {mesge[2]} • {mesge[3]} • {mesge[4]}", whisper=[ctx.author.id])



	async def update_stats(self, userid, change=0, mode="rancmd"):
		users = await self.get_stats_data()

		users[str(userid)][mode] += change

		with open("statistics.json", "w") as f:
			json.dump(users, f)

		stats = [users[str(userid)]["rancmd"], users[str(userid)]["xp"]]
		return stats

	####

	# Economy

	####

	@command
	async def roominfo(self, ctx: Message):
		"""You can see the info about the room you're in"""
		await self.send(
		    f"Name: {self.room.name} • Description: {self.room.description} • ID: {self.room.id} • Member Count: {self.room.count} • Created at: {self.room.created_at} • Is Private?: {self.room.is_private}"
		)


	@command
	#async def slots(self, ctx: Message, bet: int):
	async def slots(self, ctx: Message):
		"""Spin a slot machine with this command, gamble it out."""
		final = []
		for i in range(5):
			a = random.choice([
			    ":redDogeHouse:", ":OrangeDogeHouse:", ":PurpleDogeHouse:",
			    ":CyanDogeHouse:", ":CoolHouse:"
			])

			final.append(a)

		if final[0] == final[1] and final[1] == final[2]:
			return await self.send(
			    f"{ctx.author.mention} Triple! You won!ㅤ •ㅤ {final[0]} | {final[1]} | {final[2]}"
			)

		elif final[0] == final[1] or final[0] == final[2] or final[2] == final[
		    1]:
			return await self.send(
			    f"{ctx.author.mention} You won!ㅤ •ㅤ {final[0]} | {final[1]} | {final[2]}"
			)
		else:
			return await self.send(
			    f"{ctx.author.mention} You lost!ㅤ •ㅤ {final[0]} | {final[1]} | {final[2]}"
			)

	@command
	async def crypto(self, ctx: Message, crypc: str = None):
		"""You can see statistics about a cryptocurrency with this command | Arguments: currency = The currency the stats will be shown for"""
		if crypc == None:
			return await self.send(
			    f"{ctx.author.mention} Missing Required Argument - Usage: d!crypto <currency> • Example: d!crypto bitcoin"
			)
		reqs = requests.get(
		    f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=eur&ids={crypc}"
		)
		rejso = reqs.json()
		if rejso == []:
			return await self.send(
			    f"I couldn't find any results for the cryptocurrency: {crypc} • Example: d!crypto bitcoin"
			)
		rejson = rejso[0]

		name = rejson["name"]
		symbol = rejson["symbol"].upper()
		price = rejson["current_price"]
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

		if ranked == 1:
			rankedsym = "st"
		elif ranked == 2:
			rankedsym = "nd"
		elif ranked == 3:
			rankedsym = "rd"
		else:
			rankedsym = "th"
		whisperto = [ctx.author.id]
		await self.send(
		    message=
		    f"Crypto data for: {name} ({symbol}) • Current Price: {price}€ • Ranked: {ranked}{rankedsym} • Last 24h stats: Highest: {twenty_high}€, Lowest: {twenty_low}€, Change: {twenty_change}, Change in %: {twenty_perc}% • All Time High (ATH): {ath}€, ATH Change in %: {ath_change_perc}%, ATH at: {ath_date} • All Time Low (ATL): {atl}€, ATL Change in %: {atl_change_perc}%, ATL at: {atl_date} • Last update at {lupdt}",
		    whisper=whisperto)

	@command
	async def funfact(self, ctx: Message):
		"""Sends you a random funfact"""
		res = requests.get(
		    "https://uselessfacts.jsph.pl/random.json?language=en")
		funfactt = res.json()
		textfun = funfactt["text"]
		whisperto = [ctx.author.id]
		await self.send(message=textfun, whisper=whisperto)

	@command
	async def define(self, ctx: Message, *, term: str = None):
		"""Searches for the specified term on Urban Dictionary | Arguments: term = The term the bot will search for"""
		if term == None:
			return await self.send(
			    f"{ctx.author.mention} Missing Required Argument - Usage: d!define <term> • Example: d!define lmao"
			)
		index = 0
		async with aiohttp.ClientSession() as session:  # Opens client session
			async with session.get("https://api.urbandictionary.com/v0/define",
			                       params={"term": term}) as r:  # Result
				result = await r.json()  # Parses file as json

			resss = result["list"]

			#data = result["list"][index]  # Assigns list in dict as 'data'
			if resss == []:
				await self.send(
				    f"Couldn't find any results for {term} on Urban Dictionary"
				)
				return

			data = result["list"][index]

			defin = data["definition"]  # Gets key value
			if "2." in defin:  # If there is a second definition
				defin = data["definition"].split("2.")  # Splits data
				defin = defin[0]  # Sets defin as first definition
			elif len(defin) > 250:  # Sets a 250 character limit
				defin = defin[:250]

			example = data["example"]  # Gets key value
			if "2." in defin:  # If there is a second example splits data
				example = data["example"].split("2.")  # Splits dat
				example = example[0]  # Sets defin as first example
			elif len(example) > 250:  # Sets a 250 character limit
				example = example[:250]
			whisperto = [ctx.author.id]
			await self.send(
			    message=
			    f"Results for: {term}  on Urban Dictionaryㅤㅤ • ㅤㅤDefinition: {defin}ㅤㅤ •ㅤㅤ Example: {example}",
			    whisper=whisperto)

	@command
	async def covid(self, ctx: Message, *, counry=None):
		"""You can see COVID statistics of a specified country with this command | Arguments: country = The country the stats will be shown for"""

		#countries = Covid().list_countries()
		country = string.capwords(counry)
		if "Of" in country:
			country = country.replace("Of", "of")
			print(country)

	#  if country in countries:
	#  pass
	# else:
	# await self.send("This either isn't a valid country or you didn't specify a country at all! Example: d!covid Czechia")
	#  return

		if country == None:
			active = covid.get_total_active_cases()
			confirmed = covid.get_total_confirmed_cases()
			deaths = covid.get_total_deaths()
			recovered = covid.get_total_recovered()
			whisperto = [ctx.author.id]
			await self.send(
			    message=
			    f"Worldwide COVID stats • Confirmed Cases: {confirmed} • Active Cases: {active} • Deaths: {deaths} • Recovered: {recovered} • If you wanna get stats on a specific country: d!covid <country>",
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
	
	async def returnavinfo(self, usertoget):
		try:
			if "githubuser" in usertoget.avatar_url:
				githubid = usertoget.avatar_url[40:]
				requrl = "https://api.github.com/user/" + githubid
				req = requests.get(requrl)
				reqjson = req.json()
				if 'login' not in reqjson:
					msg = reqjson['message']
					userinfogit = {"message": f"{usertoget.username} - Github: Marked as spam • "}
				else:
					createdat = reqjson['created_at']
					gitid = reqjson['id']
					gitname = reqjson['login']
					userinfogit = {"message": f"{usertoget.username} - Github: {gitname} - {gitid} ", "crdate": f"{createdat}"}
				print("git")
				return userinfogit
			else:
				print("twitter")
				return {"message": "Twitter"}
		except Exception as e:
			print(e)
			return {"message": "Twitter"}
	
	@command
	async def socialinfo(self, ctx: Context, user: User = None):
		"""The bot will try to grab info of their socials through their avatar | Arguments: user = The user the bot will search for"""
		try:
			if user == None:
				return await self.send("didnt tag u dum")
			if "githubuser" in user.avatar_url:
				githubid = user.avatar_url[40:]
				requrl = "https://api.github.com/user/" + githubid
				req = requests.get(requrl)
				reqjson = req.json()
				print(reqjson)
				if 'login' not in reqjson:
					msg = reqjson['message']
					userinfogit = f"The joined account named {user.username} owns a Github account that is marked as spam."
				else:
					createdat = reqjson['created_at']
					gitid = reqjson['id']
					gitname = reqjson['name']
					userinfogit = f"The joined account named {user.username} has a Github account with the name {reqjson['login']} | Creation Date: {createdat} | Name: {gitname} | ID: {gitid}"
				print(userinfogit)
				print(githubid)
				print(user.avatar_url)
				return await self.send(userinfogit, whisper=[ctx.author.id])
			else:
				return await self.send("The Twitter API is a dummy and I can't find user ID throughout a profile picture.", whisper=[ctx.author.id])


		except Exception as e:
			print(e)
	
	@command
	async def userinfo(self, ctx: Context, user: User = None):
		"""Command to see user info about a specified user if wanted | Arguments: user = (optional) The user the bot will get the info from"""
		if user == None:
			user = ctx.author
		user = self.get_user(user.id)
		username = user.username
		uid = user.id
		displayname = user.displayname
		followers = user.num_followers
		following = user.num_following
		avatar_url = user.avatar_url
		bio = user.bio
		perms = user.room_permissions
		if "githubuser" in user.avatar_url:
			githubid = user.avatar_url[40:]
			requrl = "https://api.github.com/user/" + githubid
			req = requests.get(requrl)
			reqjson = req.json()
			
			if 'login' not in reqjson:
				msg = reqjson['message']
				userinfogit = f"Github Account • Marked as spam"
			else:
				createdat = reqjson['created_at']
				gitid = reqjson['id']
				gitname = reqjson['name']
				userinfosoc = f"Github Account | Username {reqjson['login']} | Creation Date: {createdat} | Name: {gitname} | ID: {gitid}"
		else:
			userinfosoc = "Twitter Account • ?"
		
		await self.send(f"Username: {username} | User ID: {uid} | Display Name: {displayname} | Followers: {followers} | Following: {following} | Avatar URL: {avatar_url} | BIO: {bio} | Permissions: {perms} • {userinfosoc}", whisper=[ctx.author.id])




	

		
	@event
	async def on_user_join(self, user: User):
		joined = [user.id]
		if user.avatar_url in ["github"]:
			githubid = user.avatar_url[32:4]
			requrl = "https://api.github.com/user/" + githubid
			req = requests.get(requrl)
			reqjson = req.json()
			if 'login' not in reqjson:
				msg = reqjson['message']
				userinfogit = f"The joined account named {user.username} owns a Github account that is marked as spam."
			else:
				createdat = reqjson['created_at']
				gitname = reqjson['name']
				userinfogit = f"The joined account named {user.username} has a Github account with the name {reqjson['login']} | Creation Date: {createdat} | Name: {gitname}"
				await self.send(userinfogit, whisper=["de27447e-a633-484d-afaa-8377887dda7b"])
		else:
			pass


		botinfogotten = await self.bot_info_get()
		botinfogotten["botinfo"]["botroomname"] = f"{self.room.name}"
		botinfogotten["botinfo"]["botroomcount"] = f"{self.room.count}"
		botinfogotten["botinfo"]["botroomdescription"] = f"{self.room.description}"
		with open("botinfo.json", "w") as f:
			json.dump(botinfogotten, f)
		await self.open_settings(user.id, user.username)
		users = await self.get_settings_data()
		onJoinMessg = users[str(user.id)]["onJoinMsg"]
		if onJoinMessg == True:
			await self.send(
		    message=
		    f"Welcome {user.mention}\u200B! I am DogeBoss, a chatbot for DogeHouse, to see my commands type: d!help",
		    whisper=joined)
		elif onJoinMessg == False:
			return

	@command
	async def uptime(self, ctx: Message):
		"""You can see the bot's uptime with this command"""
		delta_uptime = datetime.utcnow() - launch_time
		hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
		minutes, seconds = divmod(remainder, 60)
		days, hours = divmod(hours, 24)

		if days == 0:
			dayst = ""
		else:
			if days > 1:
				s = "s"
			else:
				s = ""
			dayst = f"{days} day{s},"

		if hours == 0:
			hourst = ""
		else:
			if hours > 1:
				ss = "s"
			else:
				ss = ""
			hourst = f"{hours} hour{ss},"

		if minutes == 0:
			minutest = ""
		else:
			if minutes > 1:
				sss = "s"
			else:
				sss = ""
			minutest = f"{minutes} minute{sss},"

		if seconds == 0:
			secondst = f"1 second"
		else:
			if seconds > 1:
				ssss = "s"
			else:
				ssss = ""
			secondst = f"{seconds} second{ssss}"

		await self.send(
		    f"I've been online for {dayst} {hourst} {minutest} {secondst}")

	@command
	async def math(self, ctx: Message, *, expression: str = None):
		"""This command is able to calculate a mathematical expression | Arguments: expression = The math expression that will be calculated"""
		if expression == None:
			return await self.send(
			    f"{ctx.author.mention} Missing Required Argument - Usage: d!math <math-problem> • Example: d!math 69+420*1337"
			)

	# if "(" in expression:
	#return await self.send(f"You're NOT crashing me again!")
	#elif ")" in expression:
	# return await self.send(f"Surely not crashing me this time!")
		else:
			try:
				filtering = re.search(
				    "[a-zA-Z]", expression
				)  #regex filter so we make sure that no character from the alphabet gets eval'd (thanks Erlend)
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
				if filtering == None:  #filtering is None when the user passes the regex check
					calculation = eval(expression)
					print(calculation)  #evaluates the math example
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
	async def echo(self, ctx: Message, *, msage: str = None):
		"""Repeats the said message | Arguments: message = The message that the bot will repeat"""
		if msage == None:
			return await self.send(
			    f"{ctx.author.mention} Missing Required Argument - Usage: d!echo <message> • Example: d!echo wow cool. mush doge."
			)
		elif msage.startswith("$"):
			return await self.send(
			    f"{ctx.author.mention} You can't use bot commands with echo!")
		elif msage.startswith("!"):
			return await self.send(
			    f"{ctx.author.mention} You can't use bot commands with echo!")
		elif msage.startswith("d!"):
			return await self.send(
			    f"{ctx.author.mention} You can't use bot commands with echo!")
		elif msage.startswith("v!"):
			return await self.send(
			    f"{ctx.author.mention} You can't use bot commands with echo!")
		else:
			await self.send(msage)
			await asyncio.sleep(5)

	@command
	async def pp(self, ctx: Message, *, user: User = None):
		"""Shows the user's pp length | Arguments: user = (optional) The user that will be used in this command"""
		print(user)
		if user == None:
			user = ctx.author
		pps = [
		    "girl moment :SillyChamp:", "8D", "8=D", "8=D", "8==D", "8==D",
		    "8===D", "8===D", "8====D", "8====D", "8=====D", "8=====D",
		    "8======D", "8======D", "8=======D", "8=======D", "8========D",
		    "8========D", "8=========D", "8=========D", "8===============D"
		]

		pprnd = random.choice(pps)

		await self.send(f"{user.mention}'s pp: {pprnd}")

	@command
	async def fight(self, ctx: Message, *, u22: User = None):
		"""Shows the result of a fight against the message author and the specified user | Arguments: user = The user that will be used in this command"""
		if u22 == None:
			return await self.send(
			    f"{ctx.author.mention} Missing Required Argument - Usage: d!fight <user> • Example: d!fight @asylum"
			)

		user1 = ctx.author.mention
		user2 = u22

		if user1 == user2:
			await self.send(
			    "Damn, you wanna kill yourself? :Sadge:  I won't stop you I guess"
			)
			await asyncio.sleep(2.5)
			suicresp = [
			    f'{user1} has put a gun to his head and pulled the trigger :Sadge:',
			    f'{user1} drowned in the river next to his house',
			    f'{user1} tried to swim in lava, S :OMEGALUL: BAD',
			    f'The shells from a shotgun pierced {user1}\'s head'
			]
			suicresptext = random.choice(suicresp)
			await self.send(f'{suicresptext}')
			return

		#if u22 == self.user.mention:
		# await self.send("Why would you wanna do this? I'm calling PETA :hyperHammer:")
		# return
		win = random.choice([user1, user2])
		if win == user1:
			lose = user2

		else:
			lose = user1

		responses = [
		    f'That was an intense battle, but unfortunately {win} has beaten up {lose} to death',
		    f'That was a shitty battle, they both fight themselves to death',
		    f'Is that a battle? You both suck', f'Yo {lose} you lose! Ha',
		    f'I\'m not sure how, but {win} has won the battle'
		]
		response = random.choice(responses)

		await self.send(f'{response}')

if __name__ == "__main__":
	Client(DOGETOKEN, DOGEREFRESHTOKEN, prefix="d!",reconnect_voice=True).run()
