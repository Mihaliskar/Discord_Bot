# Discord_Bot

Jarvis is a custom-built Discord bot powered by OpenAI’s GPT-5 API.
It interacts naturally with users, helps with coding questions, fixes uploaded code, and provides conversational responses — all directly inside a Discord server.

## Features

- /hello - Say hello to jarvis
- /ask message - Ask a question to jarvis
- /jarvis - Get a list of all the available commands
- /code - Ask for coding help
- /vibe - Upload a code file and receive both the improved version and an explanation
- /solve - Solve assignments using jarvis (coming soon)
- /summarize - Get a summary of text or lecture notes (coming soon)
- /quiz - Get a quiz on uploaded material (coming soon)

## Technologies

- Python - Programming Language
- Discord.py – Discord bot framework for commands and events
- OpenAI API (GPT-5) – AI-powered text generation and code improvement
- GitHub - Version control & CI/CD

## Installation

Clone the repo and run 
```
pip install -r requirements.txt
```

Create a .env file
```
DISCORD_TOKEN=your_discord_bot_token
OPENAI_API_KEY=your_openai_api_key
```

Add your discord bot to a server and run the application

```
python main.py
```

