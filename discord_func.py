import discord
from discord.ext import commands
import logging
from pathlib import Path

from ai import *

class discord_func(commands.Cog):
    def __init__(self, bot, openai_key):
        self.bot = bot
        self.openai = ai(openai_key)

    async def get_file(self, msg):
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
    
    def save_file(self, text):
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
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Hello, {self.bot.user.name}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        #await self.bot.process_commands(message)

    

    @commands.command()
    async def hello(self, ctx):
        #message = "Hello"
        #instruct = "Give a friendly reply to the message by the user" + ctx.author
        #response = talk_openai(message, instruct)
        #await ctx.send(response)
        await ctx.send(f"Hello, {ctx.author.mention}!")

    @commands.command()
    async def ask(self, ctx, *, msg):
        user_name = ctx.author.display_name
        message = msg
        instruct = f"give a short and friendly reply to the user named {user_name}"
        reply = ""
        async with ctx.typing():
            try:
                reply = self.openai.talk_openai(message, instruct)
            except Exception as e:
                await ctx.send(f"Sorry {ctx.author.mention}, I run into an error: {e}")
                return

        await ctx.send(f"{ctx.author.mention} {reply}")


    @commands.command()
    async def jarvis(self, ctx):
        await ctx.send("/hello -> Say hello to the bot \n /ask message -> Ask a question to chat gpt \n /jarvis -> Get a list of all the commands " \
        "\n /code -> Ask chat gpt for coding help \n /vibe -> Fix code using chat gpt by providing a file containing the code \n /solve -> Solve assignments using chat gpt " \
        "\n /summarize -> Get a summary of lecture slides \n /quiz -> Get a quiz on slides")

    @commands.command()
    async def code(self, ctx, *, msg):
        user_name = ctx.author.display_name
        message = msg
        instruct = f"give a complete and friendly reply to the user named {user_name}, But keep it correct, informative and keep it under 1000 characters"
        reply = ""
        async with ctx.typing():
            try:
                reply = self.openai.code_openai(message, instruct)
            except Exception as e:
                await ctx.send(f"Sorry {ctx.author.mention}, I run into an error: {e}")
                return

        await ctx.send(f"{ctx.author.mention} {reply}")

    @commands.command()
    async def vibe(self, ctx, *, msg):
        files = await self.get_file(ctx.message)
        if(len(files) != 1):
            await ctx.send(f"{ctx.author.mention} Please provide one file")
            return
        user_name = ctx.author.display_name
        message = msg
        instruct = f"Return only the fixed code. No explanations needed"
        reply = ""
        async with ctx.typing():
            try:
                reply = self.openai.vibe_openai(message, instruct, files[0], 0)
            except Exception as e:
                await ctx.send(f"Sorry {ctx.author.mention}, I run into an error: {e}")
                return

        dest = self.save_file(reply)

        message = reply
        instruct = f"Explain the improvements made in this code, keep it under 1000 characters"
        reply = ""
        async with ctx.typing():
            try:
                reply = self.openai.vibe_openai(message, instruct, files[0], 1)
            except Exception as e:
                await ctx.send(f"Sorry {ctx.author.mention}, I run into an error: {e}")
                return

        await ctx.send(content = f"{ctx.author.mention} {reply}", file = discord.File(dest, filename=dest.name))

    @commands.command()
    async def solve(self, ctx, *, msg):
        await ctx.send(f"{ctx.author.mention}, this command is not yet available")

    @commands.command()
    async def summarize(self, ctx, *, msg):
        await ctx.send(f"{ctx.author.mention}, this command is not yet available")

    @commands.command()
    async def quiz(self, ctx, *, msg):
        await ctx.send(f"{ctx.author.mention}, this command is not yet available")
        
        

