import subprocess
import psutil
import pyautogui
import disnake
import time
from disnake.ext import commands
import win32gui
from win32gui import SetForegroundWindow

token = ''  # Discord Bot token for login.

# Creating a commands.Bot() instance and using 'bot'
bot = commands.Bot()

# Setup allowed mentions by Discord bot
disnake.AllowedMentions(everyone=True, users=True, roles=True, replied_user=True)

guilds = [] # Enter Discord servers here.

serverproc = None


@bot.event  # Bot has launched and is ready.
async def on_ready():
    print("The bot is ready!")
    discordactivity = "people die."  # Update Discord status
    activity = disnake.Activity(name=discordactivity, type=disnake.ActivityType.watching)
    await bot.change_presence(activity=activity)


@bot.slash_command(guild_ids=guilds)
async def start_server(inter):
    global serverproc
    await inter.send("Starting the server!")
    serverproc = subprocess.Popen(r'D:\Steam\steamapps\common\Project Zomboid Dedicated Server\StartServer64.bat', creationflags=subprocess.CREATE_NEW_CONSOLE)


@bot.slash_command(guild_ids=guilds)
async def stop_server(inter):
    await inter.send("Gracefully stopping the server. Please wait for the confirmation message that the server has been stopped before starting it again!")
    hwnd = win32gui.FindWindow(None, "C:\WINDOWS\system32\cmd.exe")  # Grab our command prompt window
    SetForegroundWindow(hwnd)  # Bring the command prompt window to the foreground so we can type commands
    pyautogui.typewrite("quit")  # This will type our quit command
    pyautogui.typewrite(["enter"])  # This will fire off the quit command
    print("Sleeping for 60")
    time.sleep(60)  # Waits for the server to save and tidy up
    print("Finishing the quit")
    pyautogui.typewrite(["enter"])  # Fires off the final key to close out the command prompt.
    await inter.followup.send("The server has been stopped and is safe to restart!")


@bot.slash_command(guild_ids=guilds)
async def terminate_server(inter):
    global serverproc
    await inter.send("Terminating the server!")
    try:
        parent_pid = serverproc.pid  # Kill parents and children
        parent = psutil.Process(parent_pid)
        for child in parent.children(recursive=True):  # or parent.children() for recursive=False
            child.kill()
        parent.kill()
    except:
        await inter.followup.send("The server is not running or we encountered an error!")


@bot.slash_command(guild_ids=guilds)
async def hp_check(inter):
    cpu = psutil.cpu_percent()  # Grab our CPU %
    ram = psutil.virtual_memory().percent  # Grab our RAM %
    await inter.send(f'Current CPU utilization:`{cpu}%`\nCurrent RAM Usage:`{ram}`%')


bot.run(token)  # Authenticate to Discord via our local token
