import discord
from discord.ext import commands
import comands as custom_comands
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)
custom_comands.setup(bot)

@bot.event
async def on_ready():
    print(f"{bot.user} jest gotowy")
    await bot.tree.sync()

bot.run(TOKEN)