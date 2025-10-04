#https://discord.com/oauth2/authorize?client_id=1417235778492436550&permissions=2815162084478016&integration_type=0&scope=bot

import os
from dotenv import load_dotenv
import asyncio
from discord_func import *



load_dotenv()

openai_key = os.getenv('OPENAI_API_KEY')
discord_token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='Discord_Bot/discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='/', intents=intents)
handler = logging.FileHandler(filename='Discord_Bot/discord.log', encoding='utf-8', mode='w')
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


async def main():
    async with bot:
        await bot.add_cog(discord_func(bot, openai_key))  # <-- await this
        await bot.start(discord_token)



asyncio.run(main())