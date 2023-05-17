# ChatGPT Discord Bot

[![License](https://img.shields.io/github/license/josantonius/chatgpt-discord-bot)](LICENSE)

A bot designed for a small Discord channel among friends.
This bot allows assigning a distinct personality to each user and maintaining the
context of previous questions and answers. It's powered by OpenAI's ChatGPT models.

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
    "model": "gpt-4",
    "max_tokens": 500,
    "temperature": 0.6,
    "openai_api_key": "<Your OpenAI API key>",
    "discord_token": "<Your Discord Bot Token>",
    "presence": "The Lounge",
    "context": [
        {
            "discord_name": "Evellyne",
            "personality": "Evelyn is a seasoned data scientist. Interact in a polite and informative manner."
        },
        {
            "discord_name": "Sammy",
            "personality": "Sam is a popular YouTube vlogger. Communicate in a cheerful and supportive way."
        },
        {
            "discord_name": "Morgan",
            "personality": "Morgan is an NFT enthusiast. Respond to them with slight skepticism and wit."
        }
    ],
    "global_personality": "Maintain a cordial demeanor.",
    "system_context": "You are an admin of a Discord channel assigned by Evelyn.",
    "error_message": "Words fail me at the moment :/"
}
```

Replace `<Your OpenAI API key>` and `<Your Discord Bot Token>` with your actual OpenAI API key and
Discord bot token respectively.

Each user in your Discord channel should have an entry in the `context` array with their Discord
username and the personality you want the bot to use when interacting with them. If a user does not
have a specific entry, the bot will use the `global_personality`.

The original names of Discord users are not sent to ChatGPT for privacy. Instead, the bot uses the
`discord_name` field to identify users.

The `system_context` is the initial context of the conversation with the bot.

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
