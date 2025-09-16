#https://discord.com/oauth2/authorize?client_id=1417235778492436550&permissions=2815162084478016&integration_type=0&scope=bot

import os
from openai import OpenAI
from dotenv import load_dotenv
import discord
from discord.ext import commands
import logging


load_dotenv()

openai_key = os.getenv('OPENAI_API_KEY')
discord_token = os.getenv('DISCORD_TOKEN')
client = OpenAI(api_key=openai_key)

'''
question = input("Ask me something: ")

response = client.responses.create(
    model="gpt-5",
    instructions="Give short answers",
    input=question
)

print(response.output_text)

'''

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


handler = logging.FileHandler(filename='Github_Bot/discord.log', encoding='utf-8', mode='w')
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
    await ctx.send(f"{ctx.author.mention}, this command is not yet available")

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