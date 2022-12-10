import discord
import dotenv
import os

# Load .env file
dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")

# Create bot
bot = discord.Bot()

# On bot ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# Load cogs
bot.load_extension("cogs.games")

# Run bot
bot.run(TOKEN)