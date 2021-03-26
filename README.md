![](https://img.shields.io/badge/PYTHON-3.5--3.8-green?style=for-the-badge)
DogeBoss
==========

This repository contains the source of an Open-Source [DogeHouse](https://www.dogehouse.tv) bot programmed in Python, use the code however you want.

IMPORTANT!
--------

Do not learn from my code, I'm a dumbass and my techniques are really bad!

What you need:
--------

To run the bot yourself, you will need these three things:

1. Python 3+ (You won't need it downloaded on your device if you're using replit)
2. Your account token and account refresh token
3. All the modules in requirements.txt

How to get Python 3+?
Either download it from [the official Python website](https://www.python.org/downloads/release/python-392) or download it in your Microsoft Windows Store.

How to get your account token and account refresh token?


1. Go to [DogeHouse](https://dogehouse.tv)
2. Login to the "bot" account
3. Open Developer options (F12 or Ctrl+Shift+I)
4. Go to Application > Local Storage > dogehouse.tv
5. Copy your token and refresh-token and put them in an .env file:

```
DOGEHOUSE_TOKEN = "DOGEHOUSE TOKEN HERE"

DOGEHOUSE_REFRESH_TOKEN = "DOGEHOUSE REFRESH TOKEN HERE"
```
(if you're on mobile, just ask your friend to get the tokens for you, there is no other way right now)

How to get all the modules in requirements.txt?

1. Run `pip install -r requirements.txt`
2. Wait, and after a few minutes or less, you should have every module downloaded

How to run
------------

1. Run on PC
- After doing everything in `What you need:` do this:
- Open your command prompt, `cd` into the folder with the main.py file
  - Run the bot with `python main.py`
  - If no errors show up, you're good to go!

2. Run on [replit](https://www.replit.com) [![Run on Repl.it](https://repl.it/badge/github/asxlvm/DogeBoss)](https://repl.it/github/asxlvm/DogeBoss)
- After doing everything in `What you need:` do this:
  - Press the "Run" button as replit will start the file with that
  - If no errors show up, you're good to go!
  
  - If you want 24/7 hosting of the bot on replit add this to the code:
  ```py
  from keep_alive import keep_alive
  
  # your code etc.
  
  keep_alive()
  ```
  - You also have to add a `keep_alive.py` file in the same directory as `main.py` with this code:
  ```py
  from flask import Flask
  from threading import Thread

  app = Flask('')

  @app.route('/')
  def home():
      return "Hello. I am alive!"

  def run():
      app.run(host='0.0.0.0',port=8080)
      print("Flask server running")

  def keep_alive():
      t = Thread(target=run)
      t.start()
      print("Keep Alive file initiated")
  ```
  - After adding all of this code, go to [Uptime Robot](https://uptimerobot.com), register an account if you don't have one already and then do the following:
    - Create a new monitor with these parameters:
      - Monitor Type: HTTP(s)
      - Friendly Name: `Of your own choice, doesn't matter`
      - URL (or IP);
        - Start your script on replit, go to "Web", copy the URL at the top and paste it in the field
      - Click on "Create Monitor" and confirm by clicking "! Create Monitor (with no alert contact selected)"

Commands
--------------------

API Commands:

Command                                 |  Description
-------------------------------------|------------------------------------------------------------------------------------
d!covid                        |  Sends COVID stats of the specified country (will implement that if no country is specified then stats for global will appear) • Usage: `d!covid <country>` • Example: `d!covid Czechia`
d!funfact              |  Sends a random fun fact • Usage: `d!funfact`
d!define         |  Sends a result for the specified term on Urban Dictionary • Usage: `d!define <term>` • Example: `d!define lmao`
d!crypto         |  Sends data about specified cryptocurrency by using the CoinGecko API • Usage: `d!crypto <currency>` • Example: `d!crypto bitcoin`

Fun Commands:

Command                          |  Description
----------------------------------|------------------------------------------------------------------------------------
d!fight            |  You fight against the user you mentioned • Usage: `d!fight <user>` • Example: `d!fight @asylum`
d!pp             |  Sends the tagged user's pp length • Usage: `d!pp <user>` • Example: `d!pp @asylum`
d!slots            |  Spins a slot machine for you (will add economy when I can! :D) • Usage: `d!slots`

Miscellaneous Commands:

Command                          |  Description
----------------------------------|------------------------------------------------------------------------------------
d!math  |  Solves a basic mathematical problem (planning to add square root etc.) • Usage: `d!math <problem>` • Example: `d!math 69+420*1337`
d!uptime                        |  Shows how long the bot is online for • Usage: `d!uptime`
d!whoami                      |  Returns basic info about the user that executed that command • Usage: `d!whoami`
d!whereami                          |  Returns basic info about the room the user is in • Usage: `d!whereami`
d!setstar        |  Sets the last sent message (not containing most bot messages) as a starred message • Usage: `d!setstar`
d!starred                        |  Shows the last starred message • Usage: `d!starred`
d!echo       |  Repeats what the user has said • Usage: `d!echo <message>` • Example: `d!echo wow so mush doge`

Credits

Awesome people            |  Why they deserve credit
----------------------------------|------------------------------------------------------------------------------------
[DogeHouse Github](https://github.com/benawad/dogehouse)     | The people that contributed to the project are the ones that deserve the most credit.
[Ben Awad](https://youtube.com/c/BenAwad97)    | He's the one who made this obviously
[DogeHouse](https://dogehouse.tv)   |  The DogeHouse dev community for being really helpful, kind and supportive <3
[dogehouse.py](https://github.com/Arthurdw/dogehouse.py)  | Arthur for making this great API wrapper, I couldn't make this bot without it obviously!
[BenBot](https://github.com/dragonismcode/benbot)  | As I grabbed a little piece of code from them and "Pythoned" it :D
[OEIS](https://github.com/sidneycadot/oeis/blob/master/README.md)  | I took their README.md and just modified it ;)


Thanks to everyone!

Made by Asylum
