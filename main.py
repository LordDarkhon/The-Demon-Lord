import discord
from discord.ext import commands
from datetime import timedelta
import os
import openai
import asyncio

# --- CONFIG ---

TOKEN = os.getenv("DISCORD_TOKEN")  # Your Discord Bot Token from Discord Developer Portal
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Your OpenAI API key

AI_TRIGGER_WORDS = ["lord", "my lord", "king", "my king"]
TIMEOUT_TRIGGER_WORDS = ["muzan", "kibutsuji", "darkhon", "tsukihiko"]
DEMON_ROLE_NAME = "Demon"
TIMEOUT_DURATION = timedelta(minutes=5)

# Setup intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

openai.api_key = OPENAI_API_KEY

async def get_ai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.8,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return "I am unable to respond right now."

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content_lower = message.content.lower()

    # AI response trigger
    if any(word in content_lower for word in AI_TRIGGER_WORDS):
        response = await get_ai_response(message.content)
        await message.channel.send(response)
        return

    # Timeout trigger for Demon role
    demon_role = discord.utils.get(message.guild.roles, name=DEMON_ROLE_NAME)
    if demon_role in message.author.roles:
        if any(word in content_lower for word in TIMEOUT_TRIGGER_WORDS):
            try:
                await message.author.timeout(duration=TIMEOUT_DURATION, reason="Forbidden word usage")
                await message.channel.send(f"{message.author.mention} has been timed out for forbidden words.")
            except Exception as e:
                await message.channel.send("I do not have permission to timeout users.")
            return

    await bot.process_commands(message)

bot.run(TOKEN)
