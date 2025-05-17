import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "muzan" in message.content.lower():
        await message.channel.send(f"Beware... I see you, {message.author.mention}.")

    await bot.process_commands(message)

bot.run("YOUR_BOT_TOKEN_HERE")
