from dogehouse import DogeClient, event, command
from dogehouse.entities import User, Message
import dogehouse, os, requests, aiohttp, random, string, datetime, time, asyncio, re, json
from datetime import datetime
from covid import Covid

DOGETOKEN = os.getenv('DOGEHOUSE_TOKEN') #getting our token from the env
DOGEREFRESHTOKEN = os.getenv('DOGEHOUSE_REFRESH_TOKEN') #getting our refresh token from the env

launch_time = datetime.utcnow() #this is for the uptime command


class Client(DogeClient): 
  @event
  async def on_ready(self):
    print(f"Successfully connected as {self.user}!")
    await self.create_room("DogeBoss!")
    await self.send(f"Hey! My name is DogeBoss! I'm a multi-purpose chatbot, to see my features, type:ㅤㅤ d!help")
  
  
  # Events, Starboard right here;
  @event
  async def on_message(self, message: Message):
    if message.content.startswith("d!"):
      pass
    elif message.content.startswith("!"):
      pass
    elif message.content.startswith("."):
      pass
    elif message.content.startswith("h!"):
      pass #code above made sure that the starred message wouldn't be a bot message
    else:
      global msg #making the two variables global so we can use them across the whole file
      global msgauthor
      msg = message.content
      msgauthor = message.author.username
    
  @command
  async def setstar(self, ctx: Message):
    global msg
    global msgauthor
    global starred #also making those global so we can use them across the whole file
    global starredauthor
    starred = msg
    starredauthor = msgauthor
    await self.send(f"Starred message was set!")
  
  @command
  async def starred(self, ctx: Message):
    global starred
    global starredauthor
    await self.send(f"Starred Message: {starred}ㅤ|ㅤMessage Creator: @{starredauthor}")
  
  
  @command
  async def whoami(self, ctx: Message):
    await self.send(f"Username: {ctx.author.mention}  •  Display Name: {ctx.author.displayname}  •  ID: {ctx.author.id}")
  
  @command
  async def whereami(self, ctx: Message):
    await self.send(f"Name: {self.room.name} • Description: {self.room.description} • ID: {self.room.id} • Member Count: {self.room.count} • Created at: {self.room.created_at} • Is Private?: {self.room.is_private}")
  
  @command
  async def slots(self, ctx: Message):
  
    final = []
    for i in range(5): #for loop
      a = random.choice([":redDogeHouse:",":OrangeDogeHouse:",":PurpleDogeHouse:",":CyanDogeHouse:",":CoolHouse:"])
    
      final.append(a)
  
    if final[0] == final[1] and final[1] == final[2]: #checks if theyre all the same
      return await self.send(f"{ctx.author.mention} Triple! You won!ㅤ •ㅤ {final[0]} | {final[1]} | {final[2]}")
  
    elif final[0] == final[1] or final[0] == final[2] or final[2] == final[1]: #checks if at least 2 are the same
      return await self.send(f"{ctx.author.mention} You won!ㅤ •ㅤ {final[0]} | {final[1]} | {final[2]}")
    else:
      return await self.send(f"{ctx.author.mention} You lost!ㅤ •ㅤ {final[0]} | {final[1]} | {final[2]}")

  @command 
  async def crypto(self, ctx: Message, crypc: str):
    reqs = requests.get(f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=eur&ids={crypc}")
    rejso = reqs.json()
    if rejso == []:
      return await self.send(f"I couldn't find any results for the cryptocurrency: {crypc} • Example: d!crypto bitcoin")
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
    
    # just for the ranked 2 last characters
    if ranked == 1:
      rankedsym = "st"
    elif ranked == 2:
      rankedsym = "nd"
    elif ranked == 3:
      rankedsym = "rd"
    else:
      rankedsym = "th"
    
    await self.send(f"Crypto data for: {name} ({symbol}) • Current Price: {price}€ • Ranked: {ranked}{rankedsym} • Last 24h stats: Highest: {twenty_high}€, Lowest: {twenty_low}€, Change: {twenty_change}, Change in %: {twenty_perc}% • All Time High (ATH): {ath}€, ATH Change in %: {ath_change_perc}%, ATH at: {ath_date} • All Time Low (ATL): {atl}€, ATL Change in %: {atl_change_perc}%, ATL at: {atl_date} • Last update at {lupdt}")

  @command
  async def funfact(self, ctx: Message):
    res = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
    funfactt = res.json()
    textfun = funfactt["text"]
    await self.send(textfun)
  
  @command
  async def define(self, ctx: Message, *, term: str):
    index = 0
    async with aiohttp.ClientSession() as session:  # Opens client session
      async with session.get("https://api.urbandictionary.com/v0/define", params={"term": term}) as r:  # Result
        result = await r.json()  # Parses file as json
      print(result)
      
      resss = result["list"]
      
      if resss == []:
        await self.send(f"Couldn't find any results for {term} on Urban Dictionary")
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
      elif len(example) > 250:   # Sets a 250 character limit
        example = example[:250]
      await self.send(f"Results for: {term}  on Urban Dictionaryㅤㅤ • ㅤㅤDefinition: {defin}ㅤㅤ •ㅤㅤ Example: {example}")

  @command
  async def covid(self, ctx: Message, *, counry = None):
    # TODO: if country == None then get global stats, need to wait for dogehouse.py to get that
    country = string.capwords(counry)
    if "Of" in country:
      country = country.replace("Of", "of")
      print(country)
    
    cases = Covid().get_status_by_country_name(country.lower())
    
    region = cases["country"]
    confirmed = cases["confirmed"]
    active = cases["active"]
    deaths = cases["deaths"]
    recovered = cases["recovered"]
    
    await self.send(f"COVID stats for {region} • Confirmed Cases: {confirmed} • Active Cases: {active} • Deaths: {deaths} • Recovered: {recovered}")


  @event
  async def on_user_join(self, user: User):
    joined = [user.id]
    await self.send(message=f"Welcome {user.mention}\u200B! I am DogeBoss, a chatbot for DogeHouse, to see my commands type: d!help", whisper=joined)
  
  @command
  async def uptime(self, ctx: Message):
    delta_uptime = datetime.utcnow() - launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    
    
    # STUPID CODE ALERT!!!!!
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
    
    # The total mess above this was just to make an s if it's more than 1 :)
    await self.send(f"I've been online for {dayst} {hourst} {minutest} {secondst}")


  @command
  async def math(self, ctx: Message, *, expression:str):
    filtering = re.search("[a-zA-Z]", expression) #regex filter so we make sure that no character from the alphabet gets eval'd (thanks Erlend)
    if filtering == None: #filtering is None when the user passes the regex check
      calculation = eval(expression) #evaluates the math example
      await self.send('Math: {}ㅤㅤ•ㅤㅤAnswer: {}'.format(expression, calculation))
    else:
      await self.send('You can type only numbers and operators (0-9, *, -, +, /, .)')




  @command
  async def echo(self, ctx: Message, *, message):
    await self.send(message)
        
  @command
  async def pp(self, ctx: Message, *, user: User):
    pps = ["girl moment :SillyChamp:",
           "8D",
           "8=D",
           "8=D",
           "8==D",
           "8==D",
           "8===D",
           "8===D",
           "8====D",
           "8====D",
           "8=====D",
           "8=====D",
           "8======D",
           "8======D",
           "8=======D",
           "8=======D",
           "8========D",
           "8========D",
           "8=========D",
           "8=========D",
           "8===============D"
           ]
    
    pprnd = random.choice(pps)
      
    await self.send(f"{user}'s pp: ㅤㅤㅤ{pprnd}")
    
  
  @command
  async def userinfo(self, ctx: Message, *, user: User):
    await self.send(f"Info about: {user.displayname}ㅤㅤ|ㅤㅤID: {user.id}ㅤㅤ|ㅤㅤUsername: {user.username}")
  
  @command
  async def fight(self, ctx: Message, *, u22: User):
      
    user1 = ctx.author.mention
    user2 = u22
    
    if user1 == user2:
      await self.send("Damn, you wanna kill yourself? :Sadge:  I won't stop you I guess")
      await asyncio.sleep(2.5)
      suicresp = [f'{user1} has put a gun to his head and pulled the trigger :Sadge:',
                  f'{user1} drowned in the river next to his house',
                  f'{user1} tried to swim in lava, S :OMEGALUL: BAD',
                  f'The shells from a shotgun pierced {user1}\'s head']
      suicresptext = random.choice(suicresp)
      await self.send(f'{suicresptext}')
      return
      
    win = random.choice([user1, user2])
    if win == user1:
      lose = user2
   
    else:
      lose = user1
     
     
    responses = [f'That was an intense battle, but unfortunately {win} has beaten up {lose} to death', f'That was a shitty battle, they both fight themselves to death', f'Is that a battle? You both suck', f'Yo {lose} you lose! Ha', f'I\'m not sure how, but {win} has won the battle']
    response = random.choice(responses)

    await self.send(f'{response}')
  
  @command
  async def help(self, ctx: Message):
    user = [ctx.author.id]
    await self.send(message="Hey, these are my commands right now! • d!echo <message>  -  Repeats what you said • d!pp <user>  -  Sends the tagged user's pp :gachiHYPER: • d!covid <country>  - Sends COVID stats for the specified country :coronaS: • d!define <term>  - Searches for the specified term on Urban Dictionary • d!funfact  - Returns a random fun fact • d!crypto <currency>  - Returns stats for the specified crypto :CryptoDOGE: • d!math <example>  -  Returns the results for a mathematical example :5Head: • d!slots  -  Slots command, economy will be implemented", whisper = user)
    await asyncio.sleep(1.5)
    await self.send(message="d!fight <user>  -  You fight the user you mentioned :hyperHammer: • d!uptime  -  Shows for how long the bot has been online • d!setstar & d!starred  -  d!setstar Sets a message to be starred, a starred message can be accessed by typing d!starred unless it's overwritten by another starred message", whisper = user)
    #whispers the help command to the user that executed it

if __name__ == "__main__":
  Client(DOGETOKEN, DOGEREFRESHTOKEN, prefix="d!").run()
