#https://discord.com/oauth2/authorize?client_id=1417235778492436550&permissions=2815162084478016&integration_type=0&scope=bot

import os
from openai import OpenAI
from dotenv import load_dotenv
import discord
from discord.ext import commands
import logging
from pathlib import Path


load_dotenv()

openai_key = os.getenv('OPENAI_API_KEY')
discord_token = os.getenv('DISCORD_TOKEN')
client = OpenAI(api_key=openai_key)


def talk_openai(question, instruction = "Give a short reply"):
    response = client.responses.create(
    model="gpt-5",
    instructions=f"You are a bot named Jarvis on a discord servers of some friends studying computer science. Please {instruction}",
    input=question
    )

    return response.output_text

def code_openai(question, instruction):
    response = client.responses.create(
        model="gpt-5",
        instructions=f"You are a bot named Jarvis on a discord server of some friends studying computer science. You are an expert on the field and you can provide a perfect answer to any question regarding our studies. Please {instruction}",
        input = question
    )

    return response.output_text

def vibe_openai(question, instruction, file, mode):
    if mode == 0:
        text = ""
        with open(file, "r") as file:
            text = file.read()
        response = client.responses.create(
            model="gpt-5",
            instructions=f"{question}. {instruction}",
            input = text
        )

        return response.output_text
    elif mode == 1:
        text = ""
        with open(file, "r") as file:
            text = file.read()
        response = client.responses.create(
            model="gpt-5",
            instructions=f"Improved code {question}. {instruction}. The old code is the input",
            input = text
        )

        return response.output_text

#def solve_openai(question, instruction, file):

#def summarize_openai(question, instruction, file):

#def quiz_openai(question, instruction, file):

async def get_file(msg):
    files = []
    for attachment in msg.attachments:
        SAVE_DIR = Path("Discord_Bot/reply_files")
        SAVE_DIR.mkdir(parents=True, exist_ok=True)

        safe_name = Path(attachment.filename).name  # strip any path components
        dest = SAVE_DIR / safe_name

        if dest.exists():
            stem, suffix = dest.stem, dest.suffix
            n = 1
            while True:
                candidate = SAVE_DIR / f"{stem} ({n}){suffix}"
                if not candidate.exists():
                    dest = candidate
                    break
                n += 1

        await attachment.save(dest)
        files.append(dest)
    return files

def save_file(text):
    SAVE_DIR = Path("Discord_Bot/reply_files")
    SAVE_DIR.mkdir(parents=True, exist_ok=True)

    safe_name = Path("reply.txt").name  # strip any path components
    dest = SAVE_DIR / safe_name

    if dest.exists():
        stem, suffix = dest.stem, dest.suffix
        n = 1
        while True:
            candidate = SAVE_DIR / f"{stem} ({n}){suffix}"
            if not candidate.exists():
                dest = candidate
                break
            n += 1
    with open(dest, "w") as file:
            file.write(text)
    return dest
    

handler = logging.FileHandler(filename='Discord_Bot/discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f"Hello, {bot.user.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    #message = "Hello"
    #instruct = "Give a friendly reply to the message by the user" + ctx.author
    #response = talk_openai(message, instruct)
    #await ctx.send(response)
    await ctx.send(f"Hello, {ctx.author.mention}!")

@bot.command()
async def ask(ctx, *, msg):
    user_name = ctx.author.display_name
    message = msg
    instruct = f"give a short and friendly reply to the user named {user_name}"
    reply = ""
    async with ctx.typing():
        try:
            reply = talk_openai(message, instruct)
        except Exception as e:
            await ctx.send(f"Sorry {ctx.author.mention}, I run into an error: {e}")
            return

    await ctx.send(f"{ctx.author.mention} {reply}")


@bot.command()
async def jarvis(ctx):
    await ctx.send("/hello -> Say hello to the bot \n /ask message -> Ask a question to chat gpt \n /jarvis -> Get a list of all the commands " \
    "\n /code -> Ask chat gpt for coding help \n /vibe -> Fix code using chat gpt by providing a file containing the code \n /solve -> Solve assignments using chat gpt " \
    "\n /summarize -> Get a summary of lecture slides \n /quiz -> Get a quiz on slides")

@bot.command()
async def code(ctx, *, msg):
    user_name = ctx.author.display_name
    message = msg
    instruct = f"give a complete and friendly reply to the user named {user_name}, But keep it correct, informative and keep it under 1000 characters"
    reply = ""
    async with ctx.typing():
        try:
            reply = code_openai(message, instruct)
        except Exception as e:
            await ctx.send(f"Sorry {ctx.author.mention}, I run into an error: {e}")
            return

    await ctx.send(f"{ctx.author.mention} {reply}")

@bot.command()
async def vibe(ctx, *, msg):
    files = await get_file(ctx.message)
    if(len(files) != 1):
        await ctx.send(f"{ctx.author.mention} Please provide one file")
        return
    user_name = ctx.author.display_name
    message = msg
    instruct = f"Return only the fixed code. No explanations needed"
    reply = ""
    async with ctx.typing():
        try:
            reply = vibe_openai(message, instruct, files[0], 0)
        except Exception as e:
            await ctx.send(f"Sorry {ctx.author.mention}, I run into an error: {e}")
            return

    dest = save_file(reply)

    message = reply
    instruct = f"Explain the improvements made in this code, keep it under 1000 characters"
    reply = ""
    async with ctx.typing():
        try:
            reply = vibe_openai(message, instruct, files[0], 1)
        except Exception as e:
            await ctx.send(f"Sorry {ctx.author.mention}, I run into an error: {e}")
            return

    await ctx.send(content = f"{ctx.author.mention} {reply}", file = discord.File(dest, filename=dest.name))

@bot.command()
async def solve(ctx, *, msg):
    await ctx.send(f"{ctx.author.mention}, this command is not yet available")

@bot.command()
async def summarize(ctx, *, msg):
    await ctx.send(f"{ctx.author.mention}, this command is not yet available")

@bot.command()
async def quiz(ctx, *, msg):
    await ctx.send(f"{ctx.author.mention}, this command is not yet available")


bot.run(discord_token, log_handler=handler, log_level=logging.DEBUG)