import never_sleep
never_sleep.awake('https://Discord-Tutoring-Bot.hknatucla.repl.co', False)
import discord
from discord.ext.commands import Bot
import os
import gspread
import time

bot = Bot(command_prefix = "$", help_command = None)

NAME = 'A'
DISCORD_USERNAME = 'B'
VC_START = 'C'
VC_END = 'D'
ELAPSED = 'E'
RUNNING_TOTAL = 'F'
REQUIRED_ROLE = "Moderator"

def next_available_row(worksheet):
  str_list = list(filter(None, worksheet.col_values(1)))
  return str(len(str_list)+1)

def get_row(name, addRow):
  try:
    cell = str(sheet.find(name))
    row_test = ''
    for k in range(7, len(cell)):
      if cell[k].isdigit():
        row_test += cell[k]
      else:
        break
    return row_test
  except:
    if addRow:
      return next_available_row(sheet)
  return -1

def register_user(name, username):
  row = get_row(name, True)
  sheet.update(NAME + str(row), name)
  sheet.update(DISCORD_USERNAME + str(row), username)
  sheet.update(VC_START + str(row), 0)
  sheet.update(VC_END + str(row), 0)
  sheet.update(ELAPSED + str(row), 0)
  sheet.update(RUNNING_TOTAL + str(row), 0)
  return

def start_clock(member):
  row = get_row(member.name, False)
  if row != -1:
    sheet.update(VC_START + str(row), time.time())
  return

def stop_clock(member):
  row = get_row(member.name, False)
  if row != -1:
    end_time = time.time()
    sheet.update(VC_END + str(row), end_time)
    start_time = int(sheet.get(VC_START + str(row))[0][0])
    elapsed_time = round(end_time - start_time, 0)
    weekly_elapsed = int(sheet.get(ELAPSED + str(row))[0][0])
    sheet.update(ELAPSED + str(row), elapsed_time + weekly_elapsed)
    if (elapsed_time + weekly_elapsed)/3600 > 1.8:
      running_total = float(sheet.get(RUNNING_TOTAL + str(row))[0][0])
      sheet.update(RUNNING_TOTAL + str(row), round(running_total + 2, 0))
    sheet.update(VC_START + str(row), 0)
    sheet.update(VC_END + str(row), 0)

gc = gspread.service_account(filename='service_account.env')

SAMPLE_SPREADSHEET_ID = os.getenv('SAMPLE_SPREADSHEET_ID')
sheet = gc.open_by_key(SAMPLE_SPREADSHEET_ID).sheet1

@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='$help'))
  print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def hello(ctx):
  await ctx.send('Hello!')

@bot.command()
async def help(ctx):
  msg = "Hello! I\'m **Tutoring Logger**, HKN\'s new Discord Bot! \n Check out the Tutoring Schedule here:"

  tutoring_schedule = discord.Embed(title="HKN Tutoring Schedule", url = "https://docs.google.com/spreadsheets/d/1boLY5YeM630_9v_-72Nf6QcSYytRfF7tBTr_P62NX50/edit?usp=sharing")

  await ctx.send(msg)
  await ctx.send(embed = tutoring_schedule)

@bot.command()
async def register(ctx, *args):
  if len(args) < 2:
    await ctx.send("Please enter your first name, a space, then your last name exactly as on the inductee spreadsheet after the register command. Ex: $register Joe Bruin")
    return
  
  full_name = str(args[0]) + " " + str(args[1])
  await ctx.send('Registering you as ' + full_name + '!')
  register_user(full_name, str(ctx.message.author.name))
  await ctx.send('Your data has been successfully submitted!')

@bot.command()
async def reset(ctx):
  if discord.utils.get(ctx.author.roles, name = REQUIRED_ROLE) == None:
    await ctx.send("Whoops! You don't have the required role for that command.")
    return
  
  for i in range(2, int(next_available_row(sheet))):
    sheet.update(ELAPSED + str(i), 0)
  await ctx.send("Weekly elapsed time has been reset.")

@bot.event
async def on_voice_state_update(member, member_before, member_after):
    
  voice_channel_before = member_before.channel
  voice_channel_after = member_after.channel

  valid_voice_channels = ['general', 'tutoring room 1', 'tutoring room 2', 'tutoring room 3', 'Available Tutors']
    
  if voice_channel_before == voice_channel_after:
    # No change
    return
    
  if voice_channel_before == None:
    # The member was not on a voice channel before the change
    if voice_channel_after.name not in valid_voice_channels:
      return
    start_clock(member)

  else:
    # The member was on a voice channel before the change
    if voice_channel_after == None:
      # The member is no longer on a voice channel after the change
      if voice_channel_before.name not in valid_voice_channels:
        return
      stop_clock(member)

    else:
      # The member is still on a voice channel after the change
      # switching from non-valid to valid
      if voice_channel_before.name not in valid_voice_channels and voice_channel_after.name in valid_voice_channels:
        start_clock(member)
      # switching from valid to non-valid
      if voice_channel_before.name in valid_voice_channels and voice_channel_after.name not in valid_voice_channels:
        stop_clock(member)
      # remaining in a valid channel
      if voice_channel_before.name in valid_voice_channels and voice_channel_after.name in valid_voice_channels:
        return

bot.run(os.getenv('TOKEN'))
