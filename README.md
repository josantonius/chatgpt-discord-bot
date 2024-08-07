# ChatGPT Discord Bot

[![License](https://img.shields.io/github/license/josantonius/chatgpt-discord-bot)](LICENSE)

A bot designed for a small Discord channel among friends. This bot allows assigning a distinct
personality to each user and maintaining the context of previous questions and answers. It also has
the ability to view and understand images, so that one or more images can be attached to the message.
It's powered by OpenAI's ChatGPT models.

## Requirements

- Python 3.6 or above.
- An OpenAI API key.
- A Discord bot token.

## Installation

Clone this repository:

```console
git clone https://github.com/josantonius/chatgpt-discord-bot.git
```

Install the required Python packages:

```bash
pip install discord.py openai
```

## Configuration

Create a `config.json` file in the root directory of the bot. This is an example of how the
configuration file should look like:

```json
{
    "model": "gpt-4o",
    "memory_characters": 120000,
    "history_refresh_interval": 900,
    "history_refresh_success_message": "Context refreshed successfully!",
    "history_refresh_force_command": "refresh",
    "temperature": 0.4,
    "openai_api_key": "<Your OpenAI API key>",
    "discord_token": "<Your Discord Bot Token>",
    "presence": "The Lounge",
    "context": [
        {
            "discord_name": "Evellyne",
            "personality": "Evelyn is a seasoned data scientist. Interact in a polite and..."
        },
        {
            "discord_name": "Sammy",
            "personality": "Sam is a popular YouTube vlogger. Communicate in a cheerful and..."
        },
        {
            "discord_name": "Morgan",
            "personality": "Morgan is an NFT enthusiast. Respond to them with skepticism..."
        }
    ],
    "global_personality": "Maintain a cordial demeanor.",
    "system_context": "You are an admin of a Discord channel assigned by Evelyn.",
    "extra_system_contexts": {
        "#ue": "You are an expert on Unreal Engine. You respond professionally and technically.",
        "#gamedev": "You are a game developer. You respond with enthusiasm and creativity."
    },
    "error_message": "Words fail me at the moment :/"
}
```

`model` is the model that the bot will use. The available models are `gpt-4o`, `gpt-4`, `gpt-3.5-turbo`,

`memory_characters` are the number of characters that the bot will remember from previous messages.
This value should not exceed the maximum number of tokens allowed by the model you are using.

`history_refresh_interval` is the interval in seconds at which the chat context is refreshed.

`history_refresh_success_message` is the message that the bot will send when the context is refreshed.

`history_refresh_force_command` is the command that users can use to force a context refresh.

`temperature` is the temperature parameter used when generating responses. Lower values will result.

Replace `<Your OpenAI API key>` and `<Your Discord Bot Token>` with your actual OpenAI API key and
Discord bot token respectively.

Each user in your Discord channel should have an entry in the `context` array with their Discord
username and the personality you want the bot to use when interacting with them. If a user does not
have a specific entry, the bot will use the `global_personality`.

The original names of Discord users are not sent to ChatGPT for privacy. Instead, the bot uses the
`discord_name` field to identify users.

The `system_context` is the initial context of the conversation with the bot.

`extra_system_contexts` is a dictionary of additional system contexts that can be used by the bot. If the message includes any of the hastags in the message, the corresponding context will be used instead of the default `system_context`.

## Running the Bot

Once you have set up the configuration file, you can run the bot using Python:

```bash
python bot.py
```

Your bot should now be running and ready to interact with in your Discord server!

## Commands

The bot is summoned by mentioning it at the start of the message. For example:

```txt
@ChatGPT How are you?
```

**It also has the ability to view and understand images, so that one or more images can be attached to the message.**

## Logging

The bot logs all messages and API calls for debugging purposes. The log is printed to the console.

## TODO

- [ ] Add new feature
- [ ] Add tests
- [ ] Improve documentation

## Changelog

Detailed changes for each release are documented in the
[release notes](https://github.com/josantonius/chatgpt-discord-bot/releases).

## Contribution

Please make sure to read the [Contributing Guide](.github/CONTRIBUTING.md), before making a pull
request, start a discussion or report a issue.

Thanks to all [contributors](https://github.com/josantonius/chatgpt-discord-bot/graphs/contributors)! :heart:

## Sponsor

If this project helps you to reduce your development time,
[you can sponsor me](https://github.com/josantonius#sponsor) to support my open source work :blush:

## License

This repository is licensed under the [MIT License](LICENSE).

Copyright © 2023-present, [Josantonius](https://github.com/josantonius#contact)
