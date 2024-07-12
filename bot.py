import re
import os
import json
import openai
import discord
import logging
import time
from collections import deque
from discord.ext import commands

script_dir = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(script_dir, 'config.json')
with open(config_path) as config_file:
    config = json.load(config_file)

logger = logging.getLogger('discord')

openai.api_key = config["openai_api_key"]

intents = discord.Intents.all()
intents.messages = True
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix="<@{bot.user.id}>", intents=intents)

history = deque()
history_length = 0
last_activity_time = time.time()
context = config["context"]
history_refresh_interval = config["history_refresh_interval"]

global_personality = config["global_personality"]

def get_user(user):
    for entry in context:
        if entry["discord_name"].lower() == user.lower():
            return entry
    return None

def get_bot_context(message_content):
    for tag, bot_context in config["extra_system_contexts"].items():
        if tag in message_content:
            return bot_context
    return config["system_context"]

def get_messages(sender, recipient, message, image_urls=None):
    sender = sender.lower()
    sender_role = "assistant" if sender == "assistant" else "user"
    role = recipient.lower() if sender == "assistant" else sender

    user = get_user(role)
    personality = user['personality'] if user else global_personality

    bot_context = get_bot_context(message)

    user_message_content = [{"type": "text", "text": f"{personality} {message}"}] if sender_role == "user" else [{"type": "text", "text": message}]

    messages = [
        {
            "role": "system",
            "content": bot_context
        },
        *[
            {"role": obj['role'], "content": obj['content']} for obj in history
        ],
        {
            "role": sender_role,
            "content": user_message_content
        }
    ]

    if image_urls:
        for url in image_urls:
            messages[-1]["content"].append({
                "type": "image_url",
                "image_url": {
                    "url": url,
                    "detail": "auto"
                }
            })

    return messages

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

def clear_history():
    global history, history_length
    history.clear()
    history_length = 0
    logger.info('History cleared due to inactivity')

async def send_long_message(channel, content):
    chunks = [content[i:i + 2000] for i in range(0, len(content), 2000)]
    for chunk in chunks:
        await channel.send(chunk)

async def generate_response(message):
    global last_activity_time
    last_activity_time = time.time()
    try:
        image_urls = []
        image_descriptions = []

        if message.attachments:
            for attachment in message.attachments:
                if any(attachment.filename.lower().endswith(image_ext) for image_ext in ['jpg', 'jpeg', 'png', 'gif']):
                    image_urls.append(attachment.url)

        def call_openai_api():
            logger.info('Making a call to the OpenAI API')
            return openai.ChatCompletion.create(
                model=config["model"],
                messages=get_messages(message.author.name, 'assistant', message.content, image_urls=image_urls)
            )

        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a " + message.author.display_name))
        async with message.channel.typing():
            logger.info(message.author.display_name + ": " + message.content)
            response = await bot.loop.run_in_executor(None, call_openai_api)
            content = response['choices'][0]['message']['content']

            add_message({"role": "user", "content": message.content})

            if image_urls:
                for description in content.split('\n'):
                    image_descriptions.append(description)
                    add_message({"role": "assistant", "content": f"Descripción de imagen: {description}"})
            else:
                add_message({"role": "assistant", "content": content})

            await send_long_message(message.channel, content)
            logger.info("Assistant: " + content)
            logger.info("Tokens: " + str(response["usage"]["total_tokens"]))

    except Exception as e:
        await message.reply(config["error_message"])
        logging.error(f"Error generating response: {e}", exc_info=True)
    finally:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=config["presence"]))

@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user} (ID: {bot.user.id})')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=config["presence"]))

@bot.event
async def on_message(message):
    global last_activity_time
    if message.content.startswith(f'<@{bot.user.id}>'):
        current_time = time.time()
        if current_time - last_activity_time > history_refresh_interval:
            clear_history()
        last_activity_time = current_time
        user_id = re.findall(r'<@!?(\d+)>', message.content)[0]
        command = message.content.replace(f'<@{user_id}>', '').strip()
        if command.lower() == config["history_refresh_force_command"]:
            clear_history()
            await message.channel.send(config["history_refresh_success_message"])
        else:
            await generate_response(message)

bot.run(config["discord_token"])
