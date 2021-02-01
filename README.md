# HKN_Discord_Bot

## Setup
This bot is entirely cloud-based, so you don't have to install any software on your computer to run it. <br /> <br />
Follow the instructions in [this tutorial](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/) to get started. Note that the Flask server in this tutorial is different from the one used. Discord has now set a limit on the number of times you can ping the API. <br /> <br />
The code for never_sleep.py was taken directly from [this Replit forum](https://repl.it/talk/ask/Uptime-Robot-not-working-with-Discord-Cloudflare/49491). Next, you will need an external pinger, like [UptimeRobot](https://uptimerobot.com/) to keep the bot alive. An HTTPS pinger with the never_sleep server address was used for this project. <br /> <br />
Since this bot uses a spreadsheet, you will need to set up an interface between the bot and the spreadsheet. Follow [this tutorial](https://gspread.readthedocs.io/en/latest/oauth2.html#enable-api-access) to enable API access for the project. The service_account.json was converted to a .env file. The gspread module was used in this project to interact with the spreadsheet. Its documentation is found [here](https://github.com/burnash/gspread).

## Testing
To test the bot, connect it with a Discord server. When you run the code in Replit, you will see the following message printed in the terminal:

`We've logged in as [Bot Name]`

To check if the bot is responding, you can use the $hello command. If the bot is setup correctly, it should respond with:

`Hello!`

## Spreadsheet Setup
The first row is assume to have column names as shown below:

| Name | Discord Username | VC Start | VC End | Weekly Elapsed Time | Running Total |
| ---- | ---------------- | -------- | ------ | ------------------- | ------------- |
