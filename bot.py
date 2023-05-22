import re
import os
import json
import openai
import discord
import logging
from collections import deque
from discord.ext import commands

script_dir = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(script_dir, 'config.json')
with open(config_path) as config_file:
    config = json.load(config_file)

logger = logging.getLogger('discord')

openai.api_key = config["openai_api_key"]

intents = discord.Intents.default()
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="<@{bot.user.id}>", intents=intents)

history = deque()
history_length = 0

context = config["context"]

global_personality = config["global_personality"]

def get_user(user):
    for entry in context:
        if entry["discord_name"].lower() == user.lower():
            return entry
    return None

def get_messages(sender, recipient, message):
    sender = sender.lower()
    sender_role = "assistant" if sender == "assistant" else "user"
    role = recipient.lower() if sender == "assistant" else sender

    user = get_user(role)
    personality = user['personality'] if user else config["global_personality"]

    bot_context=config["system_context"]

    system_role={"role": "system", "content": f"{bot_context}."}

    prefix='' if sender_role == 'assistant' else f"{personality}"
    add_message({"role": sender_role, "content": f"{prefix} {message}"})

    return [
      system_role,
      *[{"role": obj['role'], "content": obj['content']} for obj in history]
    ]

async def generate_response(message):
    try:
        if message.author == bot.user:
            return

        def call_openai_api():
            logger.info('Making a call to the OpenAI API')
            return openai.ChatCompletion.create(
                model=config["model"],
                messages=get_messages(message.author.name, 'assistant', message.content)
            )

        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a " + message.author.name))
        async with message.channel.typing():
            logger.info(message.author.name + ": " + message.content)
            response = await bot.loop.run_in_executor(None, call_openai_api)
            content = response['choices'][0]['message']['content']
            await message.reply(content)
            get_messages('assistant', message.author.name, content)
            logger.info("Assistant: " + content)
            logger.info("Tokens: " + str(response["usage"]["total_tokens"]))

        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=config["presence"]))

    except Exception as e:
        message.reply(config["error_message"])
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=config["presence"]))
        logging.error(f"Error generating response: {e}", exc_info=True)

def add_message(message):
    global history_length
    message_length = len(str(message))
    logger.info(f'Adding message of length {message_length} to history')

    while history_length > config["memory_characters"]:
        oldest_message = history.popleft()
        history_length -= len(str(oldest_message))
        logger.info(f'Removed message from history. Current history length is {history_length}')

    history.append(message)
    history_length += message_length
    logger.info(f'Added message to history. Current history length is {history_length}')

@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user} (ID: {bot.user.id})')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=config["presence"]))

@bot.event
async def on_message(message):
    if message.content.startswith(f'<@{bot.user.id}>'):
        user_id = re.findall(r'<@!?(\d+)>', message.content)[0]
        message.content = message.content.replace(f'<@{user_id}>', '').strip()
        await generate_response(message)

bot.run(config["discord_token"])