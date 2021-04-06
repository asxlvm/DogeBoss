# DogeBoss

![](https://img.shields.io/badge/Python-3.5--3.8-green)
![GitHub stars](https://img.shields.io/github/stars/asxlvm/DogeBoss)
[![Run on Repl.it](https://repl.it/badge/github/asxlvm/DogeBoss)](https://repl.it/github/asxlvm/DogeBoss)

This repository contains the source of an Open-Source [DogeHouse](https://www.dogehouse.tv) bot programmed in Python, use the code however you want.

## What you need:

To run the bot yourself, you will need these three things:

1. Python 3.x (You won't need it downloaded on your device if you're using replit)
2. Your account token and account refresh token
3. All the modules in requirements.txt

## How to get your account token and account refresh token?

1. Go to [DogeHouse](https://dogehouse.tv)
2. Login to the "bot" account
3. Open Developer options (F12 or Ctrl+Shift+I)
4. Go to Application > Local Storage > dogehouse.tv
5. Copy your token and refresh-token and put them in an .env file:

```
DOGEHOUSE_TOKEN = "DOGEHOUSE TOKEN HERE"

DOGEHOUSE_REFRESH_TOKEN = "DOGEHOUSE REFRESH TOKEN HERE"
```

How to get all the modules in requirements.txt?

1. Run `pip install -r requirements.txt`
2. Wait, and after a few minutes or less, you should have every module downloaded

## Running on Repl.it 
  - If you want 24/7 hosting of the bot on repl.it, change the variable `run_on_repl` to `True` in `main.py`.
  
  - To monitor your bot's uptime, go to [Uptime Robot](https://uptimerobot.com), register an account if you don't have one already and then do the following:
    - Create a new monitor with these parameters:
      - Monitor Type: HTTP(s)
      - Friendly Name: `Of your own choice, doesn't matter`
      - URL (or IP);
        - Start your script on replit, go to "Web", copy the URL at the top and paste it in the field
      - Click on "Create Monitor" and confirm by clicking "! Create Monitor (with no alert contact selected)"

Commands (this list does not contain all of them!)
--------------------

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

TODO:
--------------

1. d!joke & d!dadjoke
2. d!tictactoe (I have that done but I need to wait till \n new lines work)
3. Economy
4. Complex `d!fight` command with `wait_for` events etc.
5. Adding `None` values to commands so they're used easily and can return errors etc.

Thanks to everyone!
